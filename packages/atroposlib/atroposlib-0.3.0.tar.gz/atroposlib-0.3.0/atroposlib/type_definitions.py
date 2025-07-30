from typing import Any, Dict, List, Literal, Optional

from openai.types.chat import ChatCompletionContentPartParam
from typing_extensions import TypedDict

Content = str | list[ChatCompletionContentPartParam]
Item = Any
number = int | float
UUID = str


class Message(TypedDict):
    role: Literal["system", "user", "assistant", "tool"]
    content: Content
    reward: Optional[float]


class AgentStep(TypedDict, total=False):
    """Represents a single step in an agent's history.

    Attributes:
        step: The step number.
        messages: A list of messages exchanged during the step.
        reward: The reward received at this step.
    """

    step: int
    messages: List[Message]
    reward: float


# AgentHistory maps agent ids (e.g. "Player 1", "Player 2") to their respective list of steps.
AgentHistory = Dict[str, List[AgentStep]]


class Observation(TypedDict):
    """Represents an observation in a game history.

    Attributes:
        raw: The raw observation data (as a dictionary).
        rendered: The rendered string of the observation suitable for input into an LLM.
    """

    raw: Dict[str, Any]
    rendered: Content


class GameStep(TypedDict):
    """Represents a single step in a game history. Essentially an (s,a,r) triple with metadata.

    Attributes:
        step: The step number.
        agent: The agent who took the action (optional for final steps).
        observation: The observation at this step.
        action: The action taken by the agent (if any).
        reward: The reward received; can be a float or a dictionary mapping agent names to rewards.
        done: A flag indicating whether the game has ended after this step.
        info: Additional information related to the step.
    """

    step: int
    agent_id: str
    observation: Observation
    action: str
    reward: float | Dict[str, float]
    done: bool
    info: Dict[str, Any]


# GameHistory is represented as a list of game steps.
GameHistory = List[GameStep]


class EvaluationConfigGeneral(TypedDict):
    """Configuration section of evaluation results."""

    total_evaluation_time_secondes: str
    model_name: Optional[str]
    generation_parameters: Dict[str, Any]


class EvaluationResults(TypedDict):
    """Results section containing metrics for tasks and aggregated results."""

    all: Dict[str, float]  # Aggregated metrics across all tasks


class EvaluationMetrics(TypedDict):
    """Complete evaluation metrics JSON structure."""

    config_general: EvaluationConfigGeneral
    results: EvaluationResults


class EvaluationSample(TypedDict, total=False):
    """Individual sample data written to JSONL files.

    All fields are optional to accommodate different evaluation scenarios.
    """

    messages: Optional[List[Dict[str, str]]]
    question: Optional[str]
    gold_answer: Optional[str]
    gold_parsed: Optional[str]
    model_parsed: Optional[str]
    score: Optional[int]
    correct: Optional[bool]
    finish_reason: Optional[str]
    response_after_think: Optional[str]
