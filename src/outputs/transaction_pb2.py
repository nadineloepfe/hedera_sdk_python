# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: transaction.proto
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
    'transaction.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import basic_types_pb2 as basic__types__pb2
from . import transaction_body_pb2 as transaction__body__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11transaction.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x16transaction_body.proto\"\xbf\x01\n\x0bTransaction\x12(\n\x04\x62ody\x18\x01 \x01(\x0b\x32\x16.proto.TransactionBodyB\x02\x18\x01\x12&\n\x04sigs\x18\x02 \x01(\x0b\x32\x14.proto.SignatureListB\x02\x18\x01\x12\'\n\x06sigMap\x18\x03 \x01(\x0b\x32\x13.proto.SignatureMapB\x02\x18\x01\x12\x15\n\tbodyBytes\x18\x04 \x01(\x0c\x42\x02\x18\x01\x12\x1e\n\x16signedTransactionBytes\x18\x05 \x01(\x0c\x42&\n\"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.hederahashgraph.api.proto.javaP\001'
  _globals['_TRANSACTION'].fields_by_name['body']._loaded_options = None
  _globals['_TRANSACTION'].fields_by_name['body']._serialized_options = b'\030\001'
  _globals['_TRANSACTION'].fields_by_name['sigs']._loaded_options = None
  _globals['_TRANSACTION'].fields_by_name['sigs']._serialized_options = b'\030\001'
  _globals['_TRANSACTION'].fields_by_name['sigMap']._loaded_options = None
  _globals['_TRANSACTION'].fields_by_name['sigMap']._serialized_options = b'\030\001'
  _globals['_TRANSACTION'].fields_by_name['bodyBytes']._loaded_options = None
  _globals['_TRANSACTION'].fields_by_name['bodyBytes']._serialized_options = b'\030\001'
  _globals['_TRANSACTION']._serialized_start=72
  _globals['_TRANSACTION']._serialized_end=263
# @@protoc_insertion_point(module_scope)
