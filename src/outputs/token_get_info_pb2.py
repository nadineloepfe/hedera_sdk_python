# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: token_get_info.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'token_get_info.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import basic_types_pb2 as basic__types__pb2
from . import custom_fees_pb2 as custom__fees__pb2
from . import query_header_pb2 as query__header__pb2
from . import response_header_pb2 as response__header__pb2
from . import timestamp_pb2 as timestamp__pb2
from . import duration_pb2 as duration__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14token_get_info.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x11\x63ustom_fees.proto\x1a\x12query_header.proto\x1a\x15response_header.proto\x1a\x0ftimestamp.proto\x1a\x0e\x64uration.proto\"V\n\x11TokenGetInfoQuery\x12\"\n\x06header\x18\x01 \x01(\x0b\x32\x12.proto.QueryHeader\x12\x1d\n\x05token\x18\x02 \x01(\x0b\x32\x0e.proto.TokenID\"\xef\x06\n\tTokenInfo\x12\x1f\n\x07tokenId\x18\x01 \x01(\x0b\x32\x0e.proto.TokenID\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06symbol\x18\x03 \x01(\t\x12\x10\n\x08\x64\x65\x63imals\x18\x04 \x01(\r\x12\x13\n\x0btotalSupply\x18\x05 \x01(\x04\x12\"\n\x08treasury\x18\x06 \x01(\x0b\x32\x10.proto.AccountID\x12\x1c\n\x08\x61\x64minKey\x18\x07 \x01(\x0b\x32\n.proto.Key\x12\x1a\n\x06kycKey\x18\x08 \x01(\x0b\x32\n.proto.Key\x12\x1d\n\tfreezeKey\x18\t \x01(\x0b\x32\n.proto.Key\x12\x1b\n\x07wipeKey\x18\n \x01(\x0b\x32\n.proto.Key\x12\x1d\n\tsupplyKey\x18\x0b \x01(\x0b\x32\n.proto.Key\x12\x35\n\x13\x64\x65\x66\x61ultFreezeStatus\x18\x0c \x01(\x0e\x32\x18.proto.TokenFreezeStatus\x12/\n\x10\x64\x65\x66\x61ultKycStatus\x18\r \x01(\x0e\x32\x15.proto.TokenKycStatus\x12\x0f\n\x07\x64\x65leted\x18\x0e \x01(\x08\x12*\n\x10\x61utoRenewAccount\x18\x0f \x01(\x0b\x32\x10.proto.AccountID\x12(\n\x0f\x61utoRenewPeriod\x18\x10 \x01(\x0b\x32\x0f.proto.Duration\x12 \n\x06\x65xpiry\x18\x11 \x01(\x0b\x32\x10.proto.Timestamp\x12\x0c\n\x04memo\x18\x12 \x01(\t\x12#\n\ttokenType\x18\x13 \x01(\x0e\x32\x10.proto.TokenType\x12*\n\nsupplyType\x18\x14 \x01(\x0e\x32\x16.proto.TokenSupplyType\x12\x11\n\tmaxSupply\x18\x15 \x01(\x03\x12$\n\x10\x66\x65\x65_schedule_key\x18\x16 \x01(\x0b\x32\n.proto.Key\x12%\n\x0b\x63ustom_fees\x18\x17 \x03(\x0b\x32\x10.proto.CustomFee\x12\x1d\n\tpause_key\x18\x18 \x01(\x0b\x32\n.proto.Key\x12-\n\x0cpause_status\x18\x19 \x01(\x0e\x32\x17.proto.TokenPauseStatus\x12\x11\n\tledger_id\x18\x1a \x01(\x0c\x12\x10\n\x08metadata\x18\x1b \x01(\x0c\x12 \n\x0cmetadata_key\x18\x1c \x01(\x0b\x32\n.proto.Key\"b\n\x14TokenGetInfoResponse\x12%\n\x06header\x18\x01 \x01(\x0b\x32\x15.proto.ResponseHeader\x12#\n\ttokenInfo\x18\x02 \x01(\x0b\x32\x10.proto.TokenInfoB&\n\"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'token_get_info_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.hederahashgraph.api.proto.javaP\001'
  _globals['_TOKENGETINFOQUERY']._serialized_start=145
  _globals['_TOKENGETINFOQUERY']._serialized_end=231
  _globals['_TOKENINFO']._serialized_start=234
  _globals['_TOKENINFO']._serialized_end=1113
  _globals['_TOKENGETINFORESPONSE']._serialized_start=1115
  _globals['_TOKENGETINFORESPONSE']._serialized_end=1213
# @@protoc_insertion_point(module_scope)
