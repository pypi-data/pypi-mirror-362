# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .token_usage import TokenUsage
from .document_result import DocumentResult

__all__ = [
    "PersistentMessage",
    "IntermediateStep",
    "IntermediateStepToolObservations",
    "IntermediateStepToolObservationsDecisfraToolObservations",
    "IntermediateStepToolObservationsStockInfoToolObservations",
    "IntermediateStepToolObservationsStockInfoToolObservationsStockInfo",
    "IntermediateStepToolObservationsCompanyNewsToolObservations",
    "IntermediateStepToolObservationsCompanyNewsToolObservationsNewsResult",
    "IntermediateStepToolObservationsPerplexityToolObservations",
    "IntermediateStepToolObservationsRagToolObservations",
    "IntermediateStepToolObservationsDocumentChunksResult",
    "IntermediateStepToolObservationsProjectFilesResult",
    "IntermediateStepToolObservationsProjectFilesResultFile",
    "IntermediateStepToolObservationsWayakDataAnalysisResponse",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseArtifact",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifact",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactDataframeResult",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactNumberResult",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactTextResult",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactPlotResult",
    "IntermediateStepToolObservationsWayakDataAnalysisResponseReasoning",
]


class IntermediateStepToolObservationsDecisfraToolObservations(BaseModel):
    content: str

    data: Dict[str, object]

    tool_name: str = FieldInfo(alias="toolName")


class IntermediateStepToolObservationsStockInfoToolObservationsStockInfo(BaseModel):
    average_volume: Optional[int] = FieldInfo(alias="averageVolume", default=None)

    current_price: Optional[float] = FieldInfo(alias="currentPrice", default=None)

    day_high: Optional[float] = FieldInfo(alias="dayHigh", default=None)

    day_low: Optional[float] = FieldInfo(alias="dayLow", default=None)

    dividend_yield: Optional[float] = FieldInfo(alias="dividendYield", default=None)

    fifty_two_week_high: Optional[float] = FieldInfo(alias="fiftyTwoWeekHigh", default=None)

    fifty_two_week_low: Optional[float] = FieldInfo(alias="fiftyTwoWeekLow", default=None)

    forward_pe: Optional[float] = FieldInfo(alias="forwardPE", default=None)

    market_cap: Optional[int] = FieldInfo(alias="marketCap", default=None)

    open: Optional[float] = None

    previous_close: Optional[float] = FieldInfo(alias="previousClose", default=None)

    trailing_pe: Optional[float] = FieldInfo(alias="trailingPE", default=None)

    volume: Optional[int] = None


class IntermediateStepToolObservationsStockInfoToolObservations(BaseModel):
    query: str

    stock_info: IntermediateStepToolObservationsStockInfoToolObservationsStockInfo

    tool_name: str = FieldInfo(alias="toolName")


class IntermediateStepToolObservationsCompanyNewsToolObservationsNewsResult(BaseModel):
    content: str

    description: str

    language: str

    source: str

    title: str


class IntermediateStepToolObservationsCompanyNewsToolObservations(BaseModel):
    news_results: List[IntermediateStepToolObservationsCompanyNewsToolObservationsNewsResult]

    query: str

    tool_name: str = FieldInfo(alias="toolName")


class IntermediateStepToolObservationsPerplexityToolObservations(BaseModel):
    citations: List[str]

    content: str

    tool_name: str = FieldInfo(alias="toolName")

    model: Optional[str] = None

    usage: Optional[TokenUsage] = None


class IntermediateStepToolObservationsRagToolObservations(BaseModel):
    documents: List[DocumentResult]

    query: str

    tool_name: str = FieldInfo(alias="toolName")

    embedding_model: Optional[str] = None

    usage: Optional[TokenUsage] = None


class IntermediateStepToolObservationsDocumentChunksResult(BaseModel):
    document_id: str

    documents: List[DocumentResult]

    file_name: str

    tool_name: str = FieldInfo(alias="toolName")


class IntermediateStepToolObservationsProjectFilesResultFile(BaseModel):
    file_id: str

    file_name: str

    file_type: str

    total_pages: Optional[int] = None


class IntermediateStepToolObservationsProjectFilesResult(BaseModel):
    files: List[IntermediateStepToolObservationsProjectFilesResultFile]

    project_id: str

    tool_name: str = FieldInfo(alias="toolName")


class IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactDataframeResult(BaseModel):
    dataframe: Optional[str] = None

    dataframe_url: Optional[str] = None


class IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactNumberResult(BaseModel):
    number: Optional[float] = None


class IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactTextResult(BaseModel):
    text: Optional[str] = None


class IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactPlotResult(BaseModel):
    plot_insights: str

    plot_url: str


IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifact: TypeAlias = Union[
    IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactDataframeResult,
    IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactNumberResult,
    IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactTextResult,
    IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifactPlotResult,
]


class IntermediateStepToolObservationsWayakDataAnalysisResponseArtifact(BaseModel):
    artifact: IntermediateStepToolObservationsWayakDataAnalysisResponseArtifactArtifact

    artifact_type: Optional[Literal["plot", "dataframe", "number", "text"]] = None


class IntermediateStepToolObservationsWayakDataAnalysisResponseReasoning(BaseModel):
    code: Optional[str] = None

    explanation: str


class IntermediateStepToolObservationsWayakDataAnalysisResponse(BaseModel):
    artifacts: Optional[List[IntermediateStepToolObservationsWayakDataAnalysisResponseArtifact]] = None

    query: Optional[str] = None

    reasoning: Optional[IntermediateStepToolObservationsWayakDataAnalysisResponseReasoning] = None

    tool_name: str = FieldInfo(alias="toolName")

    model: Optional[str] = None

    usage: Optional[TokenUsage] = None


IntermediateStepToolObservations: TypeAlias = Union[
    IntermediateStepToolObservationsDecisfraToolObservations,
    IntermediateStepToolObservationsStockInfoToolObservations,
    IntermediateStepToolObservationsCompanyNewsToolObservations,
    IntermediateStepToolObservationsPerplexityToolObservations,
    IntermediateStepToolObservationsRagToolObservations,
    IntermediateStepToolObservationsDocumentChunksResult,
    IntermediateStepToolObservationsProjectFilesResult,
    IntermediateStepToolObservationsWayakDataAnalysisResponse,
    Dict[str, object],
    None,
]


class IntermediateStep(BaseModel):
    content: str

    role: str

    token_usage: Optional[TokenUsage] = None

    tool_calls: Optional[List[Dict[str, object]]] = None

    tool_name: Optional[str] = None

    tool_observations: Optional[IntermediateStepToolObservations] = None


class PersistentMessage(BaseModel):
    content: Dict[str, object]

    created_at: datetime

    edited_at: Optional[datetime] = None

    role: str

    thread_id: str

    id: Optional[str] = None

    agent_type: Optional[Literal["REACT", "WAYAK_V1", "DATA_ANALYST_V1"]] = None

    brain_id: Optional[str] = None

    brain_name: Optional[str] = None

    citations: Optional[List[str]] = None

    content_text: Optional[str] = None

    deleted_at: Optional[datetime] = None

    documents: Optional[Dict[str, object]] = None

    images: Optional[List[str]] = None

    intermediate_steps: Optional[List[IntermediateStep]] = None

    message_processing_status: Optional[Literal["NOT_STARTED", "PROCESSING", "ERROR", "SUCCESS"]] = None

    models: Optional[List[str]] = None

    token_usage: Optional[TokenUsage] = None

    usage_synced_at: Optional[datetime] = None
