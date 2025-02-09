import unittest
from ai_logic import *
from models import *

class TestGetRecommendation(unittest.TestCase):
    
    def test_portfolio_recommendation(self):
        chatbot = LangGraphChatBot()
        
        request = ChatRequest(
            diversification_level="high",
            investment_horizon="short",
            risk_tolerance="high",
            amount= 100
        )

        response = chatbot.run_workflow(request=request)
        print(response)

        self.assertIsInstance(response, dict) 



# Run test
# python -m unittest ./tests/test_ai_logic.py

