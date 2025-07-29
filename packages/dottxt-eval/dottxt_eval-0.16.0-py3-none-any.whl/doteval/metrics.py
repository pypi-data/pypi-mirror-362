from typing import Any, Callable, List

Metric = Callable[[List[bool]], float]


def metric(metric_func) -> Callable[..., Metric]:
    """Decorator for metrics.

    Parameters
    ----------
    metric_func : Metrics
        Function whose name will be used when attaching to evalutor.
        The function should return another function that takes a list[bool] and returns a float.
    """

    def create_metric_wrapper(metric_func, name):
        def metric_wrapper(*args: Any, **kwargs: Any):
            metric = metric_func(*args, **kwargs)
            metric.__name__ = name
            return metric

        return metric_wrapper

    metric_name = getattr(metric_func, "__name__")
    wrapper = create_metric_wrapper(metric_func, metric_name)
    wrapper.__name__ = metric_name

    return wrapper


@metric
def accuracy() -> Metric:
    """Metric for accuracy. Takes a list of boolean values and returns the percentage of the list that are True.

    Returns
    -------
    Metrics
    """

    def metric(scores: list[bool]) -> float:
        if len(scores) == 0:
            return 0
        total = 0.0
        for score in scores:
            total += float(score)
        return total / float(len(scores))

    return metric


registry = {"accuracy": accuracy()}
