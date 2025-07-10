"""
main.py
=======
FastAPI micro-service that exposes a single POST endpoint `/query` consumed by
both the Streamlit app (`app.py`) and any other HTTP client.

Request / Response contract
---------------------------
Request JSON:
```
{ "question": "Plan a trip to Goa for 5 days" }
```
Response JSON:
```
{ "answer": "...Markdown travel plan..." }
```

Inside the handler we:
1. Instantiate `GraphBuilder` (our agent) – you can swap `model_provider` here.
2. Compile the graph (`react_app = graph()`).
3. Render a PNG of the LangGraph topology for debugging (`my_graph.png`).
4. Invoke the graph with the user question.

Extending the API
-----------------
• Add new routes (e.g. `/health`, `/tools`) to expose internal status.  
• Move agent instantiation to a *startup* event if you want to reuse the graph
  across requests.

Running locally
---------------
```
uvicorn main:app --reload
```
"""
from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os
import traceback

app = FastAPI()



class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query:QueryRequest):

    try:
        print(query)
        graph = GraphBuilder(model_provider="openai")
        react_app=graph()
        
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")
        
        # Assuming request is a pydantic object like: {"question": "your text"}
        messages={"messages": [query.question]}
        output = react_app.invoke(messages)

        # If result is dict with messages:
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)
        
        return {"answer": final_output}
    except Exception as e:
        # Capture full traceback for easier debugging
        tb_str = traceback.format_exc()
        # Log traceback to stdout which uvicorn will capture
        print("Error while handling /query request:\n", tb_str)
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": tb_str})
    
    