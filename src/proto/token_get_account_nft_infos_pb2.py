# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: token_get_account_nft_infos.proto
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
    'token_get_account_nft_infos.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import basic_types_pb2 as basic__types__pb2
from . import token_get_nft_info_pb2 as token__get__nft__info__pb2
from . import query_header_pb2 as query__header__pb2
from . import response_header_pb2 as response__header__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!token_get_account_nft_infos.proto\x12\x05proto\x1a\x11\x62\x61sic_types.proto\x1a\x18token_get_nft_info.proto\x1a\x12query_header.proto\x1a\x15response_header.proto\"\x83\x01\n\x1cTokenGetAccountNftInfosQuery\x12\"\n\x06header\x18\x01 \x01(\x0b\x32\x12.proto.QueryHeader\x12#\n\taccountID\x18\x02 \x01(\x0b\x32\x10.proto.AccountID\x12\r\n\x05start\x18\x03 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x04 \x01(\x03\"k\n\x1fTokenGetAccountNftInfosResponse\x12%\n\x06header\x18\x01 \x01(\x0b\x32\x15.proto.ResponseHeader\x12!\n\x04nfts\x18\x02 \x03(\x0b\x32\x13.proto.TokenNftInfoB&\n\"com.hederahashgraph.api.proto.javaP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'token_get_account_nft_infos_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"com.hederahashgraph.api.proto.javaP\001'
  _globals['_TOKENGETACCOUNTNFTINFOSQUERY']._serialized_start=133
  _globals['_TOKENGETACCOUNTNFTINFOSQUERY']._serialized_end=264
  _globals['_TOKENGETACCOUNTNFTINFOSRESPONSE']._serialized_start=266
  _globals['_TOKENGETACCOUNTNFTINFOSRESPONSE']._serialized_end=373
# @@protoc_insertion_point(module_scope)
