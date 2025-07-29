from openobd_protocol.Configuration.Messages import CanBus_pb2 as _CanBus_pb2
from openobd_protocol.Configuration.Messages import KlineBus_pb2 as _KlineBus_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EcuList(_message.Message):
    __slots__ = ("ecus",)
    ECUS_FIELD_NUMBER: _ClassVar[int]
    ecus: _containers.RepeatedCompositeFieldContainer[Ecu]
    def __init__(self, ecus: _Optional[_Iterable[_Union[Ecu, _Mapping]]] = ...) -> None: ...

class Ecu(_message.Message):
    __slots__ = ("isotp_ecu", "kline_ecu")
    ISOTP_ECU_FIELD_NUMBER: _ClassVar[int]
    KLINE_ECU_FIELD_NUMBER: _ClassVar[int]
    isotp_ecu: IsotpEcu
    kline_ecu: KlineEcu
    def __init__(self, isotp_ecu: _Optional[_Union[IsotpEcu, _Mapping]] = ..., kline_ecu: _Optional[_Union[KlineEcu, _Mapping]] = ...) -> None: ...

class IsotpEcu(_message.Message):
    __slots__ = ("can_bus", "request_id", "response_id", "extended_request_address", "extended_response_address")
    CAN_BUS_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_REQUEST_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_RESPONSE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    can_bus: _CanBus_pb2.CanBus
    request_id: int
    response_id: int
    extended_request_address: int
    extended_response_address: int
    def __init__(self, can_bus: _Optional[_Union[_CanBus_pb2.CanBus, _Mapping]] = ..., request_id: _Optional[int] = ..., response_id: _Optional[int] = ..., extended_request_address: _Optional[int] = ..., extended_response_address: _Optional[int] = ...) -> None: ...

class KlineEcu(_message.Message):
    __slots__ = ("kline_bus", "ecu_id")
    KLINE_BUS_FIELD_NUMBER: _ClassVar[int]
    ECU_ID_FIELD_NUMBER: _ClassVar[int]
    kline_bus: _KlineBus_pb2.KlineBus
    ecu_id: int
    def __init__(self, kline_bus: _Optional[_Union[_KlineBus_pb2.KlineBus, _Mapping]] = ..., ecu_id: _Optional[int] = ...) -> None: ...
