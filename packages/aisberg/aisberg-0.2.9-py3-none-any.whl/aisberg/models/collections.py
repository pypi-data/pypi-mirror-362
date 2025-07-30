from typing import List, Optional, Union
from pydantic import BaseModel


class Collection(BaseModel):
    name: str


class GroupCollections(BaseModel):
    group: str
    collections: List[Collection]


class CollectionDataset(BaseModel):
    chunks: List[str]
    metadata: Optional[dict] = []


class CollectionCreateResponse(BaseModel):
    message: Optional[str] = None


class ChunkingDictInput(BaseModel):
    method: Optional[str] = "custom"
    params: Optional[dict] = {}


class ParseDataInput(BaseModel):
    source: Optional[str] = None
    diarize: Optional[bool] = False
    input: Optional[str] = None
    group: Optional[str] = None
    stt_model: Optional[str] = None
    vlm_model: Optional[str] = None


# Modèle plus structuré pour payload
class Payload(BaseModel):
    method: Optional[str] = None
    norm: Optional[Union[str, bool]] = None
    filetype: Optional[str] = None
    filename: Optional[str] = None
    dense_encoder: Optional[str] = None
    Category: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[str] = None
    collection_name: Optional[str] = None
    sparse_encoder: Optional[str] = None


class PointDetails(BaseModel):
    id: str
    payload: Payload


class CollectionDetails(BaseModel):
    name: str
    group: Optional[str] = None
    points: List[PointDetails]
