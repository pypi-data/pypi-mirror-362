import logging
import traceback
from enum import Enum


logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    NONE = logging.NOTSET


class GeneralException(Exception):
    def __init__(self, msn: str, severity_level: SeverityLevel):
        """
        General Exception class for the project.
        It deals with the severity level, and the logging of the exception.
        """
        # TODO - Add a data validator like pydantic to validate it.
        if not isinstance(severity_level, SeverityLevel):
            raise TypeError(f"severity_level must be an instance of SeverityLevel, not {type(severity_level)}")
        super().__init__(msn)
        self.msn = msn
        self.severity_level = severity_level

    def log(self, with_traceback=False):
        logger.log(self.severity_level.value, self.msn)
        if with_traceback:
            traceback_string = traceback.format_exc()
            logger.log(self.severity_level.value, traceback_string)


class ParameterError(GeneralException):
    """
    Raised whenever the parameter data is not valid.
    """

    def __init__(self, msn: str):
        super().__init__(msn, SeverityLevel.ERROR)


class InputDataError(GeneralException):
    """
    Raised whenever the input data is not valid.
    """

    def __init__(self, msn: str):
        super().__init__(msn, SeverityLevel.ERROR)


class SolutionError(GeneralException):
    """
    Raised when the output from the optimization or the output tables contain some problem.

    For example, if the solution is not feasible, or if the output from the optimization violates an expected
    constraint.
    """

    def __init__(self, msn: str):
        super().__init__(msn, SeverityLevel.ERROR)
