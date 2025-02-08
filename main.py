from fastapi import FastAPI
from models import ChatRequest, ChatResponse
from ai_logic import chatbot  # Import the chatbot instance

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    response = chatbot.run_workflow(request=request)
    
    return ChatResponse(
        assets=response["assets"],
        allocations=response["allocations"],
        analysis=response["analysis"]
    )



# Run with: uvicorn main:app --reload
