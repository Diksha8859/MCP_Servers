# Multi-Platform MCP Server Suite

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.12.3-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI-Integrated Database & GitHub Management Platform**

A comprehensive suite of Model Context Protocol (MCP) servers enabling AI language models to interact with MongoDB databases and GitHub repositories through natural language commands. Built using FastMCP framework for seamless integration with Claude Desktop and other AI platforms.

## 🚀 Features

### MongoDB MCP Server
- **Database Operations**: Full CRUD operations with natural language queries
- **Aggregation Pipelines**: Complex data analysis through conversational AI
- **Collection Management**: Create, list, and manage MongoDB collections
- **Real-time Statistics**: Collection stats and database insights
- **Document Operations**: Insert, update, delete with flexible filtering

### GitHub MCP Server
- **Repository Management**: Create, clone, and manage repositories
- **Issue & PR Operations**: Automated issue tracking and pull request management
- **File Operations**: Read, create, update, delete files directly through AI
- **Branch Management**: Create, switch, merge branches
- **Release Management**: Create and manage releases and tags
- **Organization Tools**: User and organization management

## 🛠️ Technologies

- **Backend**: Python 3.10, FastMCP Framework
- **Database**: MongoDB, PyMongo
- **APIs**: GitHub REST API v3, MCP Protocol 1.12.3
- **AI Integration**: Claude Desktop, Natural Language Processing
- **Development**: AsyncIO, Environment Management, Comprehensive Logging

## 📦 Installation

### Prerequisites
- Python 3.10+
- MongoDB (running locally or remote)
- GitHub Personal Access Token
- Claude Desktop (for AI integration)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Diksha8859/MCP_Servers.git
cd MCP_Servers
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r mcp_server/requirements.txt
```

4. **Configure environment variables**
```bash
cd mcp_server
cp env.example .env
# Edit .env with your credentials
```

### Environment Variables

Create a `.env` file in the `mcp_server` directory:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=your_database_name
MONGODB_COLLECTION=your_collection_name

# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USERNAME=your_github_username

# MCP Server Configuration
MCP_SERVER_NAME=mcp-servers-suite
```

## 🔧 Usage

### MongoDB Server

```bash
cd mcp_server
python mongodb_server.py
```

### GitHub Server

```bash
cd mcp_server
python github_server.py
```

### Claude Desktop Integration

1. **Open Claude Desktop**
2. **Go to Settings → MCP Servers**
3. **Add Server Configuration:**

**For MongoDB:**
- Name: `mongodb-mcp-server`
- Command: `/path/to/venv/bin/python`
- Arguments: `["/path/to/MCP_Servers/mcp_server/mongodb_server.py"]`
- Working Directory: `/path/to/MCP_Servers/mcp_server`

**For GitHub:**
- Name: `github-mcp-server`
- Command: `/path/to/venv/bin/python`
- Arguments: `["/path/to/MCP_Servers/mcp_server/github_server.py"]`
- Working Directory: `/path/to/MCP_Servers/mcp_server`

## 💬 Example Conversations

### MongoDB Operations
```
User: "What collections are in my database?"
Claude: [Lists all MongoDB collections]

User: "Find all users older than 25"
Claude: [Executes MongoDB query and returns results]

User: "Create a new user with name John and age 30"
Claude: [Inserts document into users collection]
```

### GitHub Operations
```
User: "Show me information about my latest repository"
Claude: [Displays repository details, stats, and metadata]

User: "Create a new issue titled 'Bug Fix' in my project repo"
Claude: [Creates new GitHub issue]

User: "List all open pull requests"
Claude: [Shows all open PRs with details]
```

## 📁 Project Structure

```
MCP_Servers/
├── mcp_server/
│   ├── mongodb_server.py          # MongoDB MCP Server
│   ├── github_server.py           # GitHub MCP Server
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Environment variables
│   ├── tools/
│   │   ├── mongodb.py             # MongoDB operations
│   │   └── github_tool.py         # GitHub API integration
│   ├── handlers/
│   │   ├── tool_handler.py        # Tool execution handlers
│   │   └── github_handler.py      # GitHub-specific handlers
│   ├── claude_config.json         # Claude Desktop configuration
│   ├── github_config.json         # GitHub server configuration
│   └── documentation/
│       ├── MongoDB_MCP_Server_Documentation.pdf
│       └── GitHub_MCP_Server_Documentation.docx
├── venv/                          # Virtual environment
├── README.md                      # This file
└── .gitignore                     # Git ignore rules
```

## 🔒 Security

- **Environment Variables**: Store sensitive data in `.env` files
- **GitHub Token**: Use GitHub Personal Access Tokens with minimal required permissions
- **MongoDB**: Configure proper authentication for production use
- **Network**: Restrict database and API access in production environments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP framework
- [Anthropic](https://www.anthropic.com/) for Claude Desktop integration
- [MongoDB](https://www.mongodb.com/) for database capabilities
- [GitHub](https://github.com/) for repository management APIs

## 📞 Contact

**Diksha** - [@Diksha8859](https://github.com/Diksha8859)

Project Link: [https://github.com/Diksha8859/MCP_Servers](https://github.com/Diksha8859/MCP_Servers)

---

⭐ **Star this repository if you find it helpful!**