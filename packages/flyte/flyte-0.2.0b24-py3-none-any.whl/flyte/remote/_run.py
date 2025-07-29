from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, AsyncIterator, Iterator, List, Literal, Tuple, Union, cast

import grpc
import rich.repr
from google.protobuf import timestamp
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from flyte._initialize import ensure_client, get_client, get_common_config
from flyte._protos.common import identifier_pb2, list_pb2
from flyte._protos.workflow import run_definition_pb2, run_service_pb2
from flyte.syncify import syncify

from .._protos.workflow.run_service_pb2 import WatchActionDetailsResponse
from ._console import get_run_url
from ._logs import Logs

WaitFor = Literal["terminal", "running", "logs-ready"]


def _action_time_phase(action: run_definition_pb2.Action | run_definition_pb2.ActionDetails) -> rich.repr.Result:
    """
    Rich representation of the action time and phase.
    """
    start_time = timestamp.to_datetime(action.status.start_time, timezone.utc)
    yield "start_time", start_time.isoformat()
    if action.status.phase in [
        run_definition_pb2.PHASE_FAILED,
        run_definition_pb2.PHASE_SUCCEEDED,
        run_definition_pb2.PHASE_ABORTED,
        run_definition_pb2.PHASE_TIMED_OUT,
    ]:
        end_time = timestamp.to_datetime(action.status.end_time, timezone.utc)
        yield "end_time", end_time.isoformat()
        yield "run_time", f"{(end_time - start_time).seconds} secs"
    else:
        yield "end_time", None
        yield "run_time", f"{(datetime.now(timezone.utc) - start_time).seconds} secs"
    yield "phase", run_definition_pb2.Phase.Name(action.status.phase)
    if isinstance(action, run_definition_pb2.ActionDetails):
        yield (
            "error",
            f"{action.error_info.kind}: {action.error_info.message}" if action.HasField("error_info") else "NA",
        )


def _action_rich_repr(action: run_definition_pb2.Action) -> rich.repr.Result:
    """
    Rich representation of the action.
    """
    yield "run", action.id.run.name
    if action.metadata.HasField("task"):
        yield "task", action.metadata.task.id.name
        yield "type", "task"
    yield "name", action.id.name
    yield from _action_time_phase(action)
    yield "group", action.metadata.group
    yield "parent", action.metadata.parent
    yield "attempts", action.status.attempts


def _attempt_rich_repr(action: List[run_definition_pb2.ActionAttempt]) -> rich.repr.Result:
    for attempt in action:
        yield "attempt", attempt.attempt
        yield "phase", run_definition_pb2.Phase.Name(attempt.phase)
        yield "logs_available", attempt.logs_available


def _action_details_rich_repr(action: run_definition_pb2.ActionDetails) -> rich.repr.Result:
    """
    Rich representation of the action details.
    """
    yield "name", action.id.run.name
    yield from _action_time_phase(action)
    yield "task", action.resolved_task_spec.task_template.id.name
    yield "task_type", action.resolved_task_spec.task_template.type
    yield "task_version", action.resolved_task_spec.task_template.id.version
    yield "attempts", action.attempts
    yield "error", f"{action.error_info.kind}: {action.error_info.message}" if action.HasField("error_info") else "NA"
    yield "phase", run_definition_pb2.Phase.Name(action.status.phase)
    yield "group", action.metadata.group
    yield "parent", action.metadata.parent


def _action_done_check(phase: run_definition_pb2.Phase) -> bool:
    """
    Check if the action is done.
    """
    return phase in [
        run_definition_pb2.PHASE_FAILED,
        run_definition_pb2.PHASE_SUCCEEDED,
        run_definition_pb2.PHASE_ABORTED,
        run_definition_pb2.PHASE_TIMED_OUT,
    ]


@dataclass
class Run:
    """
    A class representing a run of a task. It is used to manage the run of a task and its state on the remote
    Union API.
    """

    pb2: run_definition_pb2.Run
    action: Action = field(init=False)
    _details: RunDetails | None = None

    def __post_init__(self):
        """
        Initialize the Run object with the given run definition.
        """
        if not self.pb2.HasField("action"):
            raise RuntimeError("Run does not have an action")
        self.action = Action(self.pb2.action)

    @syncify
    @classmethod
    async def listall(
        cls,
        filters: str | None = None,
        sort_by: Tuple[str, Literal["asc", "desc"]] | None = None,
    ) -> AsyncIterator[Run]:
        """
        Get all runs for the current project and domain.

        :param filters: The filters to apply to the project list.
        :param sort_by: The sorting criteria for the project list, in the format (field, order).
        :return: An iterator of runs.
        """
        ensure_client()
        token = None
        sort_by = sort_by or ("created_at", "asc")
        sort_pb2 = list_pb2.Sort(
            key=sort_by[0], direction=list_pb2.Sort.ASCENDING if sort_by[1] == "asc" else list_pb2.Sort.DESCENDING
        )
        cfg = get_common_config()
        while True:
            req = list_pb2.ListRequest(
                limit=100,
                token=token,
                sort_by=sort_pb2,
            )
            resp = await get_client().run_service.ListRuns(
                run_service_pb2.ListRunsRequest(
                    request=req,
                    org=cfg.org,
                    project_id=identifier_pb2.ProjectIdentifier(
                        organization=cfg.org,
                        domain=cfg.domain,
                        name=cfg.project,
                    ),
                )
            )
            token = resp.token
            for r in resp.runs:
                yield cls(r)
            if not token:
                break

    @syncify
    @classmethod
    async def get(cls, name: str) -> Run:
        """
        Get the current run.

        :return: The current run.
        """
        ensure_client()
        run_details: RunDetails = await RunDetails.get.aio(name=name)
        run = run_definition_pb2.Run(
            action=run_definition_pb2.Action(
                id=run_details.action_id,
                metadata=run_details.action_details.pb2.metadata,
                status=run_details.action_details.pb2.status,
            ),
        )
        return cls(pb2=run, _details=run_details)

    @property
    def name(self) -> str:
        """
        Get the name of the run.
        """
        return self.pb2.action.id.run.name

    @property
    def phase(self) -> str:
        """
        Get the phase of the run.
        """
        return self.action.phase

    @property
    def raw_phase(self) -> run_definition_pb2.Phase:
        """
        Get the raw phase of the run.
        """
        return self.action.raw_phase

    @syncify
    async def wait(self, quiet: bool = False, wait_for: Literal["terminal", "running"] = "terminal") -> None:
        """
        Wait for the run to complete, displaying a rich progress panel with status transitions,
        time elapsed, and error details in case of failure.
        """
        return await self.action.wait(quiet=quiet, wait_for=wait_for)

    async def watch(self, cache_data_on_done: bool = False) -> AsyncGenerator[ActionDetails, None]:
        """
        Get the details of the run. This is a placeholder for getting the run details.
        """
        return self.action.watch(cache_data_on_done=cache_data_on_done)

    async def show_logs(
        self,
        attempt: int | None = None,
        max_lines: int = 100,
        show_ts: bool = False,
        raw: bool = False,
        filter_system: bool = False,
    ):
        await self.action.show_logs(attempt, max_lines, show_ts, raw, filter_system=filter_system)

    @syncify
    async def details(self) -> RunDetails:
        """
        Get the details of the run. This is a placeholder for getting the run details.
        """
        if self._details is None:
            self._details = await RunDetails.get_details.aio(self.pb2.action.id.run)
        return self._details

    @property
    def url(self) -> str:
        """
        Get the URL of the run.
        """
        client = get_client()
        return get_run_url(
            client.endpoint,
            insecure=client.insecure,
            project=self.pb2.action.id.run.project,
            domain=self.pb2.action.id.run.domain,
            run_name=self.name,
        )

    @syncify
    async def abort(self):
        """
        Aborts / Terminates the run.
        """
        try:
            await get_client().run_service.AbortRun(
                run_service_pb2.AbortRunRequest(
                    run_id=self.pb2.action.id.run,
                )
            )
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return
            raise

    def done(self) -> bool:
        """
        Check if the run is done.
        """
        return self.action.done()

    def sync(self) -> Run:
        """
        Sync the run with the remote server. This is a placeholder for syncing the run.
        """
        return self

    # TODO add add_done_callback, maybe implement sync apis etc

    def __rich_repr__(self) -> rich.repr.Result:
        """
        Rich representation of the Run object.
        """
        yield from _action_rich_repr(self.pb2.action)

    def __repr__(self) -> str:
        """
        String representation of the Action object.
        """
        import rich.pretty

        return rich.pretty.pretty_repr(self)


@dataclass
class RunDetails:
    """
    A class representing a run of a task. It is used to manage the run of a task and its state on the remote
    Union API.
    """

    pb2: run_definition_pb2.RunDetails
    action_details: ActionDetails = field(init=False)

    def __post_init__(self):
        """
        Initialize the RunDetails object with the given run definition.
        """
        self.action_details = ActionDetails(self.pb2.action)

    @syncify
    @classmethod
    async def get_details(cls, run_id: run_definition_pb2.RunIdentifier) -> RunDetails:
        """
        Get the details of the run. This is a placeholder for getting the run details.
        """
        ensure_client()
        resp = await get_client().run_service.GetRunDetails(
            run_service_pb2.GetRunDetailsRequest(
                run_id=run_id,
            )
        )
        return cls(resp.details)

    @syncify
    @classmethod
    async def get(cls, name: str | None = None) -> RunDetails:
        """
        Get a run by its ID or name. If both are provided, the ID will take precedence.

        :param uri: The URI of the run.
        :param name: The name of the run.
        """
        ensure_client()
        cfg = get_common_config()
        return await RunDetails.get_details.aio(
            run_id=run_definition_pb2.RunIdentifier(
                org=cfg.org,
                project=cfg.project,
                domain=cfg.domain,
                name=name,
            ),
        )

    @property
    def name(self) -> str:
        """
        Get the name of the action.
        """
        return self.action_details.run_name

    @property
    def task_name(self) -> str | None:
        """
        Get the name of the task.
        """
        return self.action_details.task_name

    @property
    def action_id(self) -> run_definition_pb2.ActionIdentifier:
        """
        Get the action ID.
        """
        return self.action_details.action_id

    def done(self) -> bool:
        """
        Check if the run is in a terminal state (completed or failed). This is a placeholder for checking the
        run state.
        """
        return self.action_details.done()

    async def inputs(self) -> ActionInputs:
        """
        Placeholder for inputs. This can be extended to handle inputs from the run context.
        """
        return await self.action_details.inputs()

    async def outputs(self) -> ActionOutputs:
        """
        Placeholder for outputs. This can be extended to handle outputs from the run context.
        """
        return await self.action_details.outputs()

    def __rich_repr__(self) -> rich.repr.Result:
        """
        Rich representation of the Run object.
        """
        yield "labels", str(self.pb2.run_spec.labels)
        yield "annotations", str(self.pb2.run_spec.annotations)
        yield "env-vars", str(self.pb2.run_spec.envs)
        yield "is-interruptible", str(self.pb2.run_spec.interruptible)
        yield "cache-overwrite", self.pb2.run_spec.overwrite_cache
        yield from _action_details_rich_repr(self.pb2.action)

    def __repr__(self) -> str:
        """
        String representation of the Action object.
        """
        import rich.pretty

        return rich.pretty.pretty_repr(self)


@dataclass
class Action:
    """
    A class representing an action. It is used to manage the run of a task and its state on the remote Union API.
    """

    pb2: run_definition_pb2.Action
    _details: ActionDetails | None = None

    @syncify
    @classmethod
    async def listall(
        cls,
        for_run_name: str,
        filters: str | None = None,
        sort_by: Tuple[str, Literal["asc", "desc"]] | None = None,
    ) -> Union[Iterator[Action], AsyncIterator[Action]]:
        """
        Get all actions for a given run.

        :param for_run_name: The name of the run.
        :param filters: The filters to apply to the project list.
        :param sort_by: The sorting criteria for the project list, in the format (field, order).
        :return: An iterator of projects.
        """
        ensure_client()
        token = None
        sort_by = sort_by or ("created_at", "asc")
        sort_pb2 = list_pb2.Sort(
            key=sort_by[0], direction=list_pb2.Sort.ASCENDING if sort_by[1] == "asc" else list_pb2.Sort.DESCENDING
        )
        cfg = get_common_config()
        while True:
            req = list_pb2.ListRequest(
                limit=100,
                token=token,
                sort_by=sort_pb2,
            )
            resp = await get_client().run_service.ListActions(
                run_service_pb2.ListActionsRequest(
                    request=req,
                    run_id=run_definition_pb2.RunIdentifier(
                        org=cfg.org,
                        project=cfg.project,
                        domain=cfg.domain,
                        name=for_run_name,
                    ),
                )
            )
            token = resp.token
            for r in resp.actions:
                yield cls(r)
            if not token:
                break

    @syncify
    @classmethod
    async def get(cls, uri: str | None = None, /, run_name: str | None = None, name: str | None = None) -> Action:
        """
        Get a run by its ID or name. If both are provided, the ID will take precedence.

        :param uri: The URI of the action.
        :param run_name: The name of the action.
        :param name: The name of the action.
        """
        ensure_client()
        cfg = get_common_config()
        details: ActionDetails = await ActionDetails.get_details.aio(
            run_definition_pb2.ActionIdentifier(
                run=run_definition_pb2.RunIdentifier(
                    org=cfg.org,
                    project=cfg.project,
                    domain=cfg.domain,
                    name=run_name,
                ),
                name=name,
            ),
        )
        return cls(
            pb2=run_definition_pb2.Action(
                id=details.action_id,
                metadata=details.pb2.metadata,
                status=details.pb2.status,
            ),
            _details=details,
        )

    @property
    def phase(self) -> str:
        """
        Get the phase of the action.
        """
        return run_definition_pb2.Phase.Name(self.pb2.status.phase)

    @property
    def raw_phase(self) -> run_definition_pb2.Phase:
        """
        Get the raw phase of the action.
        """
        return self.pb2.status.phase

    @property
    def name(self) -> str:
        """
        Get the name of the action.
        """
        return self.action_id.name

    @property
    def run_name(self) -> str:
        """
        Get the name of the run.
        """
        return self.action_id.run.name

    @property
    def task_name(self) -> str | None:
        """
        Get the name of the task.
        """
        if self.pb2.metadata.HasField("task") and self.pb2.metadata.task.HasField("id"):
            return self.pb2.metadata.task.id.name
        return None

    @property
    def action_id(self) -> run_definition_pb2.ActionIdentifier:
        """
        Get the action ID.
        """
        return self.pb2.id

    async def show_logs(
        self,
        attempt: int | None = None,
        max_lines: int = 30,
        show_ts: bool = False,
        raw: bool = False,
        filter_system: bool = False,
    ):
        details = await self.details()
        if not details.is_running and not details.done():
            # TODO we can short circuit here if the attempt is not the last one and it is done!
            await self.wait(wait_for="logs-ready")
            details = await self.details()
        if not attempt:
            attempt = details.attempts
        return await Logs.create_viewer(
            action_id=self.action_id,
            attempt=attempt,
            max_lines=max_lines,
            show_ts=show_ts,
            raw=raw,
            filter_system=filter_system,
        )

    async def details(self) -> ActionDetails:
        """
        Get the details of the action. This is a placeholder for getting the action details.
        """
        if not self._details:
            self._details = await ActionDetails.get_details.aio(self.action_id)
        return cast(ActionDetails, self._details)

    async def watch(
        self, cache_data_on_done: bool = False, wait_for: WaitFor = "terminal"
    ) -> AsyncGenerator[ActionDetails, None]:
        """
        Watch the action for updates. This is a placeholder for watching the action.
        """
        ad = None
        async for ad in ActionDetails.watch.aio(self.action_id):
            if ad is None:
                return
            self._details = ad
            yield ad
            if wait_for == "running" and ad.is_running:
                break
            elif wait_for == "logs-ready" and ad.logs_available():
                break
            if ad.done():
                break
        if cache_data_on_done and ad and ad.done():
            await cast(ActionDetails, self._details).outputs()

    async def wait(self, quiet: bool = False, wait_for: WaitFor = "terminal") -> None:
        """
        Wait for the run to complete, displaying a rich progress panel with status transitions,
        time elapsed, and error details in case of failure.
        """
        console = Console()
        if self.done():
            if not quiet:
                if self.pb2.status.phase == run_definition_pb2.PHASE_SUCCEEDED:
                    console.print(
                        f"[bold green]Action '{self.name}' in Run '{self.run_name}'"
                        f" completed successfully.[/bold green]"
                    )
                else:
                    details = await self.details()
                    console.print(
                        f"[bold red]Action '{self.name}' in Run '{self.run_name}'"
                        f" exited unsuccessfully in state {self.phase} with error: {details.error_info}[/bold red]"
                    )
            return

        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
                transient=True,
                disable=quiet,
            ) as progress:
                task_id = progress.add_task(f"Waiting for run '{self.name}'...", start=False)
                progress.start_task(task_id)

                async for ad in self.watch(cache_data_on_done=True, wait_for=wait_for):
                    if ad is None:
                        progress.stop_task(task_id)
                        break

                    if ad.is_running and wait_for == "running":
                        progress.start_task(task_id)
                        break

                    if ad.logs_available() and wait_for == "logs-ready":
                        progress.start_task(task_id)
                        break

                    # Update progress description with the current phase
                    progress.update(
                        task_id,
                        description=f"Run: {self.run_name} in {ad.phase}, Runtime: {ad.runtime} secs "
                        f"Attempts[{ad.attempts}]",
                    )

                    # If the action is done, handle the final state
                    if ad.done():
                        progress.stop_task(task_id)
                        if ad.pb2.status.phase == run_definition_pb2.PHASE_SUCCEEDED:
                            console.print(f"[bold green]Run '{self.run_name}' completed successfully.[/bold green]")
                        else:
                            console.print(
                                f"[bold red]Run '{self.run_name}' exited unsuccessfully in state {ad.phase}"
                                f"with error: {ad.error_info}[/bold red]"
                            )
                        break
        except asyncio.CancelledError:
            # Handle cancellation gracefully
            pass
        except KeyboardInterrupt:
            # Handle keyboard interrupt gracefully
            pass

    def done(self) -> bool:
        """
        Check if the action is done.
        """
        return _action_done_check(self.raw_phase)

    async def sync(self) -> Action:
        """
        Sync the action with the remote server. This is a placeholder for syncing the action.
        """
        return self

    def __rich_repr__(self) -> rich.repr.Result:
        """
        Rich representation of the Action object.
        """
        yield from _action_rich_repr(self.pb2)
        if self._details:
            yield from self._details.__rich_repr__()

    def __repr__(self) -> str:
        """
        String representation of the Action object.
        """
        import rich.pretty

        return rich.pretty.pretty_repr(self)


@dataclass
class ActionDetails:
    """
    A class representing an action. It is used to manage the run of a task and its state on the remote Union API.
    """

    pb2: run_definition_pb2.ActionDetails
    _inputs: ActionInputs | None = None
    _outputs: ActionOutputs | None = None

    @syncify
    @classmethod
    async def get_details(cls, action_id: run_definition_pb2.ActionIdentifier) -> ActionDetails:
        """
        Get the details of the action. This is a placeholder for getting the action details.
        """
        ensure_client()
        resp = await get_client().run_service.GetActionDetails(
            run_service_pb2.GetActionDetailsRequest(
                action_id=action_id,
            )
        )
        return ActionDetails(resp.details)

    @syncify
    @classmethod
    async def get(
        cls, uri: str | None = None, /, run_name: str | None = None, name: str | None = None
    ) -> ActionDetails:
        """
        Get a run by its ID or name. If both are provided, the ID will take precedence.

        :param uri: The URI of the action.
        :param name: The name of the action.
        :param run_name: The name of the run.
        """
        ensure_client()
        if not uri:
            assert name is not None and run_name is not None, "Either uri or name and run_name must be provided"
        cfg = get_common_config()
        return await cls.get_details.aio(
            run_definition_pb2.ActionIdentifier(
                run=run_definition_pb2.RunIdentifier(
                    org=cfg.org,
                    project=cfg.project,
                    domain=cfg.domain,
                    name=run_name,
                ),
                name=name,
            ),
        )

    @syncify
    @classmethod
    async def watch(cls, action_id: run_definition_pb2.ActionIdentifier) -> AsyncIterator[ActionDetails]:
        """
        Watch the action for updates. This is a placeholder for watching the action.
        """
        ensure_client()
        if not action_id:
            raise ValueError("Action ID is required")

        call = cast(
            AsyncIterator[WatchActionDetailsResponse],
            get_client().run_service.WatchActionDetails(
                request=run_service_pb2.WatchActionDetailsRequest(
                    action_id=action_id,
                )
            ),
        )
        try:
            async for resp in call:
                v = cls(resp.details)
                yield v
                if v.done():
                    return
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.CANCELLED:
                pass
            else:
                raise e

    async def watch_updates(self, cache_data_on_done: bool = False) -> AsyncGenerator[ActionDetails, None]:
        async for d in self.watch.aio(action_id=self.pb2.id):
            yield d
            if d.done():
                self.pb2 = d.pb2
                break

        if cache_data_on_done and self.done():
            await self._cache_data.aio()

    @property
    def phase(self) -> str:
        """
        Get the phase of the action.
        """
        return run_definition_pb2.Phase.Name(self.status.phase)

    @property
    def raw_phase(self) -> run_definition_pb2.Phase:
        """
        Get the raw phase of the action.
        """
        return self.status.phase

    @property
    def is_running(self) -> bool:
        """
        Check if the action is currently running.
        """
        return self.status.phase == run_definition_pb2.PHASE_RUNNING

    @property
    def name(self) -> str:
        """
        Get the name of the action.
        """
        return self.action_id.name

    @property
    def run_name(self) -> str:
        """
        Get the name of the run.
        """
        return self.action_id.run.name

    @property
    def task_name(self) -> str | None:
        """
        Get the name of the task.
        """
        if self.pb2.metadata.HasField("task") and self.pb2.metadata.task.HasField("id"):
            return self.pb2.metadata.task.id.name
        return None

    @property
    def action_id(self) -> run_definition_pb2.ActionIdentifier:
        """
        Get the action ID.
        """
        return self.pb2.id

    @property
    def metadata(self) -> run_definition_pb2.ActionMetadata:
        return self.pb2.metadata

    @property
    def status(self) -> run_definition_pb2.ActionStatus:
        return self.pb2.status

    @property
    def error_info(self) -> run_definition_pb2.ErrorInfo | None:
        if self.pb2.HasField("error_info"):
            return self.pb2.error_info
        return None

    @property
    def abort_info(self) -> run_definition_pb2.AbortInfo | None:
        if self.pb2.HasField("abort_info"):
            return self.pb2.abort_info
        return None

    @property
    def runtime(self) -> timedelta:
        """
        Get the runtime of the action.
        """
        start_time = timestamp.to_datetime(self.pb2.status.start_time, timezone.utc)
        if self.pb2.status.HasField("end_time"):
            end_time = timestamp.to_datetime(self.pb2.status.end_time, timezone.utc)
            return end_time - start_time
        return datetime.now(timezone.utc) - start_time

    @property
    def attempts(self) -> int:
        """
        Get the number of attempts of the action.
        """
        return self.pb2.status.attempts

    def logs_available(self, attempt: int | None = None) -> bool:
        """
        Check if logs are available for the action, optionally for a specific attempt.
        If attempt is None, it checks for the latest attempt.
        """
        if attempt is None:
            attempt = self.pb2.status.attempts
        attempts = self.pb2.attempts
        if attempts and len(attempts) >= attempt:
            return attempts[attempt - 1].logs_available
        return False

    @syncify
    async def _cache_data(self) -> bool:
        """
        Cache the inputs and outputs of the action.
        :return: Returns True if Action is terminal and all data is cached else False.
        """
        if self._inputs and self._outputs:
            return True
        if self._inputs and not self.done():
            return False
        resp = await get_client().run_service.GetActionData(
            request=run_service_pb2.GetActionDataRequest(
                action_id=self.pb2.id,
            )
        )
        self._inputs = ActionInputs(resp.inputs)
        self._outputs = ActionOutputs(resp.outputs) if resp.HasField("outputs") else None
        return self._outputs is not None

    async def inputs(self) -> ActionInputs:
        """
        Placeholder for inputs. This can be extended to handle inputs from the run context.
        """
        if not self._inputs:
            await self._cache_data.aio()
        return cast(ActionInputs, self._inputs)

    async def outputs(self) -> ActionOutputs:
        """
        Placeholder for outputs. This can be extended to handle outputs from the run context.
        """
        if not self._outputs:
            if not await self._cache_data.aio():
                raise RuntimeError(
                    "Action is not in a terminal state, outputs are not available. "
                    "Please wait for the action to complete."
                )
        return cast(ActionOutputs, self._outputs)

    def done(self) -> bool:
        """
        Check if the action is in a terminal state (completed or failed). This is a placeholder for checking the
        action state.
        """
        return _action_done_check(self.raw_phase)

    def __rich_repr__(self) -> rich.repr.Result:
        """
        Rich representation of the Action object.
        """
        yield from _action_details_rich_repr(self.pb2)

    def __repr__(self) -> str:
        """
        String representation of the Action object.
        """
        import rich.pretty

        return rich.pretty.pretty_repr(self)


@dataclass
class ActionInputs:
    """
    A class representing the inputs of an action. It is used to manage the inputs of a task and its state on the
    remote Union API.
    """

    pb2: run_definition_pb2.Inputs

    def __repr__(self):
        import rich.pretty

        import flyte.types as types

        return rich.pretty.pretty_repr(types.literal_string_repr(self.pb2))


@dataclass
class ActionOutputs:
    """
    A class representing the outputs of an action. It is used to manage the outputs of a task and its state on the
    remote Union API.
    """

    pb2: run_definition_pb2.Outputs

    def __repr__(self):
        import rich.pretty

        import flyte.types as types

        return rich.pretty.pretty_repr(types.literal_string_repr(self.pb2))
