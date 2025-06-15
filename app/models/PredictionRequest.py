from enum import Enum
from typing import List

from pydantic import BaseModel


class Model(str, Enum):
    mt5_small = "sempl-it-mt5-small"
    umt5_small = "sempl-it-umt5-small"
    gpt2_small_italian = "sempl-it-gpt2-small-italian"


class PredictionRequest(BaseModel):
    model: Model
    paragraphs: List[str]
