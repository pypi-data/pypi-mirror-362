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


cdef class BaseArrayCodec(BaseCodec):

    cdef:
        BaseCodec sub_codec
        int32_t cardinality

        object cached_return_type
        object cached_element_type
        object cached_dlist_type

    cdef _decode_array(
        self, bint is_set, object return_type, FRBuffer *buf,
        bint array_mode)

    cdef adapt_to_return_type(self, object return_type)


@cython.final
cdef class ArrayCodec(BaseArrayCodec):

    @staticmethod
    cdef BaseCodec new(bytes tid, BaseCodec sub_codec, int32_t cardinality)
