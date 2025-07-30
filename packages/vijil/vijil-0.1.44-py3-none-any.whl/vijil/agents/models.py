from dataclasses import dataclass, field
from typing import List, Optional, Literal, Union, Dict
import time
import uuid


# Message objects used in both requests and responses
@dataclass
class RetrievalData:
    id: Optional[str] = None
    index: Optional[str] = None
    content: Optional[str] = None
    score: Optional[float] = None
    filename: Optional[str] = None


@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant", "tool", "function"]
    content: Optional[str] = None
    name: Optional[str] = None
    function_call: Optional[Dict[str, str]] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Union[str, Dict[str, str]]]]] = None
    retrieval_context: Optional[List[RetrievalData]] = None


# Request format
@dataclass
class ChatCompletionRequest:
    model: str
    messages: List[Dict[str, str]]
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = 1
    stream: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    max_completion_tokens: Optional[int] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[str, float]] = None
    user: Optional[str] = None
    timeout: Optional[float] = None


# Response usage block
@dataclass
class Usage:
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]


# Response choice block
@dataclass
class ChatCompletionChoice:
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = "stop"


# Full response
@dataclass
class ChatCompletionResponse:
    id: str = str(uuid.uuid4())
    object: Literal["chat.completion"] = "chat.completion"
    created: int = field(default_factory=lambda: int(time.time()))
    model: str = ""
    choices: List[ChatCompletionChoice] = field(default_factory=list)
    usage: Optional[Usage] = None
