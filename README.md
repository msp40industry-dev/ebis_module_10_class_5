# 🚀 Multi-Agent Chatbot with FastAPI + LangGraph + Docker

Complete chatbot system with microservices architecture and multi-agent orchestration using FastAPI backend and Gradio frontend.

Part of Master's in Generative AI Engineering - EBIS Business Techschool
Module: Popular Frameworks and Libraries - Class 5

## 📋 Description

This project implements a chatbot system with two operating modes:

1. **Simple Chatbot**: Direct conversation with LLM using full context history
2. **Multi-Agent System**: Supervisor orchestrates specialized agents (research + math) to handle complex queries

The system is built with microservices architecture, containerized with Docker, and features a REST API backend with interactive web frontend.

## 🎯 Features

### Chatbot Mode
* **Stateless architecture**: Each request includes full conversation history
* **Context-aware responses**: LLM processes accumulated context
* **Simple conversational interface**: Direct Q&A without specialization

### Multi-Agent Mode
* **Supervisor orchestration**: Analyzes queries and delegates to specialists
* **Research Agent**: Web search via Tavily API for current information
* **Math Agent**: Precise calculations (add, multiply, divide) without hallucinations
* **Coordinated responses**: Supervisor combines results from multiple agents

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────┐
│                   User                          │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│         Gradio Frontend (Port 7860)             │
│         - Chat interface                         │
│         - Markdown rendering                     │
│         - Streaming effect                       │
└───────────────────┬─────────────────────────────┘
                    │ HTTP Request
                    ▼
┌─────────────────────────────────────────────────┐
│         FastAPI Backend (Port 8000)             │
│         - /chatbot endpoint                      │
│         - /multiagent endpoint                   │
│         - Swagger documentation                  │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│            LangGraph Orchestrator               │
│         - State machine management               │
│         - Agent coordination                     │
└───────────────────┬─────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│  Supervisor  │────────│  OpenAI      │
│    Agent     │        │  GPT-4.1     │
└──────┬───────┘        └──────────────┘
       │
       ├─────────┬─────────────┐
       ▼         ▼             ▼
┌─────────┐ ┌─────────┐  ┌─────────┐
│Research │ │  Math   │  │  Other  │
│ Agent   │ │ Agent   │  │ Agents  │
└─────────┘ └─────────┘  └─────────┘
```

## 🛠️ Tech Stack

- **FastAPI**: Modern Python web framework for building APIs
- **Gradio**: Interactive web UI for chat interface
- **LangGraph**: State machine orchestration for agents
- **LangChain**: Agent framework and tooling
- **OpenAI GPT-4.1**: Language model
- **Tavily API**: Web search integration
- **Docker + docker-compose**: Containerization
- **Python 3.10+**

## 🚀 Usage

Check the project files for complete implementation:
- `backend.py`: FastAPI endpoints
- `frontend.py`: Gradio chat interface
- `chatbot_agent/agent.py`: Simple chatbot logic
- `multiagent/agent.py`: Multi-agent supervisor
- `multiagent/research.py`: Research agent with Tavily
- `multiagent/math.py`: Math agent with calculation tools

### Running with Docker

The recommended way to run the application:

Start both services:
```bash
docker-compose up --build
```

Access:
- **Frontend**: http://localhost:7860
- **Backend API**: http://localhost:8000/docs

### Running Locally (without Docker)

Backend:
```bash
uvicorn backend:app --reload
```

Frontend (in separate terminal):
```bash
python frontend.py
```

## 📡 API Endpoints

### POST /chatbot

Simple conversational endpoint.

**Request:**
- `user_input`: User's message
- `history`: List of previous messages (role + content)

**Response:**
- `result`: LLM response
- `history`: Updated conversation history

### POST /multiagent

Multi-agent orchestration endpoint.

**Request:**
- `user_input`: User's query

**Response:**
- `result`: Coordinated response from agents
- `history`: Full message history including tool calls

## 🤖 Multi-Agent System

### Supervisor Agent

Central coordinator that:
- Analyzes incoming queries
- Decides which specialist agent(s) to use
- Manages handoff between agents
- Synthesizes final response

### Research Agent

**Tool**: Tavily Search API
- Searches web for current information
- Returns up-to-date data
- Example: GDP figures, current events, recent statistics

### Math Agent

**Tools**: add(), multiply(), divide()
- Performs precise calculations
- No hallucinations on numerical data
- Example: Percentage calculations, financial computations

### Example Flow

Query: *"Find the GDP of Spain and Andalusia for 2024. What percentage of Spain's GDP does Andalusia represent?"*

1. Supervisor receives query
2. Delegates to **Research Agent** → Searches GDP data
3. Research Agent returns: Spain GDP = 1,594,330M €, Andalusia GDP = 221,372M €
4. Supervisor delegates to **Math Agent** → Calculates percentage
5. Math Agent returns: 13.88%
6. Supervisor synthesizes final answer with both data and calculation

## 🐳 Docker Configuration

### docker-compose.yml

Two separate services:
- **backend**: FastAPI server (port 8000)
- **frontend**: Gradio interface (port 7860)

### Benefits

✓ **Independent scaling**: Scale services separately
✓ **Decoupled architecture**: Frontend/backend separation
✓ **Easy deployment**: Single command to run entire stack
✓ **Fault isolation**: One service failure doesn't crash the other
✓ **Portability**: Run anywhere Docker is available

## 💡 Key Concepts

**Microservices Architecture**
- Separation of concerns (frontend vs backend)
- Independent deployment and scaling
- Service-to-service communication via HTTP

**Stateless REST API**
- No server-side session storage
- Client sends full context in each request
- Horizontally scalable

**Multi-Agent Orchestration**
- Supervisor pattern for task delegation
- Specialized agents for specific capabilities
- Handoff tools for agent-to-agent transitions
- Coordinated response synthesis

**LangGraph State Management**
- State machine for agent workflows
- Message history tracking
- Tool call coordination

## 📁 Project Structure
```
multiagent-fastapi-chatbot/
├── backend.py                    # FastAPI endpoints
├── frontend.py                   # Gradio UI
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Multi-service orchestration
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── chatbot_agent/
│   ├── agent.py                 # Simple chatbot logic
│   └── utils.py                 # Helper functions
└── multiagent/
    ├── agent.py                 # Supervisor agent
    ├── research.py              # Research agent (Tavily)
    ├── math.py                  # Math agent (calculator)
    └── utils.py                 # Utility functions
```

## ⚙️ Configuration

Required environment variables (`.env` file):
```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

Optional configuration:
- `API_URL`: Backend URL (default: http://localhost:8000/multiagent)

## 🔜 Potential Improvements

- [ ] Add authentication and user management
- [ ] Implement conversation persistence (database)
- [ ] Add more specialized agents (code, finance, etc.)
- [ ] Streaming responses from backend
- [ ] Rate limiting and request validation
- [ ] Monitoring and logging (Prometheus, Grafana)
- [ ] CI/CD pipeline for automated deployment
- [ ] Kubernetes deployment manifests
- [ ] API versioning
- [ ] WebSocket support for real-time updates

## 📚 References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gradio Documentation](https://gradio.app/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## 📄 License

MIT License

## 👨‍💻 Author

Miguel - Master's in Generative AI Engineering @ EBIS Business Techschool

https://www.linkedin.com/in/miguel-s%C3%A1nchez-pinto-03771922a/ 

---

⭐ If you find this project useful, give it a star on GitHub!
