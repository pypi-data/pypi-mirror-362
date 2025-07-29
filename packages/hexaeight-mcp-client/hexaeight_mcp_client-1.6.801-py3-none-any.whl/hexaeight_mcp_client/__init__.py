"""
Enhanced HexaEight MCP Client
Framework-agnostic MCP integration for HexaEight agents with full coordination capabilities
"""

__version__ = "1.0.0"
__author__ = "HexaEight"
__license__ = "MIT"

# Core exports
from .client import (
    HexaEightMCPClient,
    HexaEightLLMAgent,
    HexaEightToolAgent,
    HexaEightUserAgent,
    HexaEightAgentConfig,
    ToolResult,
    CapabilityDiscoverySystem,
    MessageTracker,
    CapabilityInfo,
    AgentTypeStr,
    FrameworkStr
)

from .agent_manager import (
    HexaEightAgentManager,
    HexaEightAutoConfig,
    AgentCreationResult,
    LegacyAgentCreator,
    LLMConfigProtector,
    # Simple developer API functions
    quick_autogen_llm,
    quick_crewai_llm,
    quick_langchain_llm,
    quick_tool_agent,
    quick_user_agent
)

from .adapters import (
    BaseAdapter,
    AutogenAdapter,
    CrewAIAdapter,
    LangChainAdapter,
    GenericFrameworkAdapter,
    FrameworkDetector,
    create_adapter_for_framework,
    auto_detect_and_create_adapter,
    # Enhanced convenience functions
    create_autogen_agent_with_hexaeight,
    create_crewai_agent_with_hexaeight
)

from .exceptions import (
    HexaEightMCPError,
    MCPConnectionError,
    MCPToolError,
    AgentCreationError,
    DotnetScriptError,
    # Enhanced exceptions
    VerificationError,
    AgentTypeMismatchError,
    ConfigurationError,
    PasswordRequiredError,
    ServiceFormatError,
    BroadcastHandlingError,
    CapabilityDiscoveryError,
    MessageLockError,
    TaskCoordinationError
)

# All exports for external use
__all__ = [
    # Core classes
    "HexaEightMCPClient",
    "HexaEightLLMAgent", 
    "HexaEightToolAgent",
    "HexaEightUserAgent",
    "HexaEightAgentConfig",
    "ToolResult",
    "CapabilityDiscoverySystem",
    "MessageTracker",
    "CapabilityInfo",
    
    # Type definitions
    "AgentTypeStr",
    "FrameworkStr",
    
    # Agent management
    "HexaEightAgentManager",
    "HexaEightAutoConfig", 
    "AgentCreationResult",
    "LegacyAgentCreator",
    "LLMConfigProtector",
    
    # Framework adapters
    "BaseAdapter",
    "AutogenAdapter",
    "CrewAIAdapter",
    "LangChainAdapter", 
    "GenericFrameworkAdapter",
    "FrameworkDetector",
    "create_adapter_for_framework",
    "auto_detect_and_create_adapter",
    
    # Enhanced convenience functions
    "create_autogen_agent_with_hexaeight",
    "create_crewai_agent_with_hexaeight",
    
    # Simple developer API functions
    "quick_autogen_llm",
    "quick_crewai_llm", 
    "quick_langchain_llm",
    "quick_tool_agent",
    "quick_user_agent",
    
    # Exceptions
    "HexaEightMCPError",
    "MCPConnectionError",
    "MCPToolError", 
    "AgentCreationError",
    "DotnetScriptError",
    "VerificationError",
    "AgentTypeMismatchError",
    "ConfigurationError",
    "PasswordRequiredError", 
    "ServiceFormatError",
    "BroadcastHandlingError",
    "CapabilityDiscoveryError",
    "MessageLockError",
    "TaskCoordinationError"
]

def get_version():
    """Get package version"""
    return __version__

def check_requirements():
    """Check if required dependencies are available"""
    try:
        import hexaeight_agent
        return True, f"hexaeight-agent available: {getattr(hexaeight_agent, '__version__', 'unknown')}"
    except ImportError:
        return False, "hexaeight-agent required: pip install hexaeight-agent"

def print_package_info():
    """Print package information and available features"""
    print(f"🔧 HexaEight MCP Client v{__version__}")
    print("=" * 50)
    
    # Check core requirements
    has_hexaeight, hexaeight_info = check_requirements()
    print(f"Core Dependencies:")
    print(f"  hexaeight-agent: {'✅' if has_hexaeight else '❌'} {hexaeight_info}")
    
    # Check framework availability
    print(f"\nFramework Support:")
    from .adapters import FrameworkDetector
    frameworks = FrameworkDetector.detect_available_frameworks()
    
    for framework, available in frameworks.items():
        status = "✅ Available" if available else "❌ Not installed"
        print(f"  {framework.ljust(15)}: {status}")
    
    # Show agent types
    print(f"\nSupported Agent Types:")
    print(f"  LLM Agents      : parentLLM, childLLM")
    print(f"  Tool Agents     : parentTOOL, childTOOL") 
    print(f"  User Agents     : USER")
    print(f"  Legacy Agents   : parent, child")
    
    # Show key features
    print(f"\nKey Features:")
    print(f"  ✅ Auto-configuration and discovery")
    print(f"  ✅ Agent type verification")
    print(f"  ✅ Capability discovery & aggregation")
    print(f"  ✅ Message locking and coordination")
    print(f"  ✅ Task creation and delegation")
    print(f"  ✅ Scheduling and memory")
    print(f"  ✅ Framework integration (AutoGen, CrewAI, LangChain)")
    print(f"  ✅ Broadcast message filtering")
    print(f"  ✅ Tool agent format detection")
    
    print(f"\nQuick Start:")
    print(f"  # AutoGen LLM Agent")
    print(f"  agent = await quick_autogen_llm('parent_config.json')")
    print(f"  ")
    print(f"  # Tool Agent")
    print(f"  tool = await quick_tool_agent('parent_config.json', ['weather_api'])")
    print(f"  ")
    print(f"  # User Agent")
    print(f"  user = await quick_user_agent('user_config.json')")

# Configuration validation helpers
def validate_agent_type(agent_type: str) -> bool:
    """Validate agent type string"""
    valid_types = ["parentLLM", "childLLM", "parentTOOL", "childTOOL", "parent", "child", "USER"]
    return agent_type in valid_types

def validate_framework(framework: str) -> bool:
    """Validate framework string"""
    valid_frameworks = ["autogen", "crewai", "langchain", "generic"]
    return framework in valid_frameworks

def get_agent_type_info(agent_type: str) -> dict:
    """Get information about a specific agent type"""
    agent_info = {
        "parentLLM": {
            "description": "Parent LLM agent with coordination capabilities",
            "verification_required": True,
            "receives_broadcasts": True,
            "can_create_tasks": True,
            "password_required": False
        },
        "childLLM": {
            "description": "Child LLM agent for task execution",
            "verification_required": True,
            "receives_broadcasts": True,
            "can_create_tasks": False,
            "password_required": True
        },
        "parentTOOL": {
            "description": "Parent tool agent providing services",
            "verification_required": False,
            "receives_broadcasts": False,
            "can_create_tasks": False,
            "password_required": False
        },
        "childTOOL": {
            "description": "Child tool agent providing specialized services",
            "verification_required": False,
            "receives_broadcasts": False,
            "can_create_tasks": False,
            "password_required": True
        },
        "USER": {
            "description": "Human user agent for interaction",
            "verification_required": False,
            "receives_broadcasts": False,
            "can_create_tasks": False,
            "password_required": False
        },
        "parent": {
            "description": "Legacy parent agent (backward compatibility)",
            "verification_required": False,
            "receives_broadcasts": False,
            "can_create_tasks": True,
            "password_required": False
        },
        "child": {
            "description": "Legacy child agent (backward compatibility)",
            "verification_required": False,
            "receives_broadcasts": False,
            "can_create_tasks": False,
            "password_required": True
        }
    }
    
    return agent_info.get(agent_type, {"description": "Unknown agent type"})

# Utility functions for developers
def discover_config_files() -> dict:
    """Discover available configuration files in current directory"""
    import os
    import glob
    
    config_files = {
        "parent_configs": [],
        "child_configs": [],
        "general_configs": []
    }
    
    # Look for common config file patterns
    patterns = ["*config*.json", "*.json"]
    
    for pattern in patterns:
        for file_path in glob.glob(pattern):
            filename = os.path.basename(file_path).lower()
            
            if "parent" in filename:
                config_files["parent_configs"].append(file_path)
            elif "child" in filename:
                config_files["child_configs"].append(file_path)
            else:
                config_files["general_configs"].append(file_path)
    
    return config_files

def get_recommended_config_file(agent_type: str) -> str:
    """Get recommended config file name for agent type"""
    if agent_type in ["parent", "parentLLM", "parentTOOL"]:
        return "parent_config.json"
    elif agent_type in ["child", "childLLM", "childTOOL"]:
        return "child_config.json"
    elif agent_type == "USER":
        return "user_config.json"
    else:
        return "config.json"

# Development helpers
def create_example_config(agent_type: str, filename: str = None) -> str:
    """Create an example configuration file for testing"""
    if filename is None:
        filename = get_recommended_config_file(agent_type)
    
    example_config = {
        "agent_type": agent_type,
        "description": f"Example configuration for {agent_type} agent",
        "created_by": "hexaeight-mcp-client",
        "version": __version__,
        "note": "This is an example configuration. Replace with actual values."
    }
    
    try:
        import json
        with open(filename, 'w') as f:
            json.dump(example_config, f, indent=2)
        
        print(f"✅ Created example config file: {filename}")
        print(f"⚠️  Please update with actual configuration values")
        return filename
        
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return ""

def setup_development_environment():
    """Setup development environment with example files"""
    print("🔧 Setting up HexaEight MCP Client development environment...")
    
    # Check requirements
    has_hexaeight, info = check_requirements()
    if not has_hexaeight:
        print(f"❌ {info}")
        return False
    
    # Create example config files
    agent_types = ["parentLLM", "childLLM", "parentTOOL", "childTOOL", "USER"]
    
    for agent_type in agent_types:
        filename = get_recommended_config_file(agent_type)
        if not os.path.exists(filename):
            create_example_config(agent_type, filename)
    
    # Create example environment file
    if not os.path.exists(".env.example"):
        env_content = """# HexaEight MCP Client Environment Variables
HEXAEIGHT_PUBSUB_URL=http://localhost:5000
HEXAEIGHT_CLIENT_ID=your_client_id
HEXAEIGHT_TOKEN_SERVER_URL=https://your-token-server.com
"""
        try:
            with open(".env.example", 'w') as f:
                f.write(env_content)
            print("✅ Created example environment file: .env.example")
        except Exception as e:
            print(f"❌ Failed to create .env.example: {e}")
    
    print("✅ Development environment setup complete!")
    print("\nNext steps:")
    print("1. Update configuration files with actual values")
    print("2. Copy .env.example to .env and update values")
    print("3. Start your PubSub server")
    print("4. Create your first agent:")
    print("   agent = await quick_autogen_llm('parent_config.json')")
    
    return True

# Version compatibility check
def check_compatibility():
    """Check compatibility with hexaeight-agent version"""
    try:
        import hexaeight_agent
        # Add version compatibility checks here if needed
        return True, "Compatible"
    except ImportError:
        return False, "hexaeight-agent not installed"
    except Exception as e:
        return False, f"Compatibility check failed: {e}"
