# Enhanced MCP Memory

> **⚡ Optimized for Claude Sonnet 4** - This MCP server works best with Claude Sonnet 4 for optimal performance and AI-powered features.

An enhanced MCP (Model Context Protocol) server for intelligent memory and task management, designed for AI assistants and development workflows. Features semantic search, automatic task extraction, knowledge graphs, and comprehensive project management.

## ✨ Key Features

### 🧠 Intelligent Memory Management
- **Semantic search** using sentence-transformers for natural language queries
- **Automatic memory classification** with importance scoring
- **Duplicate detection** and content deduplication
- **File path associations** for code-memory relationships
- **Knowledge graph relationships** with automatic similarity detection

### 📋 Advanced Task Management
- **Auto-task extraction** from conversations and code comments
- **Priority and category management** with validation
- **Status tracking** (pending, in_progress, completed, cancelled)
- **Task-memory relationships** in knowledge graph
- **Project-based organization**

### 🔧 Enterprise Features
- **Performance monitoring** with detailed metrics
- **Health checks** and system diagnostics
- **Automatic cleanup** of old data and duplicates
- **Database optimization** tools
- **Comprehensive logging** and error tracking

### 🚀 Easy Deployment
- **uvx compatible** for one-command installation
- **Zero-configuration** startup with sensible defaults
- **Environment variable** configuration
- **Cross-platform** support (Windows, macOS, Linux)

## 🏗️ Project Structure

```
enhanced-mcp-memory/
├── mcp_server_enhanced.py    # Main MCP server
├── memory_manager.py         # Core memory/task logic
├── database.py              # Database operations
├── requirements.txt         # Python dependencies
├── setup.py                # Package configuration
├── data/                   # SQLite database storage
├── logs/                   # Application logs
└── tests/                  # Test files
```

## 🚀 Quick Start

### Option 1: Using uvx (Recommended)

```bash
# Install and run with uvx
uvx enhanced-mcp-memory
```

### Option 2: Manual Installation

```bash
# Clone and install
git clone https://github.com/cbunting99/enhanced-mcp-memory.git
cd enhanced-mcp-memory
pip install -e .

# Run the server
enhanced-mcp-memory
```

### Option 3: Development Setup

```bash
# Clone repository
git clone https://github.com/cbunting99/enhanced-mcp-memory.git
cd enhanced-mcp-memory

# Install dependencies
pip install -r requirements.txt

# Run directly
python mcp_server_enhanced.py
```

## ⚙️ MCP Configuration

Add to your MCP client configuration:

### For uvx installation:
```json
{
  "mcpServers": {
    "memory-manager": {
      "command": "uvx",
      "args": ["enhanced-mcp-memory"],
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_MEMORY_ITEMS": "1000",
        "ENABLE_AUTO_CLEANUP": "true"
      }
    }
  }
}
```

### For local installation:
```json
{
  "mcpServers": {
    "memory-manager": {
      "command": "python",
      "args": ["mcp_server_enhanced.py"],
      "cwd": "/path/to/enhanced-mcp-memory",
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_MEMORY_ITEMS": "1000",
        "ENABLE_AUTO_CLEANUP": "true"
      }
    }
  }
}
```

## 🛠️ Available Tools

### Core Memory Tools
- `get_memory_context(query)` - Get relevant memories and context
- `create_task(title, description, priority, category)` - Create new tasks
- `get_tasks(status, limit)` - Retrieve tasks with filtering
- `get_project_summary()` - Get comprehensive project overview

### System Management Tools
- `health_check()` - Check server health and connectivity
- `get_performance_stats()` - Get detailed performance metrics
- `cleanup_old_data(days_old)` - Clean up old memories and tasks
- `optimize_memories()` - Remove duplicates and optimize storage
- `get_database_stats()` - Get comprehensive database statistics

## 🔧 Configuration Options

Configure via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_MEMORY_ITEMS` | `1000` | Maximum memories per project |
| `CLEANUP_INTERVAL_HOURS` | `24` | Auto-cleanup interval |
| `ENABLE_AUTO_CLEANUP` | `true` | Enable automatic cleanup |
| `MAX_CONCURRENT_REQUESTS` | `5` | Max concurrent requests |
| `REQUEST_TIMEOUT` | `30` | Request timeout in seconds |

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python test_enhanced_features.py
python test_new_project_system.py
python test_project_tools.py

# Test MCP protocol
python test_mcp_protocol.py
```

## 📊 Performance & Monitoring

The server includes built-in performance tracking:

- **Response time monitoring** for all tools
- **Success rate tracking** with error counts
- **Memory usage statistics**
- **Database performance metrics**
- **Automatic health checks**

Access via the `get_performance_stats()` and `health_check()` tools.

## 🗄️ Database

- **SQLite** for reliable, file-based storage
- **Automatic schema migrations** for updates
- **Comprehensive indexing** for fast queries
- **Built-in backup and optimization** tools
- **Cross-platform compatibility**

Default location: `./data/mcp_memory.db`

## 🔍 Semantic Search

Powered by sentence-transformers for intelligent memory retrieval:

- **Natural language queries** - "Find memories about database optimization"
- **Similarity-based matching** using embeddings
- **Configurable similarity thresholds**
- **Automatic model downloading** (~90MB on first run)

## 📝 Logging

Comprehensive logging system:

- **Daily log rotation** in `./logs/` directory
- **Structured logging** with timestamps and levels
- **Performance tracking** integrated
- **Error tracking** with stack traces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/cbunting99/enhanced-mcp-memory/issues)
- **Documentation**: [README](https://github.com/cbunting99/enhanced-mcp-memory#readme)
- **Discussions**: [GitHub Discussions](https://github.com/cbunting99/enhanced-mcp-memory/discussions)

## 🏷️ Version History

- **v1.2.0** - Enhanced MCP server with performance monitoring and health checks
- **v1.1.0** - Added semantic search and knowledge graph features
- **v1.0.0** - Initial release with basic memory and task management