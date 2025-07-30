from typing import Dict, List, Union, Any, Optional
from pydantic import BaseModel, computed_field, ConfigDict
from enum import StrEnum


class EventTypes(StrEnum):
    run_started = "run.started"
    run_step_delta = "run.step.delta"
    message_started = "message.started"
    message_delta = "message.delta"
    message_created = "message.created"
    run_completed = "run.completed"
    done = "done"


class ContentType(StrEnum):
    text = "text"
    tool_call = "tool_call"
    tool_response = "tool_response"
    conversational_search = "conversational_search"


class ConversationalSearchCitations(BaseModel):
    url: str
    body: str
    text: str
    title: str
    range_end: int
    range_start: int
    search_result_idx: int


class ConversationalSearchResultMetadata(BaseModel):
    score: float
    document_retrieval_source: str


class ConversationalSearchResults(BaseModel):
    url: str
    body: str
    title: str
    result_metadata: ConversationalSearchResultMetadata


class ConversationalConfidenceThresholdScore(BaseModel):
    response_confidence: float
    response_confidence_threshold: float
    retrieval_confidence: float
    retrieval_confidence_threshold: float

    def table(self):
        return {
            "response_confidence": str(self.response_confidence),
            "response_confidence_threshold": str(self.response_confidence_threshold),
            "retrieval_confidence": str(self.retrieval_confidence),
            "retrieval_confidence_threshold": str(self.retrieval_confidence_threshold),
        }


class ConversationSearchMetadata(BaseModel):
    """This class is used to store additional informational about the conversational search response that was not part of the API response.

    For example, the tool call that generated the conversational search response is not part of the API response. However,
    during evaluation, we want to refer to the tool that generated the conversational search response.
    """

    tool_call_id: str
    model_config = ConfigDict(frozen=True)


class ConversationalSearch(BaseModel):
    metadata: ConversationSearchMetadata
    response_type: str
    text: str  # same as `content` in Message. This field can be removed if neccesary
    citations: List[ConversationalSearchCitations]
    search_results: List[ConversationalSearchResults]
    citations_title: str
    confidence_scores: ConversationalConfidenceThresholdScore
    response_length_option: str


class Message(BaseModel):
    role: str
    content: Union[str, Dict[str, Any]]
    type: ContentType
    # event that produced the message
    event: Optional[str] = None
    # used to correlate the Message with the retrieval context (ConversationalSearch)
    conversational_search_metadata: Optional[ConversationSearchMetadata] = None

    model_config = ConfigDict(frozen=True)


class ExtendedMessage(BaseModel):
    message: Message
    reason: dict | None = None


class KnowledgeBaseGoalDetail(BaseModel):
    enabled: bool = False
    metrics: list = []


class GoalDetail(BaseModel):
    name: str
    tool_name: str = None
    type: ContentType
    args: Dict = None
    response: str = None
    keywords: List = None
    knowledge_base: KnowledgeBaseGoalDetail = KnowledgeBaseGoalDetail()


class EvaluationData(BaseModel):
    agent: str
    goals: Dict
    story: str
    goal_details: List[GoalDetail]
    starting_sentence: str = None
