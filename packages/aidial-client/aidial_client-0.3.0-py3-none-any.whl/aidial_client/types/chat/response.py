from typing import Dict, List, Literal, Optional

from aidial_client._compatibility.pydantic import PYDANTIC_V2
from aidial_client._compatibility.pydantic_v1 import root_validator
from aidial_client._internal_types._model import ExtraAllowModel

if PYDANTIC_V2:
    from pydantic import model_validator


class Attachment(ExtraAllowModel):
    type: Optional[str] = None
    title: Optional[str] = None
    data: Optional[str] = None
    url: Optional[str] = None
    reference_type: Optional[str] = None
    reference_url: Optional[str] = None

    if PYDANTIC_V2:

        @model_validator(mode="before")
        @classmethod
        def validate_data_or_url_v2(cls, values):
            if (
                isinstance(values, dict)
                and "data" not in values
                and "url" not in values
            ):
                raise ValueError("Either data or URL must be provided")
            return values

    else:

        @root_validator(pre=True)
        def validate_data_or_url_v1(cls, values):
            if "data" not in values and "url" not in values:
                raise ValueError("Either data or URL must be provided")
            return values


class CustomContent(ExtraAllowModel):
    attachments: Optional[List[Attachment]] = None
    state: Optional[Dict] = None


class CompletionUsage(ExtraAllowModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class FunctionCall(ExtraAllowModel):
    arguments: str
    name: str


class FunctionCallDelta(ExtraAllowModel):
    arguments: Optional[str] = None
    name: Optional[str] = None


class ChatCompletionMessageToolCall(ExtraAllowModel):
    id: str
    function: FunctionCall
    type: Literal["function"]


class ToolCallDelta(ExtraAllowModel):
    index: int
    id: Optional[str] = None
    function: Optional[FunctionCallDelta] = None
    type: Optional[Literal["function"]] = None


class ChatCompletionMessage(ExtraAllowModel):
    role: Literal["assistant"]
    content: Optional[str] = None
    custom_content: Optional[CustomContent] = None
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None


class ChatCompletionMessageDelta(ExtraAllowModel):
    role: Optional[Literal["assistant"]] = None
    content: Optional[str] = None
    custom_content: Optional[CustomContent] = None
    function_call: Optional[FunctionCallDelta] = None
    tool_calls: Optional[List[ToolCallDelta]] = None


class Choice(ExtraAllowModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[str]


class ChoiceDelta(ExtraAllowModel):
    index: int
    delta: ChatCompletionMessageDelta
    finish_reason: Optional[str] = None


class ChatCompletionResponse(ExtraAllowModel):
    id: str
    object: Literal["chat.completion"]
    choices: List[Choice]
    created: int
    model: Optional[str] = None
    usage: Optional[CompletionUsage] = None


class ChatCompletionChunk(ExtraAllowModel):
    id: str
    object: Literal["chat.completion.chunk"]
    choices: List[ChoiceDelta]
    created: int
    model: Optional[str] = None
    usage: Optional[CompletionUsage] = None
