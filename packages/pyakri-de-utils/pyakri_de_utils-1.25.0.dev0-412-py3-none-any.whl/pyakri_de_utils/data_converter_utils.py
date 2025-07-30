# Content of this file is borrowed from data-converters package
import os
import re
from typing import List

import pandas as pd
import pyarrow as pa
from pyakri_de_utils import logger


class Field(object):
    def __init__(self, name, field_type):
        self._name = name
        self._type = field_type

    def name(self):
        return self._name

    def type(self):
        return self._type


class Schema(object):
    def __init__(self, fields: List[Field], d_type):
        self.dtype = d_type
        self._field_list = fields

    def fields(self):
        return self._field_list


class DataConverters(object):
    @classmethod
    def __create_arrow_schema(cls, schema):
        field_list = []
        for field in schema.fields():
            ftype, _ = cls.__split_field_type(field.type(), -1)
            field_list.append(pa.field(field.name(), ftype))
        return pa.schema(field_list)

    @classmethod
    def __split_field_type(cls, ftype, nrows):
        p = re.compile(r"(\w+)(\[.*\])")
        m = p.match(ftype)
        match_groups = m.groups()
        field_type = match_groups[0]

        dim_list = [nrows]
        if len(match_groups) > 1:
            dp = re.compile("\[(\d*)\]")
            dlist = dp.findall(match_groups[1])
            if not dlist[0]:
                dlist[0] = -1
            dim_list.extend([int(_) for _ in dlist])

        return field_type, dim_list

    @classmethod
    def numpy_to_arrow(cls, data, schema: Schema):
        logger.info("Received Output Shape {}".format(data.shape))
        schema_info = cls.__create_arrow_schema(schema)
        if data.ndim == 1:
            arr = pa.array(data)
            return pa.Table.from_arrays([arr], schema_info.names)
        else:
            # Handles multi-dim cases by reducing them to 2D
            # Because Arrow doesn't support Tensors as col-types
            if data.shape[0] != 0:
                data = data.reshape(data.shape[0], -1)
            obj = pd.DataFrame([[_] for _ in data])
            obj.rename(columns={0: schema_info.names[0]}, inplace=True)
            return pa.Table.from_pandas(obj)

    @classmethod
    def arrow_to_arrow_file(cls, base_path, file_path, arrow_obj: pa.Table):
        with open(os.path.join(base_path, file_path), "wb") as arrow_file:
            writer = pa.RecordBatchStreamWriter(arrow_file, arrow_obj.schema)
            writer.write_table(arrow_obj)
            writer.close()
