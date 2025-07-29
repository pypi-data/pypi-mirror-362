from prometheus_client import Counter, generate_latest

from .config import MetricListConfig


class Metrics:
    def __init__(self, metrics_config: MetricListConfig | None = None):
        self.metrics: dict[str, Counter | dict[str, Counter]] | None = None
        self.labels: dict[str, dict[str, any]] | None = None

        if metrics_config:
            self.init_metrics(metrics_config)

    @staticmethod
    def _get_label_names(**labels):
        return ('type', 'process') + tuple(list(labels.keys()))

    @staticmethod
    def _get_label_type_process(process):
        type_, process_ = process.split('.')
        return {'type': type_, 'process': process_}

    def _get_labels(self, name, process):
        try:
            l = self.labels.get(name).get(process)
            l.update(self._get_label_type_process(process))
            return l
        except AttributeError:
            return None

    def add_metric(self, name, documentation: str | None = None, labels: dict[str, dict[str, any]] | None = None):
        """
        Add metric to processing
        :param name: Metrics name
        :param documentation: Description of metric
        :param labels: Additional arguments. E.g. {'service.run': {'trigger_count': 0, 'trigger_time': '0m'}}
        :return: None
        """
        documentation = documentation or ""
        if not self.metrics:
            self.metrics = {}
        if not self.labels:
            self.labels = {}

        if labels:
            labelnames = self._get_label_names(**(list(labels.values())[0]))

            counter = Counter(name, documentation, labelnames=labelnames)
            self.metrics.update({name: counter})
            self.labels.update({name: labels})

            for process in labels.keys():
                self.increment_metric(name, 0.0, process=process)  # init metrics with 0 value
        else:
            self.metrics[name] = Counter(name, documentation, labelnames=())
            self.increment_metric(name, 0.0)  # init metric with 0 value

    def get_metric(self, name) -> Counter | None:
        """
        Get metric by name
        :param name: Metric name
        :return: Counter | None
        """
        try:
            return self.metrics.get(name)
        except AttributeError:
            return None

    def increment_metric(self, name, value: float | None = None, process: str | None=None):
        """
        Increment metric by name for value
        :param name: Metric name
        :param value: Increment value. 1.0 by default if None
        :param process: Process name if you use labels
        :return: None
        """
        value = value if value is not None else 1.0
        metric = self.get_metric(name)
        assert metric, f"Metric {name} not set. Add it by calling {self.__class__.__name__}.add_metric('{name}', 'Description')"

        labels_ = self._get_labels(name, process)
        assert labels_ and process or not labels_, "Add process name for increment for this metric"
        label = metric.labels(**labels_) if labels_ else None
        label.inc(value) if label else metric.inc(value)

    @staticmethod
    def collect_metrics():
        return generate_latest().decode()

    def init_metrics(self, metrics_conf: MetricListConfig):
        for metric in metrics_conf.root:
            self.add_metric(**metric.model_dump())
