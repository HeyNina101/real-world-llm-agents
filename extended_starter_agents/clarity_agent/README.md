# Clarity Agent

A simple and decoupled AI agent that analyzes topics and provides balanced lists of pros and cons using different LLM providers.

## Features

- **Decoupled architecture**: Easy switching between LLM providers
- **Multiple providers**: Support for OpenAI and Anthropic
- **REST API**: Simple interface with FastAPI
- **Flexible configuration**: Environment variables for all settings
- **Structured logging**: Detailed logs with Loguru
- **Robust validation**: Input and response validation

## 📁 Project Structure

```
clarity_agent/
├── agent/             # Agent logic
├── llm/               # LLM providers
│   └── platforms/     # Specific implementations
├── api/               # REST API
├── config/            # Configuration
├── utils/             # Utilities
└── tests/             # Tests
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/HeyNina101/real-world-llm-agents.git
cd real-world-llm-agents/extended_starter_agents/clarity_agent

```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

## ⚙️ Configuration

Set up your `.env` file with the required API keys:

```env
# Required: At least one API key
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Optional: Provider configuration
DEFAULT_LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

## 🚀 Usage

### Start the server
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example requests

**Analyze a topic:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Remote work",
    "llm_provider": "openai"
  }'
```

**Check available providers:**
```bash
curl "http://localhost:8000/providers"
```

**Health check:**
```bash
curl "http://localhost:8000/"
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/analyze` | Analyze topic |
| GET | `/agent/info` | Agent information |
| GET | `/providers` | List providers |

## 🏗️ Architecture

### Agent Layer
- `BaseAgent`: Abstract base class for all agents
- `ClarityAgent`: Implementation for pros/cons analysis

### LLM Layer
- `BaseLLMProvider`: Abstract base for LLM providers
- `OpenAIProvider`: OpenAI implementation
- `AnthropicProvider`: Anthropic implementation

### Benefits of this architecture:
- **Easy to extend**: Add new providers by implementing `BaseLLMProvider`
- **Easy to test**: Mock providers for testing
- **Configuration driven**: Switch providers via environment variables
- **Separation of concerns**: Each layer has a single responsibility

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.
```

## 🔧 Development

### Adding a new LLM provider

1. Create a new file in `llm/platforms/`
2. Implement `BaseLLMProvider`
3. Add provider to the factory in `api/api.py`
4. Update configuration in `config/settings.py`

### Adding a new agent type

1. Create a new file in `agent/`
2. Implement `BaseAgent`
3. Add endpoints in `api/api.py`

## 📝 Example Response

```json
{
  "success": true,
  "data": {
    "topic": "Remote Work",
    "analysis": {
      "pros": [
        "Increased flexibility and work-life balance",
        "Reduced commuting costs and time",
        "Access to global talent pool"
      ],
      "cons": [
        "Potential isolation and communication challenges",
        "Difficulties in team collaboration",
        "Blurred boundaries between work and personal life"
      ]
    },
    "summary": "Remote work offers flexibility benefits but requires careful management of communication and boundaries."
  },
  "message": "Analysis completed successfully",
  "metadata": {
    "model_used": "gpt-3.5-turbo",
    "tokens_used": 245,
    "provider": "openai"
  }
}
```

## 📄 License

This project is licensed under the MIT License.