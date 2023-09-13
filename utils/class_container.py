from enum import Enum, auto

from utils.clone_service import CloneService
from utils.code_metric_analyser_service import CodeMetricAnalyserService


class ClassContainer:
    class Classes(Enum):
        CLONE_SERVICE = auto()
        CODE_METRIC_ANALYSER_SERVICE = auto()

    __instances: dict[Classes, any] = {}

    def get_clone_service(self):
        service: CloneService = self.__instances.get(self.Classes.CLONE_SERVICE)
        if not service:
            service = CloneService()
            self.__instances[self.Classes.CLONE_SERVICE] = service
        return service

    def get_code_analysis_service(self):
        service: CodeMetricAnalyserService = self.__instances.get(self.Classes.CODE_METRIC_ANALYSER_SERVICE)
        if not service:
            service = CodeMetricAnalyserService()
            self.__instances[self.Classes.CODE_METRIC_ANALYSER_SERVICE] = service
        return service
