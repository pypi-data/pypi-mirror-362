from google.protobuf import timestamp_pb2 as _timestamp_pb2
from . import common_pb2 as _common_pb2
from . import uuid_pb2 as _uuid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LatestQuantumComputerCalibrationLookupV1(_message.Message):
    __slots__ = ("qc_id",)
    QC_ID_FIELD_NUMBER: _ClassVar[int]
    qc_id: _uuid_pb2.Uuid
    def __init__(self, qc_id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ...) -> None: ...

class CalibrationLookupV1(_message.Message):
    __slots__ = ("id", "tag")
    ID_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.Uuid
    tag: CalibrationTagLookupV1
    def __init__(self, id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ..., tag: _Optional[_Union[CalibrationTagLookupV1, _Mapping]] = ...) -> None: ...

class CalibrationTagLookupV1(_message.Message):
    __slots__ = ("qc_id", "tag")
    QC_ID_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    qc_id: _uuid_pb2.Uuid
    tag: str
    def __init__(self, qc_id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ..., tag: _Optional[str] = ...) -> None: ...

class CalibrationMetadataV1(_message.Message):
    __slots__ = ("id", "created_at", "dut_label", "is_valid", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DUT_LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: _uuid_pb2.Uuid
    created_at: _timestamp_pb2.Timestamp
    dut_label: str
    is_valid: bool
    metadata: bytes
    def __init__(self, id: _Optional[_Union[_uuid_pb2.Uuid, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., dut_label: _Optional[str] = ..., is_valid: bool = ..., metadata: _Optional[bytes] = ...) -> None: ...
