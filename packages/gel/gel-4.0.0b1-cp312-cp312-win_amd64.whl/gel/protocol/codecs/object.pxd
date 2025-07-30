#
# This source file is part of the EdgeDB open source project.
#
# Copyright 2016-present MagicStack Inc. and the EdgeDB authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


@cython.final
cdef class ObjectCodec(BaseNamedRecordCodec):
    cdef:
        bint is_sparse
        object cached_dataclass_fields
        tuple names
        tuple flags
        tuple source_types

        dict cached_tid_map
        tuple cached_return_type_subcodecs
        tuple cached_return_type_dlists
        object cached_return_type_proxy
        object cached_return_type
        object cached_field_origins
        object cached_orig_return_type
        Py_ssize_t cached_tid_index

    cdef encode_args(self, WriteBuffer buf, dict obj)

    cdef adapt_to_return_type(self, object return_type)

    cdef _decode_plain(self, FRBuffer *buf, Py_ssize_t elem_count)

    @staticmethod
    cdef BaseCodec new(bytes tid, tuple names, tuple flags,
                       tuple cards, tuple codecs, tuple source_types,
                       bint is_sparse)


@cython.final
cdef class ObjectTypeNullCodec(BaseCodec):
    cdef:
        str name
        bint schema_defined

    @staticmethod
    cdef BaseCodec new(bytes tid, str name, bint schema_defined)


@cython.final
cdef class CompoundTypeNullCodec(BaseCodec):
    cdef:
        str name
        bint schema_defined
        int op
        tuple components

    @staticmethod
    cdef BaseCodec new(bytes tid, str name, bint schema_defined,
                       int op, tuple components)
