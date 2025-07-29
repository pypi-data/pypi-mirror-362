from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModuleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNNING: _ClassVar[ModuleStatus]
    IDLE: _ClassVar[ModuleStatus]
    ENDED: _ClassVar[ModuleStatus]
RUNNING: ModuleStatus
IDLE: ModuleStatus
ENDED: ModuleStatus

class ModuleStatusRequest(_message.Message):
    __slots__ = ("module_id",)
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    def __init__(self, module_id: _Optional[str] = ...) -> None: ...

class ModuleStatusResponse(_message.Message):
    __slots__ = ("module_id", "status", "message")
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    status: ModuleStatus
    message: str
    def __init__(self, module_id: _Optional[str] = ..., status: _Optional[_Union[ModuleStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class GetAllModulesStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListModulesStatusRequest(_message.Message):
    __slots__ = ("list_size", "offset")
    LIST_SIZE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    list_size: int
    offset: int
    def __init__(self, list_size: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class ListModulesStatusResponse(_message.Message):
    __slots__ = ("list_size", "modules_statuses")
    LIST_SIZE_FIELD_NUMBER: _ClassVar[int]
    MODULES_STATUSES_FIELD_NUMBER: _ClassVar[int]
    list_size: int
    modules_statuses: _containers.RepeatedCompositeFieldContainer[ModuleStatusResponse]
    def __init__(self, list_size: _Optional[int] = ..., modules_statuses: _Optional[_Iterable[_Union[ModuleStatusResponse, _Mapping]]] = ...) -> None: ...

class UpdateStatusRequest(_message.Message):
    __slots__ = ("module_id", "status")
    MODULE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    module_id: str
    status: ModuleStatus
    def __init__(self, module_id: _Optional[str] = ..., status: _Optional[_Union[ModuleStatus, str]] = ...) -> None: ...

class UpdateStatusResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
