import datetime

import polars as pl

POLARS_TO_PYTHON = {
    pl.Int8: int,
    pl.Int16: int,
    pl.Int32: int,
    pl.Int64: int,
    pl.UInt8: int,
    pl.UInt16: int,
    pl.UInt32: int,
    pl.UInt64: int,
    pl.Float32: float,
    pl.Float64: float,
    pl.Boolean: bool,
    pl.Utf8: str,
    pl.String: str,
    pl.Categorical: str,
    pl.Date: datetime.date,
    pl.Datetime: datetime.datetime,
    pl.Time: datetime.time,
    pl.Duration: datetime.timedelta,
    pl.Object: object,
    pl.List: list,
    pl.Struct: dict,
    pl.Null: type(None),
}
