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

1. **Add a new tool** – create a class in `tools/` that returns a list of `@tool`-decorated callables.  
2. Append the tool list in `agent/agentic_workflow.py` (`self.tools.extend([...])`).  
3. The agent can now call it autonomously – no further changes required.

LangGraph ensures the agent decides when to call which tool and loops until it reaches an END node.

---

## 🧪 Running notebooks / experiments
Jupyter notebooks can live in `experiments/` for rapid prototyping; they share the same utilities & config loader as the main app.

---

## 📜 License
Distributed under the MIT License. Feel free to fork-and-build your own production-grade agentic apps!