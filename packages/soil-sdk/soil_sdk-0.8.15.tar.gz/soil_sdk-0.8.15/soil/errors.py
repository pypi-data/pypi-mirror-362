"""Exceptions for SOIL-SDK"""


class SoilSDKError(Exception):
    """Common soil-sdk exception"""


class InternalSoilError(SoilSDKError):
    """Generic soil-sdk error"""


class LoginError(SoilSDKError):
    """Exception to raise when unable to login Soil"""


class ExperimentError(SoilSDKError):
    """Exception to raise when an error has occurred while executing a Soil experiment"""


class ExperimentTimeoutError(SoilSDKError):
    """Exception to raise when a Soil experiment times out"""


class ObjectNotFound(SoilSDKError):
    """Exception to raise when Soil object could not be found"""


class DictionaryNotFound(ObjectNotFound):
    """Exception to raise when Soil Dictionary could not be found"""


class GraphStateNotFound(ObjectNotFound):
    """Exception to raise when Soil Graph State could not be found"""


class DataNotFound(ObjectNotFound):
    """Exception to raise when Soil data could not be found"""


class JobCollectionNotFound(ObjectNotFound):
    """Exception to raise when Soil job collection could not be found"""


class ModuleNotFound(ObjectNotFound):
    """Exception to raise when Soil module could not be found"""


class ObjectNotUploaded(SoilSDKError):
    """Exception to raise when Soil object could not be uploaded"""


class GraphStateNotSaved(ObjectNotUploaded):
    """Exception to raise when Soil Graph State could not be saved"""


class DictionaryNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil Dictionary could not be uploaded"""


class DataNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil data could not be uploaded"""


class ModuleNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil Module could not be uploaded"""


class AlertDataNotUploaded(ObjectNotUploaded):
    """Exception to raise when Soil alert could not be uploaded"""


class AlertNotUploaded(AlertDataNotUploaded):
    """Exception to raise when Soil alert condition could not be uploaded"""


class EventNotUploaded(AlertDataNotUploaded):
    """Exception to raise when Soil event alert could not be uploaded"""


class DataStructureError(SoilSDKError):
    """Exception to raise when Soil DataStructure has any error"""


class DataStructureType(DataStructureError):
    """Exception to raise when Soil DataStructure type is not recognised"""


class DataStructurePipelineNotFound(DataStructureError):
    """Exception to raise when Soil DataStructure Pipeline is not found"""


class PipelineContextNotSaved(DataStructureError):
    """Exception to raise when Soil Pipeline is not found"""


class ProjectContextNotFound(DataStructureError):
    """Exception to raise when Soil Project Context is not found"""


class GraphLogNotCreated(SoilSDKError):
    """Exception to raise when Soil Graph Log could not be created"""
