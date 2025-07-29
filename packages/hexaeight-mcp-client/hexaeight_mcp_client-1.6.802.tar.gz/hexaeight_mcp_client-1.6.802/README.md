# HexaEight MCP Client

🚀 **Framework-agnostic MCP integration with secure LLM configuration, automatic multi-agent coordination, and military-grade encryption.**

Build sophisticated multi-agent systems with minimal code while maintaining complete security and framework choice.

## 🌟 Key Features

- 🔐 **Secure LLM Configuration** - Encrypt API keys and endpoints with HexaEight's military-grade encryption
- 🤖 **Framework Integration** - AutoGen, CrewAI, LangChain with encrypted LLM configs  
- 🛠️ **Multi-Agent Types** - LLM agents, Tool agents, User agents with automatic coordination
- 🌐 **Automatic Discovery** - Dynamic capability discovery and intelligent message routing
- 📡 **PubSub Coordination** - Seamless agent communication and task delegation
- ⚡ **One-Line Setup** - From configuration to production-ready agents instantly
- 🎯 **Business Logic** - Write your actual API/database code once in tool agents
- 🔒 **Production Security** - Zero plain-text secrets, secure agent identity management

## 📋 Requirements

### Core Requirements

1. **HexaEight License** 
   - Purchase from [store.hexaeight.com](https://store.hexaeight.com)
   - Install on your development/production machine
   - Enables creation of **1 parent configuration** + **unlimited child configurations**

2. **HexaEight Agentic IAM Server** *(Releasing Soon)*
   - Create CLIENT Application (CLIENTID) 
   - Provisions PubSub server bonded to your CLIENTID
   - Enables seamless agent communication

3. **Python Environment**
   - Python 3.8+
   - .NET SDK (for agent creation)

### Agent Licensing Model

| Agent Type | License Requirement | Expiry Behavior |
|------------|--------------------|-----------------| 
| **Parent Agents** | ✅ Active HexaEight license required | ❌ Stop working when license expires |
| **Child Agents** | ✅ Created with valid license | ✅ Continue working after license expires |

**Note**: All agents (parent and child) are tied to your CLIENT Application (CLIENTID).

## 🚀 Installation

```bash
# Basic installation
pip install hexaeight-mcp-client

# With framework support
pip install hexaeight-mcp-client[autogen]    # For AutoGen
pip install hexaeight-mcp-client[crewai]     # For CrewAI
pip install hexaeight-mcp-client[langchain]  # For LangChain
pip install hexaeight-mcp-client[all]        # All frameworks
```

### Prerequisites

```bash
# Core HexaEight agent package
pip install hexaeight-agent

# Optional: Framework packages
pip install pyautogen  # For AutoGen integration
pip install crewai     # For CrewAI integration  
pip install langchain  # For LangChain integration
```

## 🔐 Secure LLM Configuration

### Encrypt Your LLM Configuration

```python
from hexaeight_mcp_client import HexaEightAutoConfig, quick_autogen_llm

# Your sensitive LLM configuration
llm_config = {
    "provider": "openai",
    "api_key": "sk-your-actual-openai-api-key-here",  # Real API key
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000
}

# Create agent for encryption capabilities
agent = await quick_autogen_llm('parent_config.json')

# Encrypt and protect your configuration
protector = HexaEightAutoConfig.create_llm_config_protector(agent.hexaeight_agent)
protector.save_protected_config(llm_config, "secure_openai.enc")

print("✅ API keys encrypted and secured!")
```

### Supported LLM Providers

| Provider | Configuration Example |
|----------|----------------------|
| **OpenAI** | `{"provider": "openai", "api_key": "sk-...", "model": "gpt-4"}` |
| **Azure OpenAI** | `{"provider": "azure_openai", "api_key": "...", "azure_endpoint": "https://..."}` |
| **Anthropic** | `{"provider": "anthropic", "api_key": "sk-ant-...", "model": "claude-3-sonnet"}` |
| **Local Ollama** | `{"provider": "ollama", "base_url": "http://localhost:11434", "model": "llama2"}` |

## 🤖 Framework Integration with Secure LLM Config

### AutoGen Integration

```python
from hexaeight_mcp_client import HexaEightAutoConfig, create_autogen_agent_with_hexaeight

# Create AutoGen agent with encrypted LLM configuration
autogen_agent, hexaeight_agent = await create_autogen_agent_with_hexaeight(
    config_file="parent_config.json",
    agent_type="parentLLM",
    name="IntelligentCoordinator",
    system_message="You can coordinate with multiple specialized agents and services."
)

# AutoGen agent now has:
# ✅ Encrypted LLM configuration (your API keys secure)
# ✅ HexaEight coordination tools
# ✅ Automatic capability discovery
# ✅ Multi-agent coordination via PubSub
```

### CrewAI Integration

```python
from hexaeight_mcp_client import create_crewai_agent_with_hexaeight

# Create CrewAI agent with encrypted LLM configuration
crewai_agent, hexaeight_agent = await create_crewai_agent_with_hexaeight(
    config_file="parent_config.json",
    agent_type="parentLLM", 
    role="Multi-Agent Coordinator",
    goal="Coordinate complex workflows using available tools and services",
    backstory="Expert in orchestrating multi-agent systems with secure communication"
)

# CrewAI agent now has:
# ✅ Encrypted LLM configuration
# ✅ Role-based coordination capabilities
# ✅ Access to dynamic tool discovery
# ✅ Secure multi-agent communication
```

### LangChain Integration

```python
from hexaeight_mcp_client import HexaEightAutoConfig

# Create LangChain setup with encrypted LLM configuration
hexaeight_agent = await HexaEightAutoConfig.create_llm_agent_with_protected_config(
    agent_type="parentLLM",
    config_file="parent_config.json",
    encrypted_llm_config_file="secure_openai.enc",
    framework="langchain"
)

# Access decrypted LLM config for LangChain
llm_config = hexaeight_agent.llm_config

# Use with LangChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

llm = ChatOpenAI(
    model=llm_config["model"],
    openai_api_key=llm_config["api_key"],  # Securely decrypted
    temperature=llm_config["temperature"]
)

# LangChain agent with HexaEight tools
tools = hexaeight_agent.get_available_tools()
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
```

## 🛠️ Multi-Agent Architecture

### Agent Types

| Agent Type | Purpose | Verification | Broadcasts | Use Case |
|------------|---------|--------------|------------|----------|
| **parentLLM** | LLM coordination | ✅ Required | ✅ Receives all | Main intelligence and coordination |
| **childLLM** | LLM task execution | ✅ Required | ✅ Receives all | Specialized LLM workers |
| **parentTOOL** | Service provision | ❌ Not required | ❌ Ignores broadcasts | API services, databases |
| **childTOOL** | Specialized services | ❌ Not required | ❌ Ignores broadcasts | Specific tool implementations |
| **USER** | Human interaction | ❌ Not required | ❌ Broadcasts to LLMs only | User interfaces |

### Quick Agent Creation

```python
from hexaeight_mcp_client import quick_autogen_llm, quick_tool_agent, quick_user_agent

# LLM Agent (Intelligence Layer)
llm_agent = await quick_autogen_llm(
    config_file="parent_config.json",
    agent_type="parentLLM"
)

# Tool Agent (Business Logic Layer) 
weather_agent = await quick_tool_agent(
    config_file="weather_config.json",
    service_formats=["weather_request", "forecast_request"],
    agent_type="parentTOOL"
)

# User Agent (Interface Layer)
user_agent = await quick_user_agent(
    config_file="user_config.json"
)
```

## 🔧 Implementing Business Logic (Tool Agents)

### Weather Service Example

```python
class WeatherService:
    async def initialize(self):
        # Create tool agent
        self.agent = await quick_tool_agent(
            config_file="weather_config.json",
            service_formats=["weather_request", "location_query"],
            agent_type="parentTOOL"
        )
        
        # Register your business logic
        self.agent.register_service_handler("weather_request", self.handle_weather)
    
    async def handle_weather(self, content, event, tracker):
        """YOUR ACTUAL BUSINESS LOGIC GOES HERE"""
        
        # Parse request
        request = json.loads(content)
        location = request.get("location", "London")
        
        # 🌍 CALL YOUR ACTUAL WEATHER API
        weather_data = await self.call_openweather_api(location)
        
        # Process and enhance data
        enhanced_data = self.process_weather_data(weather_data)
        
        # Send structured response
        response = {
            "type": "weather_response",
            "location": location,
            "data": enhanced_data,
            "processed_by": self.agent.agent_name
        }
        
        await self.agent.hexaeight_agent.publish_to_agent(
            self.agent.pubsub_url,
            "internal_id",
            event.sender_internal_id,
            json.dumps(response),
            "weather_response"
        )
        
        return True
    
    async def call_openweather_api(self, location):
        """Your actual API integration"""
        # Real API call to OpenWeatherMap, WeatherAPI, etc.
        api_key = "your-weather-api-key"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        # ... implement actual API call
        pass
```

### Database Service Example

```python
class DatabaseService:
    async def initialize(self):
        self.agent = await quick_tool_agent(
            config_file="db_config.json",
            service_formats=["database_query", "customer_lookup"],
            agent_type="parentTOOL"
        )
        
        self.agent.register_service_handler("database_query", self.handle_query)
    
    async def handle_query(self, content, event, tracker):
        """YOUR ACTUAL DATABASE LOGIC"""
        
        # Parse database request
        query_data = json.loads(content)
        
        # 🗄️ EXECUTE REAL DATABASE OPERATIONS
        results = await self.execute_sql_query(query_data)
        
        # Send results back
        response = {
            "type": "database_response",
            "results": results,
            "processed_by": self.agent.agent_name
        }
        
        await self.send_response(response, event)
        return True
    
    async def execute_sql_query(self, query_data):
        """Your actual database operations"""
        # Real database connection and queries
        # PostgreSQL, MongoDB, MySQL, etc.
        pass
```

## 🌐 Automatic Coordination & Discovery

### Capability Discovery

```python
# LLM agents automatically discover available tools
llm_agent = await quick_autogen_llm("parent_config.json")

# Discover what services are available
capabilities = await llm_agent.capability_discovery.discover_ecosystem_capabilities()

print("Available Services:")
for service_id, info in capabilities["tool_capabilities"].items():
    service_name = info["capabilities"]["service_name"]
    endpoints = info["capabilities"]["endpoints"]
    print(f"  🔧 {service_name}: {endpoints}")
```

### User Interaction

```python
# User requests are automatically routed to appropriate agents
user_agent = await quick_user_agent("user_config.json")

# This broadcast only reaches LLM agents
await user_agent.broadcast_to_llms("Get me the weather in Tokyo and customer data for account 1001")

# LLM agents will:
# 1. Understand the request
# 2. Discover available weather and database services  
# 3. Coordinate with appropriate tool agents
# 4. Aggregate results and respond to user
```

## 📡 Complete System Example

```python
import asyncio
from hexaeight_mcp_client import *

async def create_intelligent_system():
    """Create a complete multi-agent system"""
    
    # 1. Setup secure LLM configuration
    llm_config = {
        "provider": "openai",
        "api_key": "sk-your-key",
        "model": "gpt-4"
    }
    
    agent = await quick_autogen_llm('parent_config.json')
    protector = HexaEightAutoConfig.create_llm_config_protector(agent.hexaeight_agent)
    protector.save_protected_config(llm_config, "secure_llm.enc")
    
    # 2. Create LLM coordinator with encrypted config
    coordinator = await HexaEightAutoConfig.create_llm_agent_with_protected_config(
        agent_type="parentLLM",
        config_file="parent_config.json",
        encrypted_llm_config_file="secure_llm.enc",
        framework="autogen"
    )
    
    # 3. Create specialized tool agents
    weather_service = await quick_tool_agent(
        "weather_config.json",
        ["weather_request", "forecast_request"],
        "parentTOOL"
    )
    
    database_service = await quick_tool_agent(
        "db_config.json", 
        ["database_query", "customer_lookup"],
        "parentTOOL"
    )
    
    # 4. Create user interface
    user_interface = await quick_user_agent("user_config.json")
    
    # 5. Register business logic with tool agents
    # (Your actual API calls, database operations, etc.)
    
    # 6. System automatically coordinates!
    # - User sends requests to LLM agents
    # - LLM agents discover available tools
    # - Tool agents process specialized requests
    # - Results are coordinated and returned
    
    print("🚀 Intelligent multi-agent system ready!")
    
    # Example user interaction
    await user_interface.broadcast_to_llms(
        "What's the weather in London and show me premium customer data?"
    )

# Run the system
asyncio.run(create_intelligent_system())
```

## 🎯 Use Cases

### Enterprise AI Assistants
- **LLM Agents**: Understand user requests, coordinate responses
- **Tool Agents**: CRM data, financial systems, inventory management
- **User Agents**: Employee interfaces, customer portals

### Data Analysis Platforms  
- **LLM Agents**: Interpret analysis requests, generate insights
- **Tool Agents**: Database queries, API data feeds, visualization
- **User Agents**: Analyst interfaces, report generation

### Customer Service Automation
- **LLM Agents**: Natural language understanding, response generation  
- **Tool Agents**: Ticketing systems, knowledge bases, payment processing
- **User Agents**: Customer chat interfaces, agent dashboards

### IoT and Smart Systems
- **LLM Agents**: Command interpretation, system orchestration
- **Tool Agents**: Device control, sensor data, automation rules
- **User Agents**: Mobile apps, voice interfaces, dashboards

## 🔒 Security Features

- **🔐 API Key Encryption**: Zero plain-text secrets using HexaEight's military-grade encryption
- **🛡️ Secure Agent Identity**: Cryptographic agent authentication and authorization  
- **📡 Encrypted Communication**: All agent messages encrypted via HexaEight PubSub
- **🎯 Message Filtering**: Agents only process relevant messages based on type and format
- **🔍 Capability Isolation**: Tool agents expose only intended service capabilities
- **⚡ Automatic Locking**: Single-attempt message locking prevents processing conflicts

## 📊 Configuration Examples

### Parent Agent Configuration (parent_config.json)
```json
{
  "agent_type": "parentLLM",
  "client_id": "your-client-id",
  "description": "Main LLM coordination agent",
  "framework": "autogen"
}
```

### Tool Agent Configuration (weather_config.json)
```json
{
  "agent_type": "parentTOOL",
  "client_id": "your-client-id", 
  "service_name": "WeatherAPI",
  "description": "Weather data service"
}
```

### Encrypted LLM Configuration (secure_llm.enc)
```
# This file contains encrypted LLM configuration
# Generated by: protector.save_protected_config(llm_config, "secure_llm.enc")
[Encrypted binary data - your API keys are secure!]
```

## 🚀 Getting Started Checklist

- [ ] Purchase HexaEight License from [store.hexaeight.com](https://store.hexaeight.com)
- [ ] Install license on your development machine
- [ ] Create CLIENT Application via HexaEight Agentic IAM Server *(when available)*
- [ ] Install hexaeight-mcp-client: `pip install hexaeight-mcp-client[all]`
- [ ] Create your first LLM configuration and encrypt it
- [ ] Build your first tool agent with actual business logic
- [ ] Test multi-agent coordination
- [ ] Deploy to production with real PubSub server

## 🛠️ Development Tools

```python
from hexaeight_mcp_client import *

# Check package info and framework availability
print_package_info()

# Setup development environment with example configs
setup_development_environment()

# Discover available configuration files
config_files = discover_config_files()
print("Available configs:", config_files)

# Validate agent types and configurations  
is_valid = validate_agent_type("parentLLM")
agent_info = get_agent_type_info("parentLLM")
```

## 📚 API Reference

### Core Classes
- `HexaEightMCPClient` - Base MCP client functionality
- `HexaEightLLMAgent` - LLM agents with coordination capabilities
- `HexaEightToolAgent` - Tool agents for business logic
- `HexaEightUserAgent` - User agents for human interaction
- `LLMConfigProtector` - Encrypt/decrypt LLM configurations

### Framework Adapters
- `AutogenAdapter` - Microsoft AutoGen integration
- `CrewAIAdapter` - CrewAI framework integration  
- `LangChainAdapter` - LangChain framework integration
- `GenericFrameworkAdapter` - Custom framework integration

### Quick Setup Functions
- `quick_autogen_llm()` - Create AutoGen LLM agent
- `quick_crewai_llm()` - Create CrewAI LLM agent
- `quick_tool_agent()` - Create tool agent
- `quick_user_agent()` - Create user agent

## 🆘 Troubleshooting

### Common Issues

**Q: "Failed to encrypt LLM configuration"**  
A: Ensure you have a valid HexaEight agent loaded before creating the config protector.

**Q: "Tool agent not receiving messages"**  
A: Verify your service_formats match the message types being sent by LLM agents.

**Q: "LLM verification failed"**  
A: Make sure your agent_type is "parentLLM" or "childLLM" and provide appropriate verification responses.

**Q: "Connection to PubSub failed"**  
A: Check that your CLIENT Application is properly configured and PubSub server is running.

## 🔗 Links & Resources

- **🏪 HexaEight Store**: [store.hexaeight.com](https://store.hexaeight.com) - Purchase licenses
- **📖 Documentation**: [GitHub Repository](https://github.com/HexaEightTeam/hexaeight-mcp-client)
- **🐛 Issues**: [GitHub Issues](https://github.com/HexaEightTeam/hexaeight-mcp-client/issues)
- **📦 HexaEight Agent**: [hexaeight-agent on PyPI](https://pypi.org/project/hexaeight-agent/)
- **💬 Support**: Contact support for licensing and technical issues

## 📄 License

MIT License - see LICENSE file for details.

---

**🌟 Ready to build intelligent multi-agent systems with enterprise-grade security?**

Start with `pip install hexaeight-mcp-client[all]` and create your first encrypted LLM agent today!
