from enum import Enum
from typing import List

from pydantic import BaseModel


class Model(str, Enum):
    it5_small = "it5-small"
    mt5_small = "mt5-small"
    umt5_small = "umt5-small"
    gpt2_small_italian = "gpt2-small-italian"


class PredictionRequest(BaseModel):
    model: Model
    paragraphs: List[str]
