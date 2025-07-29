import os


def ipython_check() -> bool:
    """
    Check if interface is launching from iPython (not colab)
    :return is_ipython (bool): True or False
    """
    is_ipython = False
    try:  # Check if running interactively using ipython.
        from IPython import get_ipython

        if get_ipython() is not None:
            is_ipython = True
    except (ImportError, NameError):
        pass
    return is_ipython


def is_in_cluster() -> bool:
    """
    Check if the task is running in a cluster
    :return is_in_cluster (bool): True or False
    """
    if os.getenv("_UN_CLS"):
        return True
    return False
