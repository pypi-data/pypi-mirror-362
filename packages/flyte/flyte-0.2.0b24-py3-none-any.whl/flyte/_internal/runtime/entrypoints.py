from typing import List, Optional, Tuple

import flyte.errors
from flyte._code_bundle import download_bundle
from flyte._context import contextual_run
from flyte._internal import Controller
from flyte._internal.imagebuild.image_builder import ImageCache
from flyte._logging import log, logger
from flyte._task import TaskTemplate
from flyte.models import ActionID, Checkpoints, CodeBundle, RawDataPath

from .convert import Error, Inputs, Outputs
from .task_serde import load_task
from .taskrunner import (
    convert_and_run,
    extract_download_run_upload,
)


async def direct_dispatch(
    task: TaskTemplate,
    *,
    action: ActionID,
    raw_data_path: RawDataPath,
    controller: Controller,
    version: str,
    output_path: str,
    run_base_dir: str,
    checkpoints: Checkpoints | None = None,
    code_bundle: CodeBundle | None = None,
    inputs: Inputs | None = None,
) -> Tuple[Optional[Outputs], Optional[Error]]:
    """
    This method is used today by the local_controller and is positioned to be used by a rust core in the future.
    The caller, loads the task and invokes this method. This method is used to convert the inputs to native types,
    The reason for this is that the rust entrypoint will not have access to the python context, and
    will not be able to run the tasks in the context tree.
    """
    return await contextual_run(
        convert_and_run,
        task=task,
        inputs=inputs or Inputs.empty(),
        action=action,
        raw_data_path=raw_data_path,
        checkpoints=checkpoints,
        code_bundle=code_bundle,
        controller=controller,
        version=version,
        output_path=output_path,
        run_base_dir=run_base_dir,
    )


async def _download_and_load_task(
    code_bundle: CodeBundle | None, resolver: str | None = None, resolver_args: List[str] | None = None
) -> TaskTemplate:
    if code_bundle and (code_bundle.tgz or code_bundle.pkl):
        logger.debug(f"Downloading {code_bundle}")
        downloaded_path = await download_bundle(code_bundle)
        code_bundle = code_bundle.with_downloaded_path(downloaded_path)
        if code_bundle.pkl:
            try:
                logger.debug(f"Loading task from pkl: {code_bundle.downloaded_path}")
                import gzip

                import cloudpickle

                with gzip.open(str(code_bundle.downloaded_path), "rb") as f:
                    return cloudpickle.load(f)
            except Exception as e:
                logger.exception(f"Failed to load pickled task from {code_bundle.downloaded_path}. Reason: {e!s}")
                raise

        if not resolver or not resolver_args:
            raise flyte.errors.RuntimeSystemError(
                "MalformedCommand", "Resolver and resolver args are required. for task"
            )
        logger.debug(
            f"Loading task from tgz: {code_bundle.downloaded_path}, resolver: {resolver}, args: {resolver_args}"
        )
        return load_task(resolver, *resolver_args)
    if not resolver or not resolver_args:
        raise flyte.errors.RuntimeSystemError("MalformedCommand", "Resolver and resolver args are required. for task")
    logger.debug(f"No code bundle provided, loading task from resolver: {resolver}, args: {resolver_args}")
    return load_task(resolver, *resolver_args)


@log
async def load_and_run_task(
    action: ActionID,
    raw_data_path: RawDataPath,
    output_path: str,
    run_base_dir: str,
    version: str,
    controller: Controller,
    resolver: str,
    resolver_args: List[str],
    checkpoints: Checkpoints | None = None,
    code_bundle: CodeBundle | None = None,
    input_path: str | None = None,
    image_cache: ImageCache | None = None,
):
    """
    This method is invoked from the runtime/CLI and is used to run a task. This creates the context tree,
    for the tasks to run in. It also handles the loading of the task.

    :param controller: Controller to use for the task.
    :param resolver: The resolver to use to load the task.
    :param resolver_args: The arguments to pass to the resolver.
    :param action: The ActionID to use for the task.
    :param raw_data_path: The raw data path to use for the task.
    :param output_path: The output path to use for the task.
    :param run_base_dir: Base output directory to pass down to child tasks.
    :param version: The version of the task to run.
    :param checkpoints: The checkpoints to use for the task.
    :param code_bundle: The code bundle to use for the task.
    :param input_path: The input path to use for the task.
    :param image_cache: Mappings of Image identifiers to image URIs.
    """
    task = await _download_and_load_task(code_bundle, resolver, resolver_args)

    await contextual_run(
        extract_download_run_upload,
        task,
        action=action,
        version=version,
        controller=controller,
        raw_data_path=raw_data_path,
        output_path=output_path,
        run_base_dir=run_base_dir,
        checkpoints=checkpoints,
        code_bundle=code_bundle,
        input_path=input_path,
        image_cache=image_cache,
    )
