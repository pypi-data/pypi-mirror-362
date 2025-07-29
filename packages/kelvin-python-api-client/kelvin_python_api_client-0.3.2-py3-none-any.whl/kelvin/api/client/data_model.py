"""
Data Model.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Generic, Iterator, List, Mapping, Sequence, TypeVar, Union

import structlog
from pydantic.v1 import Extra, ValidationError, validator
from pydantic.v1.fields import ModelField

from .base_model import BaseModel
from .utils import parse_resource

if TYPE_CHECKING:
    import pandas as pd


logger = structlog.get_logger(__name__)

T = TypeVar("T")


class DataModel(BaseModel):
    """Model base-class."""

    if TYPE_CHECKING:
        fields: Any
        schema: Any

    class Config(BaseModel.Config):
        """Model config."""

        extra = Extra.allow

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    def __getattribute__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            result = super().__getattribute__(name)
        except AttributeError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        return getattr(head, tail)
                    except AttributeError:
                        pass
            raise

        return KList(result) if isinstance(result, list) else result

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute."""

        if name.startswith("_"):
            super().__setattr__(name, value)

        try:
            super().__setattr__(name, value)
        except ValueError:
            if "_" in name:
                # fall back to attribute on child field
                head, tail = name.rsplit("_", 1)
                if head in self.__fields__:
                    head = getattr(self, head)
                    try:
                        setattr(head, tail, value)
                    except ValueError:
                        pass
                    else:
                        return
            raise

    @validator("*", pre=True)
    def convert_datetime(cls, value: Any, field: ModelField) -> Any:
        """Correct data-type for datetime values."""

        if not isinstance(value, datetime):
            return value

        field_type = field.type_

        if not isinstance(field_type, type):
            return value

        if issubclass(field_type, str):
            suffix = "Z" if value.microsecond else ".000000Z"
            return value.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + suffix
        elif issubclass(field_type, float):
            return value.timestamp()
        elif issubclass(field_type, int):
            return int(value.timestamp() * 1e9)
        else:
            return value


P = TypeVar("P", bound=DataModel)


class PaginatorDataModel(DataModel, Generic[P]):
    """Paginator data-model."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise model."""

        super().__init__(**kwargs)

    @validator("data", pre=True, check_fields=False)
    def validate_data(cls, v: Sequence[Mapping[str, Any]], field: ModelField) -> List[P]:
        """Validate data field."""

        T = field.type_
        results = []

        for item in v:
            try:
                results += [T(**item)]
            except ValidationError as e:
                logger.warning("Skipped invalid item", name=T.__name__, item=item, error=e)

        return results

    def __getitem__(self, item: Union[str, int]) -> Any:
        """Get item."""

        if isinstance(item, int):
            return self.data[item]

        return super().__getitem__(item)

    def to_df(self) -> pd.DataFrame:
        """
        Converts the data in the object to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the data.
        """
        import pandas as pd

        if len(self.data) == 0:
            return pd.DataFrame()

        headers: List[str] = sorted(list(self.data[0].dict().keys()))
        return pd.DataFrame([item.dict() for item in self.data], columns=headers)


class KList(List[P]):
    """
    Represents a list of objects of DataModel type.

    This class extends the built-in List class and provides additional functionality.

    Methods:
        to_df(): Converts the list to a pandas DataFrame.

    """

    def to_df(self) -> pd.DataFrame:
        """
        Converts the list to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame representation of the list.

        """
        import pandas as pd

        if len(self) == 0:
            return pd.DataFrame()
        dates: List[str] = []
        krns: List[str] = []
        annotations = self[0].__annotations__
        columns = list(annotations.keys())
        for field_name, field_info in annotations.items():
            if "datetime" in field_info:
                dates.append(field_name)
            if "KRN" in field_info:
                krns.append(field_name)
        dataframe = pd.DataFrame([item.dict() for item in self], columns=columns)
        objects: List[str] = []

        dict_columns: dict[str, bool] = dataframe.transform(lambda x: x.apply(type).eq(dict)).all().to_dict()
        for key, item in dict_columns.items():
            if item:
                objects.append(key)

        index: List[str] = []
        if len(dates) > 0:
            for key in dates:
                dataframe[key] = pd.to_datetime(dataframe[key], utc=True).dt.tz_convert("UTC")
                index.append(key)
            dataframe.set_index(index, inplace=True)
        if len(krns) > 0:
            krn_index: List[str] = []
            for key in krns:
                krn_dataframe = pd.json_normalize(dataframe.pop(key).apply(parse_resource))
                krn_dataframe.index = dataframe.index
                dataframe = pd.concat([dataframe, krn_dataframe], axis=1)
                dataframe = dataframe.set_index([*krn_dataframe.columns], append=True)
                krn_index = [*krn_index, *krn_dataframe.columns]
            dataframe = dataframe.reset_index(krn_index)
        if len(objects) > 0:
            for key in objects:
                object_dataframe = pd.json_normalize(dataframe.pop(key)).apply(pd.Series).add_prefix(f"{key}.")
                object_dataframe.index = dataframe.index
                dataframe = pd.concat([object_dataframe, dataframe], axis=1)
        return dataframe


class KIterator(Iterator[P]):
    """
    An iterator class that wraps another iterator and provides additional functionality.

    Args:
        iterator (Iterator[Any]): The iterator to be wrapped.

    Attributes:
        iterator (Iterator[Any]): The wrapped iterator.

    Methods:
        __iter__(): Returns the iterator object itself.
        __next__(): Returns the next item from the iterator.
        to_df(): Convert the iterator's data into a pandas DataFrame.

    """

    def __init__(self, iterator: Iterator[Any]) -> None:
        self.iterator: Iterator[Any] = iterator

    def __iter__(self) -> Any:
        return self.iterator.__iter__()

    def __next__(self) -> Any:
        return self.iterator.__next__()

    def to_df(self, datastreams_as_column: bool = False) -> pd.DataFrame:
        INDEX = ["timestamp", "resource"]
        """
        Convert the iterator's data into a pandas DataFrame.

        Returns:
            pd.DataFrame: The pandas DataFrame containing the iterator's data.
        """
        import pandas as pd

        dataframe = pd.DataFrame.from_records(self.iterator)
        if dataframe.empty:
            return pd.DataFrame()

        if "timestamp" in dataframe.columns:
            dataframe["timestamp"] = pd.to_datetime(dataframe.timestamp, utc=True).dt.tz_convert("UTC")

        if "resource" in dataframe.columns:
            dataframe.set_index(INDEX, inplace=True)
            dataframe = dataframe.reset_index("resource")
            resource = pd.json_normalize(dataframe.pop("resource").apply(parse_resource))
            resource.index = dataframe.index
            dataframe = pd.concat([resource, dataframe], axis=1)
            dataframe = dataframe.set_index([*resource.columns], append=True)
            if datastreams_as_column:
                dataframe = dataframe.payload.unstack("datastream_name")
                dataframe = dataframe.reset_index()
                dataframe = dataframe.rename_axis(None, axis=1)
                dataframe.set_index(["timestamp", "asset_name"], inplace=True)

        return dataframe


DataModelBase = DataModel
