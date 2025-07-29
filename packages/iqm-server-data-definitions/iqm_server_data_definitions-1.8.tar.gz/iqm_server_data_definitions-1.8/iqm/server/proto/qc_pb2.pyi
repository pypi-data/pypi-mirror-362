from . import common_pb2 as _common_pb2
from . import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuantumComputerLookupV1(_message.Message):
    __slots__ = ("id", "alias")
    ID_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.Uuid
    alias: str
    def __init__(self, id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ..., alias: _Optional[str] = ...) -> None: ...

class ListQuantumComputerFiltersV1(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QuantumComputerV1(_message.Message):
    __slots__ = ("id", "alias", "display_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.Uuid
    alias: str
    display_name: str
    def __init__(self, id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ..., alias: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class QuantumComputersListV1(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[QuantumComputerV1]
    def __init__(self, items: _Optional[_Iterable[_Union[QuantumComputerV1, _Mapping]]] = ...) -> None: ...

class QuantumComputerResourceLookupV1(_message.Message):
    __slots__ = ("qc_id", "resource_name")
    QC_ID_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    qc_id: _uuid_pb2.Uuid
    resource_name: str
    def __init__(self, qc_id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ..., resource_name: _Optional[str] = ...) -> None: ...
