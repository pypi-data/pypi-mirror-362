"""
Enhanced exceptions for HexaEight MCP Client
"""

class HexaEightMCPError(Exception):
    """Base exception for HexaEight MCP Client"""
    pass

class MCPConnectionError(HexaEightMCPError):
    """Raised when MCP server connection fails"""
    pass

class MCPToolError(HexaEightMCPError):
    """Raised when tool execution fails"""
    pass

class AgentCreationError(HexaEightMCPError):
    """Raised when agent creation fails"""
    pass

class DotnetScriptError(HexaEightMCPError):
    """Raised when dotnet script execution fails"""
    pass

# NEW: Enhanced exception handling for agent types and coordination

class VerificationError(HexaEightMCPError):
    """Raised when LLM verification fails"""
    pass

class AgentTypeMismatchError(HexaEightMCPError):
    """Raised when agent type doesn't match expected behavior"""
    pass

class ConfigurationError(HexaEightMCPError):
    """Raised when agent configuration is invalid"""
    pass

class PasswordRequiredError(ConfigurationError):
    """Raised when password is required for child agent but not provided"""
    pass

class ServiceFormatError(HexaEightMCPError):
    """Raised when service format is not recognized by tool agent"""
    pass

class BroadcastHandlingError(HexaEightMCPError):
    """Raised when broadcast message processing fails"""
    pass

class CapabilityDiscoveryError(HexaEightMCPError):
    """Raised when capability discovery from child agents fails"""
    pass

class MessageLockError(HexaEightMCPError):
    """Raised when message locking fails"""
    pass

class TaskCoordinationError(HexaEightMCPError):
    """Raised when task coordination between agents fails"""
    pass
