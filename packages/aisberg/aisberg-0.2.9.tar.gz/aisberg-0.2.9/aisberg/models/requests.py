from typing import List, Any, Tuple
from io import BytesIO

from pydantic import BaseModel, RootModel, ConfigDict


class AnyDict(BaseModel):
    model_config = ConfigDict(extra="allow")


class AnyList(RootModel[List[Any]]):
    pass


HttpxFileField = List[Tuple[str, Tuple[str, BytesIO, str]]]
