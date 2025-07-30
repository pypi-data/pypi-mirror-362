# 🧬 Forgen

A Python framework for building generative AI wrapper components, including agents, tools, pipelines, and training utilities. Forgen provides a modular architecture for creating AI-driven applications with structured input/output processing and LLM integration.

## 🚀 Quick Start

```bash
# Install in development mode
pip install -e .

# Install from requirements
pip install -r requirements.txt

# Run tests
python forgen/agent/test.py
python forgen/tool/test.py
python forgen/pipeline/test.py
```

## 🏗️ Core Architecture

Forgen is built around four primary modules that work together to create powerful AI-driven applications:

### 🤖 **Agent Module** (`forgen/agent/`)

The Agent module provides intelligent, autonomous components that can make decisions and execute complex workflows using LLMs.

**Key Components:**
- **`GenerativeAgent`**: Main agent class with prompt-based behavior and module composition
- **`AgentBuilder`**: Constructs agents by chaining GenerativeNodes
- **`GenerativeNode`**: Processing unit with InputPhase → GenerationPhase → OutputPhase flow

**Core Features:**
- Autonomous strategy generation using LLMs
- Dynamic tool selection and execution
- Multi-iteration problem solving
- Modular composition with other agents and tools

```python
from forgen.agent import GenerativeAgent

agent = GenerativeAgent(
    prompt="Analyze financial data and provide insights",
    modules=[calculator_tool, data_analyzer, report_generator],
    max_iterations=5
)

result = agent.execute({"financial_data": data})
```

### 🔧 **Tool Module** (`forgen/tool/`)

The Tool module provides modular processing units that follow a tri-phase pattern for consistent data processing.

**Key Components:**
- **`Tool`**: Basic processing unit with input/output schemas and validation
- **`GenerativeTool`**: LLM-powered tool for content generation and analysis
- **`ToolBuilder`**: Creates tools with input/output schemas and validation
- **`AutoToolGenerator`**: Automatically generates tools from natural language descriptions

**Core Features:**
- Tri-phase processing (Input → Operative → Output)
- Schema validation with `forced_interface` option
- Automatic tool generation from descriptions
- Sandboxed execution environment

```python
from forgen.tool import ToolBuilder

builder = ToolBuilder(tool_name="text_analyzer")
builder.set_input_schema({"text": str})
builder.set_output_schema({"sentiment": str, "confidence": float})
builder.set_operative_function(analyze_text)

analyzer = builder.build()
result = analyzer.execute({"text": "Great product!"})
```

### 🔄 **Pipeline Module** (`forgen/pipeline/`)

The Pipeline module manages complex workflows with dependencies between components, enabling sophisticated multi-step processing.

**Key Components:**
- **`Pipeline`**: Manages workflows with component dependencies
- **`PipelineBuilder`**: Constructs pipelines from multiple agents/tools
- **`SerialPipeline`**: Sequential execution of components
- **`MultiPathPipeline`**: Parallel and conditional execution paths

**Core Features:**
- Dependency management between components
- Serial and parallel execution patterns
- Data flow orchestration
- Error handling and recovery

```python
from forgen.pipeline import PipelineBuilder

builder = PipelineBuilder()
builder.add_node("preprocessor", preprocessing_tool)
builder.add_node("analyzer", analysis_tool, depends_on=["preprocessor"])
builder.add_node("reporter", report_tool, depends_on=["analyzer"])

pipeline = builder.build()
result = pipeline.execute({"raw_data": data})
```

### 🌐 **AMCP Module** (`forgen/amcp/`)

The AMCP (Agent Module Communication Protocol) module provides standardized interfaces for component discovery, registration, and remote execution.

**Key Components:**
- **`AMCPComponent`**: Structured grouping of modules with metadata
- **`AMCPRegistry`**: Component registration and discovery system
- **`AMCPServer`**: Flask-based server for remote component execution
- **`AMCPClient`**: Client for interacting with remote AMCP servers

**Core Features:**
- Component serialization/deserialization
- Remote execution via HTTP APIs
- Service discovery and registration
- Multi-tenant component management

```python
from forgen.amcp import AMCPComponent, AMCPServer

# Create component
component = AMCPComponent(
    id="finance_tools",
    name="Financial Analysis Tools",
    domain="finance",
    modules=[budget_tool, forecast_tool, risk_analyzer]
)

# Serve via AMCP
server = AMCPServer()
server.register_component(component)
server.run(host="localhost", port=5000)
```

## 🔄 Design Patterns

### Tri-Phase Processing
All components use a consistent **InputPhase → ProcessingPhase → OutputPhase** pattern:

1. **InputPhase**: Validates and preprocesses incoming data
2. **ProcessingPhase**: Performs core operation (computation, generation, etc.)
3. **OutputPhase**: Validates and postprocesses results

### Schema Validation
Enforced input/output schemas ensure data integrity:

```python
# Define schemas
input_schema = {"text": str, "language": str}
output_schema = {"translation": str, "confidence": float}

# Enable strict validation
tool.set_forced_interface(True)
```

### Modular Composition
Components can be nested and composed:

```python
# Agent that uses tools and other agents
agent = GenerativeAgent(
    prompt="Comprehensive data analysis",
    modules=[
        data_preprocessor,     # Tool
        analysis_pipeline,     # Pipeline
        specialist_agent       # Another agent
    ]
)
```

## 📁 Package Structure

```
forgen/
├── agent/              # Autonomous AI agents
│   ├── agent.py       # GenerativeAgent implementation
│   ├── builder.py     # AgentBuilder for construction
│   ├── examples/      # Example implementations
│   └── helper.py      # Utility functions
├── tool/              # Modular processing tools
│   ├── tool.py        # Base Tool class
│   ├── builder.py     # ToolBuilder for construction
│   ├── gen/           # Generative tool utilities
│   └── examples/      # Example tools
├── pipeline/          # Workflow orchestration
│   ├── pipeline.py    # Pipeline implementations
│   ├── builder.py     # PipelineBuilder
│   └── examples/      # Example pipelines
├── amcp/              # Component protocol
│   ├── component.py   # AMCPComponent class
│   ├── registry.py    # Component registry
│   ├── server.py      # AMCP server
│   ├── client.py      # AMCP client
│   └── examples.py    # Usage examples
├── llm/               # LLM interfaces
│   ├── openai_interface/
│   └── anthropic_interface/
├── registry/          # Module registration
├── security/          # Security utilities
└── util/              # Common utilities
```

## 🔌 LLM Integration

Forgen supports multiple LLM providers through unified interfaces:

```python
# OpenAI integration
from forgen.llm.openai_interface import OpenAIInterface

interface = OpenAIInterface(api_key="your_key")
agent = GenerativeAgent(
    prompt="Analyze this data",
    generation_function=interface.generate
)

# Anthropic integration  
from forgen.llm.anthropic_interface import AnthropicInterface

interface = AnthropicInterface(api_key="your_key")
agent = GenerativeAgent(
    prompt="Analyze this data",
    generation_function=interface.generate
)
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t forgen .

# Run with environment variables
docker run -e OPTIONS="--reload" -e WORKERS=2 -p 5000:5000 forgen
```

### AMCP Server
```bash
# Start AMCP server with components
python -m forgen.amcp.cli ./examples --port 8080 --domain "production"
```

## 🧪 Testing

Each module includes comprehensive tests:

```bash
# Test individual modules
python forgen/agent/test.py    # Agent tests
python forgen/tool/test.py     # Tool tests
python forgen/pipeline/test.py # Pipeline tests
python forgen/amcp/test.py     # AMCP tests

# Run all tests
python -m pytest
```

## 📊 Example: Complete Workflow

```python
from forgen.tool import ToolBuilder
from forgen.agent import GenerativeAgent
from forgen.pipeline import PipelineBuilder
from forgen.amcp import AMCPComponent, AMCPServer

# 1. Create tools
data_tool = ToolBuilder("data_processor").build()
analysis_tool = ToolBuilder("analyzer").build()

# 2. Create agent
agent = GenerativeAgent(
    prompt="Provide intelligent analysis",
    modules=[data_tool, analysis_tool]
)

# 3. Create pipeline
pipeline = PipelineBuilder()\
    .add_node("preprocessor", data_tool)\
    .add_node("agent", agent, depends_on=["preprocessor"])\
    .build()

# 4. Create AMCP component
component = AMCPComponent(
    id="analysis_suite",
    name="Data Analysis Suite",
    domain="analytics",
    modules=[pipeline]
)

# 5. Serve via AMCP
server = AMCPServer()
server.register_component(component)
server.run()
```

## 🔧 Configuration

Configure Forgen using environment variables:

```bash
# Default LLM model
DEFAULT_MODEL_NAME=gpt-4

# API keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# AMCP server
FORGEN_API_KEY=your_master_key
```

## 📖 Documentation

- **Agent Guide**: `forgen/agent/README.md`
- **Tool Guide**: `forgen/tool/README.md` 
- **Pipeline Guide**: `forgen/pipeline/README.md`
- **AMCP Guide**: `forgen/amcp/README.md`
- **API Docs**: `docs/` (Sphinx format)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**ForGen AI** - *Building the future of modular AI applications*