from pydantic import BaseModel
from typing import TypedDict, Optional, Dict


class ChatRequest(BaseModel):
    diversification_level: str      # can be high,medium,low
    investment_horizon: str         # can be short,long 
    risk_tolerance: str             # can be high,medium,low
    amount: float                   # investment amount


class Analysis_Output(BaseModel):
    asset_name: str
    reason: str


class Portfolio_Output(BaseModel):
    assets: list[str]
    allocations: list[float]
    analysis: list[Analysis_Output]


class ChatState(TypedDict):
    market_data: Optional[dict]
    diversification_level: str      # can be high,medium,low
    investment_horizon: str         # can be short,long 
    risk_tolerance: str             # can be high,medium,low
    amount: float                   # investment amount
    assets: Optional[list[str]]
    allocations: Optional[list[float]]
    analysis: Optional[dict]
    

class ChatResponse(Portfolio_Output):
    pass
