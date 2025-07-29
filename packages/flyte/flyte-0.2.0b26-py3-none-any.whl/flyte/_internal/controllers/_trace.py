from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Optional

from flyte.models import ActionID, NativeInterface


@dataclass
class TraceInfo:
    """
    Trace information for the action. This is used to record the trace of the action and should be called when
     the action is completed.
    """

    action: ActionID
    interface: NativeInterface
    inputs_path: str
    duration: Optional[timedelta] = None
    output: Optional[Any] = None
    error: Optional[Exception] = None
    name: str = ""

    def add_outputs(self, output: Any, duration: timedelta):
        """
        Add outputs to the trace information.
        :param output: Output of the action
        :param duration: Duration of the action
        :return:
        """
        self.output = output
        self.duration = duration

    def add_error(self, error: Exception, duration: timedelta):
        """
        Add error to the trace information.
        :param error: Error of the action
        :param duration: Duration of the action
        :return:
        """
        self.error = error
        self.duration = duration
