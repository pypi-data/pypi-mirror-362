# Multi-Agent Debugger

A powerful Python package that uses multiple AI agents to debug API failures by analyzing logs, code, and user questions. Built with CrewAI, it supports LLM providers including OpenAI, Anthropic, Google, Ollama, and more.

## 🎥 Demo Video

Watch the multiagent-debugger in action:

[![Multi-Agent Debugger Demo](https://img.youtube.com/vi/9VTe12iVQ-A/0.jpg)](https://youtu.be/9VTe12iVQ-A?feature=shared)

## 🏗️ Architecture

The Multi-Agent Debugger uses a sophisticated architecture that combines multiple specialized AI agents working together to analyze and debug API failures.

### Core Agent Flow

![Core Agent Flow](docs/assets/architecture_simple.png)

### Detailed Architecture

![Detailed Architecture](docs/assets/architecture.png)

## ✨ Features

### 🤖 Multi-Agent Architecture
- **Question Analyzer Agent**: Extracts key entities from natural language questions and classifies error types
- **Log Analyzer Agent**: Searches and filters logs for relevant information, extracts stack traces
- **Code Path Analyzer Agent**: Validates and analyzes code paths found in logs
- **Code Analyzer Agent**: Finds API handlers, dependencies, and error handling code
- **Root Cause Agent**: Synthesizes findings to determine failure causes and generates visual flowcharts

### 🔧 Comprehensive Analysis Tools
- **Log Analysis**: Enhanced grep, filtering, stack trace extraction, and error pattern analysis
- **Code Analysis**: API handler discovery, dependency mapping, error handler identification, multi-language support
- **Flowchart Generation**: Error flow, system architecture, decision trees, sequence diagrams, and debugging storyboards
- **Natural Language Processing**: Convert user questions into structured queries

### 🌐 Multi-Provider LLM Support
- **OpenAI**
- **Anthropic**
- **Google**
- **Ollama**
- **Azure OpenAI**
- **AWS Bedrock**
- **And 50+ more providers**

### 🎨 Creative Features
- **Storytelling**: Detective-style narratives with metaphors and analogies
- **Visual Flowcharts**: Mermaid diagrams for error propagation and system architecture
- **Copyable Output**: Clean, copyable flowchart code for easy sharing
- **Multi-language Support**: Python, JavaScript, Java, Go, Rust, and more

### 📊 Output Formats
- **Structured JSON**: Programmatic access to analysis results
- **Text Documents**: Human-readable reports saved to local files
- **Visual Flowcharts**: Mermaid diagrams for documentation and sharing

## 🚀 Installation

```bash
# From PyPI
pip install multiagent-debugger

# From source
git clone https://github.com/VishApp/multiagent-debugger.git
cd multiagent-debugger
pip install -e .
```

## ⚡ Quick Start

1. **Set up your configuration:**
```bash
multiagent-debugger setup
```

2. **Debug an API failure:**
```bash
multiagent-debugger debug "Why did my /api/users endpoint fail yesterday?"
```

3. **View generated files:**
- Analysis results in JSON format
- Text documents in current directory
- Visual flowcharts for documentation

## 🖥️ Command-Line Usage

### Debug Command

```
Usage: python -m multiagent_debugger debug [OPTIONS] QUESTION

  Debug an API failure or error scenario with multi-agent assistance.

Arguments:
  QUESTION    The natural language question or debugging prompt.
              Example: 'find the common errors and the root-cause'

Options:
  -c, --config PATH             Path to config file (YAML)
  -v, --verbose                 Enable verbose output for detailed logs
  --mode [frequent|latest|all]  Log analysis mode:
                                  frequent: Find most common error patterns
                                  latest:   Focus on most recent errors
                                  all:      Analyze all available log lines
  --time-window-hours INT       Time window (hours) for log analysis
  --max-lines INT               Maximum log lines to analyze
  -h, --help                    Show this message and exit

Examples:
  multiagent-debugger debug 'find the common errors and the root-cause' \
      --config ~/.config/multiagent-debugger/config.yaml --mode latest

  multiagent-debugger debug 'why did the upload to S3 fail?' \
      --mode frequent --time-window-hours 12
```

This command analyzes your logs, extracts error patterns and code paths, and provides root cause analysis with actionable solutions and flowcharts.

## ⚙️ Configuration

Create a `config.yaml` file (or use the setup command):

```yaml
# Paths to log files
log_paths:
  - "/var/log/myapp/app.log"
  - "/var/log/nginx/access.log"

# Log analysis options
analysis_mode: "frequent"   # frequent, latest, all
time_window_hours: 24      # analyze logs from last N hours
max_lines: 10000           # maximum log lines to analyze

# LLM configuration
llm:
  provider: openai  # or anthropic, google, ollama, etc.
  model_name: gpt-4
  temperature: 0.1
  #api_key: optional, can use environment variable
```

### Custom Providers

The system supports various LLM providers including OpenRouter, Anthropic, Google, and others. See [Custom Providers Guide](docs/CUSTOM_PROVIDERS.md) for detailed configuration instructions.

### Environment Variables

Set the appropriate environment variable for your chosen provider:

- **OpenAI**: `OPENAI_API_KEY`
- **Anthropic**: `ANTHROPIC_API_KEY`
- **Google**: `GOOGLE_API_KEY`
- **Azure**: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`
- **AWS**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- See documentation for other providers

## 🔍 How It Works

### 1. Question Analysis
- Extracts key information like API routes, timestamps, and error types
- Classifies the error type (API, Database, File, Network, etc.)
- Structures the query for other agents

### 2. Log Analysis
- Searches through specified log files using enhanced grep
- Filters relevant log entries by time and pattern
- Extracts stack traces and error patterns
- **Dynamically extracts code paths** (file paths, line numbers, function names)
- Validates code paths found in logs

### 3. Code Analysis
- Locates relevant API handlers and endpoints
- Identifies dependencies and error handlers
- Maps the code structure and relationships
- Supports multiple programming languages (Python, JavaScript, Java, Go, Rust, etc.)

### 4. Root Cause Analysis
- Synthesizes information from all previous agents
- Determines the most likely cause with confidence levels
- Generates creative narratives and metaphors
- Creates visual flowcharts for documentation

### 5. Output Generation
- Structured JSON for programmatic access
- Human-readable text documents
- Visual flowcharts in Mermaid format
- Copyable flowchart code for easy sharing

## 🛠️ Advanced Usage

### List Available Providers
```bash
multiagent-debugger list-providers
```

### List Models for a Provider
```bash
multiagent-debugger list-models openai
```

### Debug with Custom Config
```bash
multiagent-debugger debug "Question?" --config path/to/config.yaml
```

### Analyze Recent Errors Only
```bash
multiagent-debugger debug "What went wrong?" --mode latest --time-window-hours 2
```

### Analyze Large Log Files
```bash
multiagent-debugger debug "Find patterns" --max-lines 50000
```

## 🧪 Development

```bash
# Create virtual environment
python package_builder.py venv

# Install development dependencies
python package_builder.py install

# Run tests
python package_builder.py test

# Build distribution
python package_builder.py dist
```

## 📋 Requirements

- **Python**: 3.8+
- **Dependencies**:
  - crewai>=0.28.0
  - pydantic>=2.0.0
  - And others (see requirements.txt)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🆘 Support

- **GitHub Issues**: [Report a bug](https://github.com/VishApp/multiagent-debugger/issues)
- **Documentation**: [Read more](https://github.com/VishApp/multiagent-debugger#readme)

## 🎯 Use Cases

- **API Debugging**: Quickly identify why API endpoints are failing
- **Production Issues**: Analyze logs and code to find root causes
- **Error Investigation**: Understand complex error chains and dependencies
- **Documentation**: Generate visual flowcharts for error propagation
- **Team Collaboration**: Share analysis results in multiple formats
- **Multi-language Projects**: Support for Python, JavaScript, Java, Go, Rust, and more
- **Time-based Analysis**: Focus on recent errors or specific time periods
- **Large Log Analysis**: Handle massive log files with configurable limits
