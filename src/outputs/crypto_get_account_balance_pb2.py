# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: crypto_get_account_balance.proto
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
    'crypto_get_account_balance.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import basic_types_pb2 as basic__types__pb2
from . import query_header_pb2 as query__header__pb2
from . import response_header_pb2 as response__header__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n crypto_get_account_balance.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x12query_header.proto\x1a\x15response_header.proto\"\xa3\x01\n\x1c\x43ryptoGetAccountBalanceQuery\x12\"\n\x06header\x18\x01 \x01(\x0b\x32\x12.proto.QueryHeader\x12%\n\taccountID\x18\x02 \x01(\x0b\x32\x10.proto.AccountIDH\x00\x12\'\n\ncontractID\x18\x03 \x01(\x0b\x32\x11.proto.ContractIDH\x00\x42\x0f\n\rbalanceSource\"\xae\x01\n\x1f\x43ryptoGetAccountBalanceResponse\x12%\n\x06header\x18\x01 \x01(\x0b\x32\x15.proto.ResponseHeader\x12#\n\taccountID\x18\x02 \x01(\x0b\x32\x10.proto.AccountID\x12\x0f\n\x07\x62\x61lance\x18\x03 \x01(\x04\x12.\n\rtokenBalances\x18\x04 \x03(\x0b\x32\x13.proto.TokenBalanceB\x02\x18\x01\x42&\n\"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'crypto_get_account_balance_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.hederahashgraph.api.proto.javaP\001'
  _globals['_CRYPTOGETACCOUNTBALANCERESPONSE'].fields_by_name['tokenBalances']._loaded_options = None
  _globals['_CRYPTOGETACCOUNTBALANCERESPONSE'].fields_by_name['tokenBalances']._serialized_options = b'\030\001'
  _globals['_CRYPTOGETACCOUNTBALANCEQUERY']._serialized_start=106
  _globals['_CRYPTOGETACCOUNTBALANCEQUERY']._serialized_end=269
  _globals['_CRYPTOGETACCOUNTBALANCERESPONSE']._serialized_start=272
  _globals['_CRYPTOGETACCOUNTBALANCERESPONSE']._serialized_end=446
# @@protoc_insertion_point(module_scope)
