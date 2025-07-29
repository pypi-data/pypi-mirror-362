from dataclasses import dataclass
from datetime import timedelta
from typing import Optional, Tuple, Union


@dataclass
class ReusePolicy:
    """
    ReusePolicy can be used to configure a task to reuse the environment. This is useful when the environment creation
    is expensive and the runtime of the task is short. The environment will be reused for the next invocation of the
    task, even the python process maybe be reused by subsequent task invocations. A good mental model is to think of
    the environment as a container that is reused for multiple tasks, more like a long-running service.

    Caution: It is important to note that the environment is shared, so managing memory and resources is important.

    :param replicas: Either a single int representing number of replicas or a tuple of two ints representing
     the min and max
    :param idle_ttl: The maximum idle duration for an environment replica, specified as either seconds (int) or a
        timedelta. If not set, the environment's global default will be used.
        When a replica remains idle — meaning no tasks are running — for this duration, it will be automatically
        terminated.
    """

    replicas: Union[int, Tuple[int, int]] = 1
    idle_ttl: Optional[Union[int, timedelta]] = None
