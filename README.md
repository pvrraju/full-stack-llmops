# 🌍 Full-Stack LLMOps – AI Travel Planner

An end-to-end reference project that demonstrates how to build, wire, and ship **agentic applications** powered by Large-Language-Models (LLMs).

The app you run is an **AI Travel Planner & Expense Estimator**:

* Ask for any trip plan – e.g. *"Plan me a 7-day budget trip to Vienna in October"*.
* The agent fetches real-time weather, top attractions / restaurants, transportation options, converts currencies, and calculates daily budgets.
* Results are returned as a neatly-formatted Markdown itinerary.

Under the hood the project shows how to combine

* **LangGraph + LangChain** for tool-calling agents
* **FastAPI** for the backend API
* **Streamlit** for a low-code front-end
* Proper **configuration / logging / exception handling** for production-ready LLM services.



---





## 📂 Project Layout

```text
full-stack-llmops/
├── agent/                   # LangGraph agent + tools wiring
│   └── agentic_workflow.py
├── tools/                  # Re-usable external tools (weather, places, etc.)
├── utils/                  # Helper classes (model loader, converters, …)
├── config/                 # YAML config & secrets indirection
├── main.py                 # FastAPI app (backend API)
├── app.py                  # Streamlit UI (front-end)
├── requirements.txt        # Python dependencies
└── README.md               # ← you are here
```

---

## 🛠️  Features & Architecture

| Layer | Tech | Responsibilities |
|-------|------|------------------|
| **LLM Agent** | LangGraph (`GraphBuilder`) | 1) Accept user query 2) Decide whether a tool call is required 3) Execute tool(s) 4) Respond.  The graph is compiled once & cached. |
| **Tools** | LangChain Tools | • `WeatherInfoTool` – OpenWeatherMap API  
• `PlaceSearchTool` – Google Places API + Tavily fallback  
• `CalculatorTool` – hotel / expense arithmetic  
• `CurrencyConverterTool` – Exchange-rate API |
| **Model Loader** | `utils/model_loader.py` | Loads **OpenAI** (`gpt-4o-mini` by default) or **Groq** models via env vars & YAML config. |
| **Backend** | FastAPI (`main.py`) | Exposes POST `/query` → JSON `{answer: …}`. Captures & returns tracebacks for easier debugging. |
| **Front-end** | Streamlit (`app.py`) | Minimal chat-like interface that calls the backend and renders itinerary Markdown. |
| **Observability** | `my_graph.png` | Each request re-exports the agent graph as a Mermaid PNG for easy visual inspection. |

---

## 🚀 Quick-start

### 1. Clone & enter project
```bash
git clone https://github.com/your_username/full-stack-llmops.git
cd full-stack-llmops
```

### 2. Create virtual env & install deps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
(Or use `uv venv`/`uv pip` if you prefer.)

### 3. Set environment variables
```bash
# LLM provider
export OPENAI_API_KEY="sk-..."            # required (or set GROQ_API_KEY instead)

# Tool providers
export OPENWEATHERMAP_API_KEY="..."       # Weather
export GPLACES_API_KEY="..."              # Google Places
export EXCHANGE_RATE_API_KEY="..."        # Currency conversion
# (Tavily Search uses its public endpoint and needs no key by default)
```
You may also tweak `config/config.yaml` to change the default model.

### 4. Run backend & front-end (two terminals)
```bash
# Terminal 1 – FastAPI backend
uvicorn main:app --reload

# Terminal 2 – Streamlit front-end
streamlit run app.py
```
Navigate to `http://localhost:8501` in your browser and start chatting!

---

## 🔍 Endpoints

| Method | Path | Payload | Response |
|--------|------|---------|----------|
| POST | `/query` | `{ "question": "Plan a trip to Goa for 5 days" }` | `{ "answer": "…markdown itinerary…" }` |

All server-side exceptions are returned with HTTP 500 and include a `traceback` field for transparent debugging during development.

---

## 🤖 Extending the Agent
## 🤖 Build **Your Own** Tool-Equipped Agent

This project is intentionally opinionated *yet* highly extensible. In just a few
lines of code you can bolt on brand-new capabilities, swap the LLM, or even
reshape the entire execution graph.

### 1️⃣ Create a tool

````python
# tools/flight_search_tool.py
from langchain.tools import tool
from typing import List

class FlightSearchTool:
    def __init__(self):
        self.flight_tool_list: List = self._setup_tools()

    def _setup_tools(self) -> List:
        @tool
        def find_cheapest_flight(origin: str, destination: str, date: str) -> dict:
            """Return the cheapest flight for the given route & date."""
            # Call your favourite flight API here…
            return {"price": 350, "airline": "Example Air"}

        return [find_cheapest_flight]
````

*A tool is nothing more than a Python callable with JSON-serialisable inputs &
outputs plus the `@tool` decorator.*

### 2️⃣ Register the tool

Open `agent/agentic_workflow.py` and add:

```python
from tools.flight_search_tool import FlightSearchTool

self.flight_tools = FlightSearchTool()
self.tools.extend(self.flight_tools.flight_tool_list)
```

That’s it—the LLM can now autonomously decide when to invoke
`find_cheapest_flight`.

### 3️⃣ (optional) Tweak the system prompt

Tell the LLM *when* to use your new skill by editing
`prompt_library/prompts.py`:

> "When the user asks about flights, call `find_cheapest_flight`."

### 4️⃣ Choose your LLM

Swap providers by editing `config/config.yaml` **or** passing
`GraphBuilder(model_provider="groq")` (OpenAI is default).

### 5️⃣ Evolve the graph

Add memory, retrieval augmentation, guardrail nodes, etc. by updating
`GraphBuilder.build_graph()`. LangGraph compiles the topology once per request
and caches it, so experimentation is quick.

---

## 🏗️ Reuse the framework for **any** domain

Replace the travel-specific tools with finance calculators, knowledge-base
search, IoT device controllers—whatever your project requires. The surrounding
infrastructure (FastAPI, Streamlit, config, logging) remains unchanged so you
can focus exclusively on tool logic and prompt design.

---

## 🧪 Running notebooks / experiments
Jupyter notebooks can live in `experiments/` for rapid prototyping; they share the same utilities & config loader as the main app.

---

## 📜 License
Distributed under the MIT License. Feel free to fork-and-build your own production-grade agentic apps!