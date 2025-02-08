from langgraph.graph import StateGraph, START, END
from openai import OpenAI
import json
from models import *
from market_data import get_market_data
from config import settings



PORTFOLIO_RECCOMENDER_PROMPT = """
You are a portfolio advisor specializing in cryptocurrency investments on a Layer 2 blockchain called Base.
Your job is to analyze the user's portfolio preferences and current market data to generate an optimal investment recommendation.

### Inputs to Consider
- **Diversification Level**: `"high"`, `"medium"`, `"low"`. This determines whether the portfolio is **broadly diversified** or **focused on fewer assets**.
- **Investment Horizon**: `"short"` (1-6 months) or `"long"` (6+ months). This influences asset selection based on **volatility and expected returns**.
- **Risk Tolerance**: `"high"`, `"medium"`, `"low"`. Higher risk means **higher volatility assets**, lower risk means **more stable assets**.
- **Investment Amount**: Total amount available for allocation.
- **Market Data**: Cryptocurrency metrics, which includes token fees, name, symbol, total supply, TVL (Total Value Locked), transaction count, and volume in USD. 
                   Additionally, the data contains 7-day daily market statistics, including opening and closing prices, daily high and low prices, daily trading volume, TVL and fees.

### Instructions for Your Recommendation
1 **Select up to 10 cryptocurrencies** that align with the user's diversification preference, investment horizon, and risk tolerance. Do not reccomend stablecoins.
2 **Allocate investment** across the selected cryptocurrencies, ensuring the **allocations sum to 1.0 (100%)**.  
3 **Provide explanation** for each cryptocurrency chosen in a few sentences. Highlight key details of your decision, referencing provided market data and user input.

Your response must be in JSON format with the following structure as an example
{
  "assets": ["cbETH", "CBBTC"],
  "allocations": [0.6, 0.4],
  "analysis": {
    "cbETH": "Reason",
    "CBBTC": "Reason"
  }
}
"""

class LangGraphChatBot:
    def __init__(self):
        """Initialize the AI model and build the LangGraph workflow."""
        self.llm = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        self.graph = self._build_workflow()

    
    def _fetch_market_data(self, state: ChatState) -> ChatState:
        state["market_data"] = get_market_data()
        return state


    def _portfolio_recommendation(self, state: ChatState) -> ChatState:
        
        user_prompt = f"""
        User Portfolio Preferences:
        - Diversification level: {state["diversification_level"]}
        - Investment Horizen: {state["investment_horizon"]}
        - Risk Tolerance: {state["risk_tolerance"]}
        - Investment Amount: {state["amount"]}

        Current Market Data Prices: {state["market_data"]}
        """

        messages = [
            {"role": "system", "content": PORTFOLIO_RECCOMENDER_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        response = self.llm.beta.chat.completions.parse(
            model="gpt-4o-2024-11-20",
            temperature=0,
            messages=messages,
            response_format=Portfolio_Output
        )
    
        response = response.choices[0].message.content
        response = json.loads(response)     # converts str to dict

        state["assets"] = response["assets"]
        state["allocations"] = response["allocations"]
        state["analysis"] = response["analysis"]

        return state


    def _build_workflow(self) -> StateGraph:
        """Creates and compiles the LangGraph workflow."""
        workflow = StateGraph(ChatState)
        workflow.add_node("fetch_market_data",self._fetch_market_data)
        workflow.add_node("portfolio_recommendation", self._portfolio_recommendation)

        workflow.add_edge(START, "fetch_market_data")  
        workflow.add_edge("fetch_market_data", "portfolio_recommendation")   
        workflow.add_edge("portfolio_recommendation", END)       

        return workflow.compile()


    def run_workflow(
        self,
        request: ChatRequest
    ) -> dict:
        """Runs the LangGraph workflow with the input from requests."""
        state = ChatState(
            market_data=None,   # Retrieved later by fetch market data node
            diversification_level=request.diversification_level,
            investment_horizon=request.investment_horizon,
            risk_tolerance=request.risk_tolerance,
            amount=request.amount,
            assets=None,    # Filled later by portfolio reccomendation node
            allocations=None,
            analysis=None
        )
        result = self.graph.invoke(state)
        return result


# Create a singleton instance of the chatbot for reuse
chatbot = LangGraphChatBot()