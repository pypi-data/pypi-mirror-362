import pandas as pd
import pyarrow as pa


def write_arrow_from_df(data: pd.DataFrame, arrow_file_path):
    table = pa.Table.from_pandas(data)
    writer = pa.RecordBatchStreamWriter(arrow_file_path, table.schema)
    writer.write(table)
    writer.close()
