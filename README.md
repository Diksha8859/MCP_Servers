# MCP Servers - MongoDB & GitHub Integration

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.12.3+-green.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Professional Model Context Protocol (MCP) servers for seamless integration between Claude Desktop and MongoDB databases, plus comprehensive GitHub repository management.

## 🚀 Overview

This repository contains two production-ready MCP servers:

### 🗄️ **MongoDB MCP Server**
- Complete CRUD operations with natural language interface
- Advanced aggregation pipelines and analytics
- Collection management and performance monitoring
- Type-safe operations with comprehensive validation

### 🐙 **GitHub MCP Server** 
- Repository management and code browsing
- Issue tracking and pull request operations
- Advanced search and trending discovery
- User and organization management

## 📁 Project Structure

```
MCP/
├── mcp_server/
│   ├── tools/
│   │   ├── mongodb.py          # MongoDB operations
│   │   └── github_tool.py      # GitHub API integration
│   ├── handlers/
│   │   ├── tool_handler.py     # MongoDB request handling
│   │   └── github_handler.py   # GitHub request handling
│   ├── main.py                 # MongoDB MCP server
│   ├── github_server.py        # GitHub MCP server
│   ├── requirements.txt        # Python dependencies
│   └── docs/                   # Comprehensive documentation
├── .gitignore
└── README.md
```

## 🔧 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB instance (for MongoDB server)
- GitHub Personal Access Token (for GitHub server)
- Claude Desktop application

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mcp-servers.git
   cd mcp-servers
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   cd mcp_server
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your settings
   MONGODB_URI=mongodb://localhost:27017/
   MONGODB_DATABASE=your_database
   GITHUB_TOKEN=your_github_token
   GITHUB_USERNAME=your_username
   ```

### MongoDB Server Setup

1. **Configure Claude Desktop**
   ```json
   {
     "mcpServers": {
       "mongodb-mcp-server": {
         "command": "python",
         "args": ["/path/to/mcp_server/main.py"],
         "env": {
           "MONGODB_URI": "mongodb://localhost:27017/",
           "MONGODB_DATABASE": "your_database"
         }
       }
     }
   }
   ```

2. **Start the server**
   ```bash
   python main.py
   ```

### GitHub Server Setup

1. **Configure Claude Desktop**
   ```json
   {
     "mcpServers": {
       "github-mcp-server": {
         "command": "python",
         "args": ["/path/to/mcp_server/github_server.py"],
         "env": {
           "GITHUB_TOKEN": "your_token",
           "GITHUB_USERNAME": "your_username"
         }
       }
     }
   }
   ```

2. **Start the server**
   ```bash
   python github_server.py
   ```

## 🛠️ Available Tools

### MongoDB Operations
- `mongodb_find` - Query documents with filtering and sorting
- `mongodb_insert` - Insert single or multiple documents
- `mongodb_update` - Update documents with upsert support
- `mongodb_delete` - Delete documents with filtering
- `mongodb_aggregate` - Execute aggregation pipelines
- `mongodb_get_collections` - List all collections
- `mongodb_get_collection_stats` - Get collection statistics

### GitHub Operations
- `github_get_repository_info` - Get repository details
- `github_list_repositories` - List user/org repositories
- `github_get_repository_contents` - Browse files and directories
- `github_list_issues` - List and filter issues
- `github_create_issue` - Create new issues
- `github_search_repositories` - Advanced repository search
- `github_get_user_info` - Get user profile information
- And 6+ more tools for comprehensive GitHub management

## 📚 Documentation

- **[MongoDB MCP Server Documentation](mcp_server/MongoDB_MCP_Documentation.md)** - Complete implementation guide
- **[GitHub MCP Server Documentation](mcp_server/GitHub_MCP_Documentation.md)** - Comprehensive API reference
- **[Implementation Tickets](mcp_server/TICKETS.md)** - Development roadmap and architecture

## 🌟 Features

### MongoDB Server
- ✅ Natural language database queries
- ✅ Advanced aggregation and analytics
- ✅ Real-time performance monitoring
- ✅ Type-safe operations with validation
- ✅ Connection pooling and optimization
- ✅ Comprehensive error handling

### GitHub Server
- ✅ Complete repository management
- ✅ Issue and PR workflow integration
- ✅ Advanced search and discovery
- ✅ Personal and organization operations
- ✅ Rate limiting and authentication
- ✅ Real-time GitHub data access

## 🔒 Security

- Environment-based configuration
- Secure credential management
- Input validation and sanitization
- Rate limiting and error handling
- No hardcoded secrets or tokens

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Usage Examples

### MongoDB Natural Language Queries
```
"Show me all active users created in the last month"
"Calculate average order value by customer segment"
"Find products with low inventory levels"
```

### GitHub Operations
```
"Show me trending Python repositories this week"
"List all open issues in microsoft/vscode with bug labels"
"Get information about the FastAPI repository"
"Create an issue for login bug in my project"
```

## 🚀 Architecture

Both servers follow modern software architecture patterns:

- **Repository Pattern** for data access abstraction
- **Handler Pattern** for request routing and validation  
- **Decorator Pattern** for clean tool registration
- **Strategy Pattern** for different operation types
- **Factory Pattern** for component instantiation

## 📊 Performance

- Async/await for non-blocking operations
- Connection pooling for database efficiency
- Intelligent caching for frequently accessed data
- Rate limiting compliance for API operations
- Memory-efficient processing for large datasets

## 🔧 Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Formatting
```bash
black mcp_server/
```

### Type Checking
```bash
mypy mcp_server/
```

---

**Built with ❤️ for the Claude Desktop and MCP ecosystem**

For support, please open an issue or contact the development team.