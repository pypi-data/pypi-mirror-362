"""
Enhanced HexaEight MCP Client - Complete implementation with agent type support
Framework-agnostic MCP integration for HexaEight agents with coordination capabilities
"""

import asyncio
import json
import logging
import time
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable, Literal, Set
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

try:
    from hexaeight_agent import HexaEightAgent
except ImportError:
    raise ImportError("hexaeight-agent is required. Install with: pip install hexaeight-agent")

from .exceptions import (
    HexaEightMCPError, MCPToolError, VerificationError, AgentTypeMismatchError,
    ConfigurationError, PasswordRequiredError, ServiceFormatError, 
    BroadcastHandlingError, CapabilityDiscoveryError, MessageLockError,
    TaskCoordinationError
)

logger = logging.getLogger(__name__)

# Type definitions
AgentTypeStr = Literal["parentLLM", "childLLM", "parentTOOL", "childTOOL", "parent", "child", "USER"]
FrameworkStr = Literal["autogen", "crewai", "langchain", "generic"]

@dataclass
class ToolResult:
    """Standardized tool execution result"""
    success: bool
    content: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "content": self.content,
            "error": self.error,
            "metadata": self.metadata,
            "execution_time": self.execution_time
        }
    
    def __str__(self) -> str:
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        return f"{status}: {self.content if self.success else self.error}"

@dataclass
class HexaEightAgentConfig:
    """Configuration for HexaEight agents"""
    agent_type: AgentTypeStr
    config_file: str  # parent_config.json or child_config.json
    password: Optional[str] = None  # Required for child agents only
    framework: Optional[FrameworkStr] = "autogen"
    service_formats: Optional[List[str]] = None  # For TOOL agents
    client_id: Optional[str] = None
    token_server_url: Optional[str] = None
    pubsub_url: Optional[str] = None  # Auto-discovered if not provided
    loadenv: bool = True
    logging: bool = False
    
    def __post_init__(self):
        """Validate configuration"""
        # Validate child agent password requirement
        if self.agent_type in ["child", "childLLM", "childTOOL"] and not self.password:
            raise PasswordRequiredError(f"Password required for agent type: {self.agent_type}")
        
        # Validate tool agent service formats
        if "TOOL" in self.agent_type and not self.service_formats:
            raise ConfigurationError(f"service_formats required for TOOL agent type: {self.agent_type}")

@dataclass
class MessageTracker:
    """Track messages and their locking status"""
    message_id: str
    sender: str
    content: Any
    received_at: datetime
    lock_attempted: bool = False
    lock_successful: bool = False
    lock_failed: bool = False
    processed: bool = False
    relevant: bool = True

@dataclass
class CapabilityInfo:
    """Information about agent capabilities"""
    agent_name: str
    agent_type: str
    internal_id: str
    capabilities: Dict[str, Any]
    last_updated: datetime
    
class CapabilityDiscoverySystem:
    """System for discovering and aggregating capabilities from child agents"""
    
    def __init__(self, parent_agent):
        self.parent_agent = parent_agent
        self.child_capabilities: Dict[str, CapabilityInfo] = {}
        self.discovery_timeout = 30.0
        self.cache_ttl = 300  # 5 minutes
        self.pending_discoveries: Dict[str, asyncio.Event] = {}
        
    async def discover_ecosystem_capabilities(self, timeout: float = None) -> Dict[str, Any]:
        """Discover all capabilities from child agents"""
        if timeout is None:
            timeout = self.discovery_timeout
            
        try:
            # Create capability discovery request
            request_id = str(uuid.uuid4())
            discovery_message = {
                "type": "capability_discovery",
                "request_id": request_id,
                "requester": self.parent_agent.hexaeight_agent.get_internal_identity(),
                "response_format": "mcp_tools",
                "timeout": timeout
            }
            
            # Create event for tracking responses
            discovery_event = asyncio.Event()
            self.pending_discoveries[request_id] = discovery_event
            
            # Send discovery message to all child agents
            await self.parent_agent._send_internal_message(
                "capability_discovery", 
                json.dumps(discovery_message)
            )
            
            # Wait for responses or timeout
            try:
                await asyncio.wait_for(discovery_event.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning(f"Capability discovery timed out after {timeout}s")
            
            # Clean up
            self.pending_discoveries.pop(request_id, None)
            
            # Return aggregated capabilities
            return self._aggregate_capabilities()
            
        except Exception as e:
            raise CapabilityDiscoveryError(f"Failed to discover ecosystem capabilities: {e}")
    
    def register_child_capability_response(self, response: Dict[str, Any]):
        """Register capabilities reported by child agent"""
        try:
            request_id = response.get("request_id")
            responder_id = response.get("responder")
            responder_name = response.get("responder_name")
            capabilities = response.get("capabilities", {})
            
            if responder_id:
                capability_info = CapabilityInfo(
                    agent_name=responder_name or "Unknown",
                    agent_type="TOOL",  # Assume tool agent for now
                    internal_id=responder_id,
                    capabilities=capabilities,
                    last_updated=datetime.utcnow()
                )
                
                self.child_capabilities[responder_id] = capability_info
                
                # Signal discovery completion if this was requested
                if request_id in self.pending_discoveries:
                    self.pending_discoveries[request_id].set()
                    
        except Exception as e:
            logger.error(f"Error registering child capability response: {e}")
    
    def _aggregate_capabilities(self) -> Dict[str, Any]:
        """Aggregate all child capabilities into unified format"""
        aggregated = {
            "llm_capabilities": {
                "reasoning": True,
                "coordination": True,
                "task_creation": True,
                "scheduling": True
            },
            "tool_capabilities": {},
            "service_formats": [],
            "last_updated": datetime.utcnow().isoformat()
        }
        
        for child_id, info in self.child_capabilities.items():
            if info.capabilities:
                aggregated["tool_capabilities"][child_id] = {
                    "agent_name": info.agent_name,
                    "capabilities": info.capabilities
                }
                
                # Extract service formats
                if "formats" in info.capabilities:
                    aggregated["service_formats"].extend(info.capabilities["formats"])
        
        return aggregated

class HexaEightMCPClient:
    """
    Enhanced MCP client for HexaEight agents with agent type support
    """
    
    def __init__(self, hexaeight_agent: Optional[HexaEightAgent] = None):
        self.hexaeight_agent = hexaeight_agent
        self.available_tools: Dict[str, Dict[str, Any]] = {}
        self.tool_handlers: Dict[str, Callable] = {}
        self._initialized = False
        self.agent_config: Optional[HexaEightAgentConfig] = None
        self.agent_name: Optional[str] = None
        self.pubsub_url: Optional[str] = None
        
        # Message tracking
        self.message_tracker: Dict[str, MessageTracker] = {}
        self.failed_locks: Set[str] = set()
        self.processed_messages: Set[str] = set()
        
        # Initialize built-in HexaEight tools
        self._register_hexaeight_tools()
    
    def _register_hexaeight_tools(self):
        """Register built-in HexaEight identity and communication tools"""
        hexaeight_tools = {
            "hexaeight_get_identity": {
                "name": "hexaeight_get_identity",
                "description": "Get HexaEight agent identity and capabilities",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "hexaeight_send_message": {
                "name": "hexaeight_send_message", 
                "description": "Send secure message via HexaEight PubSub",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pubsub_url": {"type": "string", "description": "PubSub server URL"},
                        "target_type": {"type": "string", "description": "Target type (agent_name/internal_id)"},
                        "target_value": {"type": "string", "description": "Target identifier"},
                        "message": {"type": "string", "description": "Message content"},
                        "message_type": {"type": "string", "default": "text", "description": "Message type"}
                    },
                    "required": ["pubsub_url", "target_type", "target_value", "message"]
                }
            },
            "hexaeight_create_task": {
                "name": "hexaeight_create_task",
                "description": "Create and assign multi-step task to agents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "pubsub_url": {"type": "string", "description": "PubSub server URL"},
                        "title": {"type": "string", "description": "Task title"},
                        "steps": {"type": "array", "items": {"type": "string"}, "description": "Task steps"},
                        "target_type": {"type": "string", "description": "Target type"},
                        "target_value": {"type": "string", "description": "Target identifier"}
                    },
                    "required": ["pubsub_url", "title", "steps", "target_type", "target_value"]
                }
            }
        }
        
        self.available_tools.update(hexaeight_tools)
        
        # Register handlers
        self.tool_handlers["hexaeight_get_identity"] = self._handle_get_identity
        self.tool_handlers["hexaeight_send_message"] = self._handle_send_message  
        self.tool_handlers["hexaeight_create_task"] = self._handle_create_task
    
    async def _handle_get_identity(self, **kwargs) -> ToolResult:
        """Handle get identity tool"""
        start_time = time.time()
        try:
            if not self.hexaeight_agent:
                return ToolResult(
                    False, None, "No HexaEight agent available",
                    execution_time=time.time() - start_time
                )
            
            agent_name = await self.hexaeight_agent.get_agent_name()
            internal_id = self.hexaeight_agent.get_internal_identity()
            
            identity_info = {
                "agent_name": agent_name,
                "agent_type": self.agent_config.agent_type if self.agent_config else "unknown",
                "internal_id": internal_id[:20] + "..." if len(internal_id) > 20 else internal_id,
                "is_connected_to_pubsub": self.hexaeight_agent.is_connected_to_pubsub(),
                "capabilities": {
                    "can_send_messages": True,
                    "can_create_tasks": True, 
                    "has_secure_identity": bool(internal_id)
                }
            }
            
            return ToolResult(
                True, identity_info,
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                False, None, str(e),
                execution_time=time.time() - start_time
            )
    
    async def _handle_send_message(self, **kwargs) -> ToolResult:
        """Handle send message tool"""
        start_time = time.time()
        try:
            if not self.hexaeight_agent:
                return ToolResult(
                    False, None, "No HexaEight agent available",
                    execution_time=time.time() - start_time
                )
            
            result = await self.hexaeight_agent.publish_to_agent(
                kwargs["pubsub_url"],
                kwargs["target_type"],
                kwargs["target_value"],
                kwargs["message"],
                kwargs.get("message_type", "text")
            )
            
            return ToolResult(
                result,
                {"message_sent": result, "target": f"{kwargs['target_type']}:{kwargs['target_value']}"},
                None if result else "Failed to send message",
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                False, None, str(e),
                execution_time=time.time() - start_time
            )
    
    async def _handle_create_task(self, **kwargs) -> ToolResult:
        """Handle create task tool"""
        start_time = time.time()
        try:
            if not self.hexaeight_agent:
                return ToolResult(
                    False, None, "No HexaEight agent available",
                    execution_time=time.time() - start_time
                )
            
            result = await self.hexaeight_agent.create_and_assign_task(
                kwargs["pubsub_url"],
                kwargs["title"],
                kwargs["steps"],
                kwargs["target_type"],
                kwargs["target_value"]
            )
            
            return ToolResult(
                bool(result),
                {
                    "task_created": bool(result),
                    "task_title": kwargs["title"],
                    "step_count": len(kwargs["steps"]),
                    "assigned_to": f"{kwargs['target_type']}:{kwargs['target_value']}"
                },
                None if result else "Failed to create task",
                execution_time=time.time() - start_time
            )
        except Exception as e:
            return ToolResult(
                False, None, str(e),
                execution_time=time.time() - start_time
            )
    
    async def call_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """Call any available tool (HexaEight or external)"""
        if tool_name not in self.tool_handlers:
            return ToolResult(False, None, f"Tool {tool_name} not found")
        
        try:
            return await self.tool_handlers[tool_name](**kwargs)
        except Exception as e:
            return ToolResult(False, None, f"Tool execution failed: {e}")
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all available tools"""
        return self.available_tools.copy()
    
    def register_tool(self, tool_name: str, tool_schema: Dict[str, Any], 
                     handler: Callable) -> None:
        """Register a new tool"""
        self.available_tools[tool_name] = tool_schema
        self.tool_handlers[tool_name] = handler
    
    async def _send_internal_message(self, message_type: str, content: str) -> bool:
        """Send internal message to ecosystem"""
        if not self.hexaeight_agent or not self.pubsub_url:
            return False
            
        try:
            return await self.hexaeight_agent.publish_broadcast(self.pubsub_url, content)
        except Exception as e:
            logger.error(f"Failed to send internal message: {e}")
            return False

class HexaEightLLMAgent(HexaEightMCPClient):
    """Enhanced LLM agent with full coordination capabilities"""
    
    def __init__(self, config: HexaEightAgentConfig):
        super().__init__()
        self.config = config
        self.agent_config = config
        
        # Validate LLM agent type
        if "LLM" not in config.agent_type and config.agent_type not in ["parent", "child"]:
            raise AgentTypeMismatchError(f"Invalid LLM agent type: {config.agent_type}")
        
        # Initialize coordination systems
        self.capability_discovery = CapabilityDiscoverySystem(self)
        self.active_tasks: Dict[str, Any] = {}
        self.verification_responses: Dict[str, str] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.task_handlers: List[Callable] = []
        
        # Setup default verification responses
        self._setup_default_verification_responses()
    
    def _setup_default_verification_responses(self):
        """Setup default responses for verification questions"""
        framework = self.config.framework or "autogen"
        
        self.verification_responses.update({
            "capabilities": f"I am a {framework} LLM agent with coordination capabilities. "
                          f"I can reason, create tasks, delegate to child agents, schedule actions, "
                          f"and coordinate multi-agent workflows.",
            "tools": f"I have access to HexaEight coordination tools for messaging, task creation, "
                    f"and agent coordination. I can also discover and utilize tools from child agents.",
            "domain": f"I specialize in {framework} framework integration with multi-agent coordination."
        })
    
    async def auto_initialize(self) -> bool:
        """Complete agent initialization with identity resolution"""
        try:
            # Initialize HexaEight agent
            self.hexaeight_agent = HexaEightAgent()
            
            # Load agent configuration
            if self.config.agent_type in ["child", "childLLM"]:
                success = self.hexaeight_agent.load_ai_child_agent(
                    self.config.password,
                    self.config.config_file,
                    self.config.loadenv,
                    self.config.client_id or "",
                    self.config.token_server_url or "",
                    self.config.logging
                )
            else:
                success = self.hexaeight_agent.load_ai_parent_agent(
                    self.config.config_file,
                    self.config.loadenv,
                    self.config.client_id or "",
                    self.config.token_server_url or "",
                    self.config.logging
                )
            
            if not success:
                raise ConfigurationError("Failed to load agent configuration")
            
            # Get agent name from hexaeight_agent
            self.agent_name = await self.hexaeight_agent.get_agent_name()
            if not self.agent_name:
                raise ConfigurationError("Failed to get agent name")
            
            # Auto-discover PubSub URL if not provided
            if not self.config.pubsub_url:
                self.pubsub_url = self._discover_pubsub_url()
            else:
                self.pubsub_url = self.config.pubsub_url
            
            # Connect to PubSub with proper agent type
            connected = await self.hexaeight_agent.connect_to_pubsub(
                self.pubsub_url, 
                self.config.agent_type
            )
            
            if not connected:
                raise MCPConnectionError("Failed to connect to PubSub server")
            
            # Setup event handlers
            self._setup_event_handlers()
            
            # Start event processing
            asyncio.create_task(self.hexaeight_agent.start_event_processing())
            
            # Initial capability discovery for parent agents
            if self.config.agent_type in ["parentLLM", "parent"]:
                asyncio.create_task(self._initial_capability_discovery())
            
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM agent: {e}")
            return False
    
    def _discover_pubsub_url(self) -> str:
        """Auto-discover PubSub server URL"""
        # Check environment variable
        pubsub_url = os.environ.get("HEXAEIGHT_PUBSUB_URL")
        if pubsub_url:
            return pubsub_url
        
        # Default to localhost
        return "http://localhost:5000"
    
    def _setup_event_handlers(self):
        """Setup event handlers for message processing"""
        self.hexaeight_agent.register_event_handler('message_received', self._handle_message_received)
        self.hexaeight_agent.register_event_handler('task_received', self._handle_task_received)
        self.hexaeight_agent.register_event_handler('task_step_received', self._handle_task_step_received)
    
    async def _initial_capability_discovery(self):
        """Perform initial capability discovery"""
        try:
            await asyncio.sleep(2)  # Wait for child agents to connect
            await self.capability_discovery.discover_ecosystem_capabilities()
        except Exception as e:
            logger.warning(f"Initial capability discovery failed: {e}")
    
    async def _handle_message_received(self, event):
        """Handle incoming messages with locking logic"""
        try:
            message_id = event.message_id
            
            # Skip if already processed or lock failed
            if message_id in self.processed_messages or message_id in self.failed_locks:
                return
            
            # Track message
            tracker = MessageTracker(
                message_id=message_id,
                sender=event.sender,
                content=event.decrypted_content,
                received_at=event.timestamp
            )
            self.message_tracker[message_id] = tracker
            
            # Determine if message is relevant
            relevant = await self._is_message_relevant(event)
            tracker.relevant = relevant
            
            if not relevant:
                return
            
            # Attempt to lock message (only once)
            tracker.lock_attempted = True
            locked = await self.hexaeight_agent.lock_message(self.pubsub_url, message_id)
            
            if locked:
                tracker.lock_successful = True
                await self._process_locked_message(event, tracker)
            else:
                tracker.lock_failed = True
                self.failed_locks.add(message_id)
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _is_message_relevant(self, event) -> bool:
        """Determine if message is relevant to this LLM agent"""
        try:
            # Parse message content
            content = event.decrypted_content
            
            # Check for capability discovery requests
            try:
                msg_data = json.loads(content)
                if isinstance(msg_data, dict):
                    if msg_data.get("type") == "capability_discovery":
                        return False  # LLM agents don't respond to capability discovery
                    
                    # Check for capability requests from external systems
                    if "capabilities" in content.lower() or "what can you do" in content.lower():
                        return True
            except:
                pass
            
            # For now, consider all broadcast messages relevant
            # This can be enhanced with more sophisticated relevance detection
            return True
            
        except Exception as e:
            logger.error(f"Error determining message relevance: {e}")
            return False
    
    async def _process_locked_message(self, event, tracker: MessageTracker):
        """Process a successfully locked message"""
        try:
            content = event.decrypted_content
            
            # Check for capability requests
            if "capabilities" in content.lower() or "what can you do" in content.lower():
                await self._handle_capability_request(event, tracker)
                return
            
            # Route to custom handlers
            for handler in self.message_handlers.values():
                try:
                    handled = await handler(event, tracker)
                    if handled:
                        break
                except Exception as e:
                    logger.error(f"Message handler error: {e}")
            
            # Mark as processed
            tracker.processed = True
            self.processed_messages.add(tracker.message_id)
            
            # Release lock
            await self.hexaeight_agent.release_lock(self.pubsub_url, tracker.message_id)
            
        except Exception as e:
            logger.error(f"Error processing locked message: {e}")
            # Release lock on error
            try:
                await self.hexaeight_agent.release_lock(self.pubsub_url, tracker.message_id)
            except:
                pass
    
    async def _handle_capability_request(self, event, tracker: MessageTracker):
        """Handle capability request from external system"""
        try:
            # Discover current ecosystem capabilities
            capabilities = await self.capability_discovery.discover_ecosystem_capabilities(timeout=15.0)
            
            # Format response
            response = {
                "agent_name": self.agent_name,
                "agent_type": self.config.agent_type,
                "capabilities": capabilities,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Send response back to requester
            await self.hexaeight_agent.publish_to_agent(
                self.pubsub_url,
                "internal_id",
                event.sender_internal_id,
                json.dumps(response),
                "capability_response"
            )
            
        except Exception as e:
            logger.error(f"Error handling capability request: {e}")
    
    async def _handle_task_received(self, event):
        """Handle task received events"""
        # Implement task coordination logic
        pass
    
    async def _handle_task_step_received(self, event):
        """Handle task step received events"""
        # Implement task step processing logic
        pass
    
    async def handle_verification_question(self, question: str) -> str:
        """Auto-respond to verification questions based on framework"""
        question_lower = question.lower()
        
        # Check for known question patterns
        if "capabilities" in question_lower or "tools" in question_lower:
            return self.verification_responses["capabilities"]
        elif "domain" in question_lower or "specialize" in question_lower:
            return self.verification_responses["domain"]
        elif "functions" in question_lower:
            return self.verification_responses["tools"]
        
        # Default response
        return f"I am a {self.config.framework} LLM agent capable of reasoning, coordination, and multi-agent task management."
    
    def register_message_handler(self, message_type: str, handler: Callable):
        """Register custom message processing logic"""
        self.message_handlers[message_type] = handler
    
    def register_task_handler(self, handler: Callable):
        """Register custom task processing logic"""
        self.task_handlers.append(handler)

class HexaEightToolAgent(HexaEightMCPClient):
    """Enhanced tool agent with format-specific processing"""
    
    def __init__(self, config: HexaEightAgentConfig):
        super().__init__()
        self.config = config
        self.agent_config = config
        
        # Validate tool agent type
        if "TOOL" not in config.agent_type:
            raise AgentTypeMismatchError(f"Invalid tool agent type: {config.agent_type}")
        
        if not config.service_formats:
            raise ServiceFormatError("service_formats required for tool agent")
        
        self.service_formats = config.service_formats
        self.my_capabilities: Dict[str, Any] = {}
        self.service_handlers: Dict[str, Callable] = {}
        
        # Register default capabilities
        self._register_default_capabilities()
    
    def _register_default_capabilities(self):
        """Register default tool capabilities"""
        self.my_capabilities = {
            "agent_name": "tool_agent",  # Will be updated after initialization
            "service_formats": self.service_formats,
            "tools": [],
            "description": f"Tool agent supporting formats: {', '.join(self.service_formats)}"
        }
    
    async def auto_initialize(self) -> bool:
        """Initialize tool agent (no verification needed)"""
        try:
            # Initialize HexaEight agent
            self.hexaeight_agent = HexaEightAgent()
            
            # Load agent configuration
            if self.config.agent_type == "childTOOL":
                success = self.hexaeight_agent.load_ai_child_agent(
                    self.config.password,
                    self.config.config_file,
                    self.config.loadenv,
                    self.config.client_id or "",
                    self.config.token_server_url or "",
                    self.config.logging
                )
            else:
                success = self.hexaeight_agent.load_ai_parent_agent(
                    self.config.config_file,
                    self.config.loadenv,
                    self.config.client_id or "",
                    self.config.token_server_url or "",
                    self.config.logging
                )
            
            if not success:
                raise ConfigurationError("Failed to load agent configuration")
            
            # Get agent name from hexaeight_agent
            self.agent_name = await self.hexaeight_agent.get_agent_name()
            if not self.agent_name:
                raise ConfigurationError("Failed to get agent name")
            
            # Update capabilities with actual agent name
            self.my_capabilities["agent_name"] = self.agent_name
            
            # Auto-discover PubSub URL if not provided
            if not self.config.pubsub_url:
                self.pubsub_url = self._discover_pubsub_url()
            else:
                self.pubsub_url = self.config.pubsub_url
            
            # Connect to PubSub as TOOL agent (no verification)
            connected = await self.hexaeight_agent.connect_to_pubsub(
                self.pubsub_url, 
                self.config.agent_type
            )
            
            if not connected:
                raise MCPConnectionError("Failed to connect to PubSub server")
            
            # Setup event handlers
            self._setup_event_handlers()
            
            # Start event processing
            asyncio.create_task(self.hexaeight_agent.start_event_processing())
            
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize tool agent: {e}")
            return False
    
    def _discover_pubsub_url(self) -> str:
        """Auto-discover PubSub server URL"""
        pubsub_url = os.environ.get("HEXAEIGHT_PUBSUB_URL")
        if pubsub_url:
            return pubsub_url
        return "http://localhost:5000"
    
    def _setup_event_handlers(self):
        """Setup event handlers for message processing"""
        self.hexaeight_agent.register_event_handler('message_received', self._handle_message_received)
    
    async def _handle_message_received(self, event):
        """Handle incoming messages with format filtering and locking"""
        try:
            message_id = event.message_id
            
            # Skip if already processed or lock failed
            if message_id in self.processed_messages or message_id in self.failed_locks:
                return
            
            # Track message
            tracker = MessageTracker(
                message_id=message_id,
                sender=event.sender,
                content=event.decrypted_content,
                received_at=event.timestamp
            )
            self.message_tracker[message_id] = tracker
            
            # Check if message matches our service formats
            if not self.should_process_message(event.decrypted_content):
                tracker.relevant = False
                return
            
            tracker.relevant = True
            
            # Attempt to lock message (only once)
            tracker.lock_attempted = True
            locked = await self.hexaeight_agent.lock_message(self.pubsub_url, message_id)
            
            if locked:
                tracker.lock_successful = True
                await self._process_tool_request(event, tracker)
            else:
                tracker.lock_failed = True
                self.failed_locks.add(message_id)
                
        except Exception as e:
            logger.error(f"Error handling message in tool agent: {e}")
    
    def should_process_message(self, content: str) -> bool:
        """Check if message matches expected service formats"""
        try:
            # Parse message content
            try:
                msg_data = json.loads(content)
                if isinstance(msg_data, dict):
                    # Check for capability discovery requests
                    if msg_data.get("type") == "capability_discovery":
                        return True
                    
                    # Check message format/type
                    msg_type = msg_data.get("type", "")
                    msg_format = msg_data.get("format", "")
                    
                    # Check if matches our service formats
                    if msg_type in self.service_formats or msg_format in self.service_formats:
                        return True
            except:
                pass
            
            # Check for format keywords in content
            for format_type in self.service_formats:
                if format_type.lower() in content.lower():
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking message format: {e}")
            return False
    
    async def _process_tool_request(self, event, tracker: MessageTracker):
        """Process a tool request after locking"""
        try:
            content = event.decrypted_content
            
            # Handle capability discovery requests
            try:
                msg_data = json.loads(content)
                if isinstance(msg_data, dict) and msg_data.get("type") == "capability_discovery":
                    await self._handle_capability_discovery_request(event, msg_data, tracker)
                    return
            except:
                pass
            
            # Route to service handlers
            for format_type, handler in self.service_handlers.items():
                if format_type.lower() in content.lower():
                    try:
                        result = await handler(content, event, tracker)
                        if result:
                            break
                    except Exception as e:
                        logger.error(f"Service handler error: {e}")
            
            # Mark as processed
            tracker.processed = True
            self.processed_messages.add(tracker.message_id)
            
            # Release lock
            await self.hexaeight_agent.release_lock(self.pubsub_url, tracker.message_id)
            
        except Exception as e:
            logger.error(f"Error processing tool request: {e}")
            # Release lock on error
            try:
                await self.hexaeight_agent.release_lock(self.pubsub_url, tracker.message_id)
            except:
                pass
    
    async def _handle_capability_discovery_request(self, event, request_data: Dict[str, Any], tracker: MessageTracker):
        """Respond to capability discovery from parent LLM"""
        try:
            request_id = request_data.get("request_id")
            requester = request_data.get("requester")
            
            # Format capability response
            response = {
                "type": "capability_response",
                "request_id": request_id,
                "responder": self.hexaeight_agent.get_internal_identity(),
                "responder_name": self.agent_name,
                "capabilities": self.my_capabilities
            }
            
            # Send response back to requester
            await self.hexaeight_agent.publish_to_agent(
                self.pubsub_url,
                "internal_id",
                requester,
                json.dumps(response),
                "capability_response"
            )
            
        except Exception as e:
            logger.error(f"Error handling capability discovery request: {e}")
    
    def register_my_capabilities(self, capabilities: Dict[str, Any]):
        """Register this tool's capabilities"""
        self.my_capabilities.update(capabilities)
    
    def register_service_handler(self, format_type: str, handler: Callable):
        """Register handlers for specific service formats"""
        self.service_handlers[format_type] = handler

class HexaEightUserAgent(HexaEightMCPClient):
    """Enhanced user agent for human interaction"""
    
    def __init__(self, config: HexaEightAgentConfig):
        super().__init__()
        self.config = config
        self.agent_config = config
        
        # Validate user agent type
        if config.agent_type != "USER":
            raise AgentTypeMismatchError(f"Invalid user agent type: {config.agent_type}")
    
    async def auto_initialize(self) -> bool:
        """Initialize user agent"""
        try:
            # Initialize HexaEight agent
            self.hexaeight_agent = HexaEightAgent()
            
            # Load configuration (user agents typically use parent config)
            success = self.hexaeight_agent.load_ai_parent_agent(
                self.config.config_file,
                self.config.loadenv,
                self.config.client_id or "",
                self.config.token_server_url or "",
                self.config.logging
            )
            
            if not success:
                raise ConfigurationError("Failed to load agent configuration")
            
            # Get agent name
            self.agent_name = await self.hexaeight_agent.get_agent_name()
            if not self.agent_name:
                raise ConfigurationError("Failed to get agent name")
            
            # Auto-discover PubSub URL
            if not self.config.pubsub_url:
                self.pubsub_url = self._discover_pubsub_url()
            else:
                self.pubsub_url = self.config.pubsub_url
            
            # Connect as USER (no verification)
            connected = await self.hexaeight_agent.connect_to_pubsub(
                self.pubsub_url, 
                "USER"
            )
            
            if not connected:
                raise MCPConnectionError("Failed to connect to PubSub server")
            
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize user agent: {e}")
            return False
    
    def _discover_pubsub_url(self) -> str:
        """Auto-discover PubSub server URL"""
        pubsub_url = os.environ.get("HEXAEIGHT_PUBSUB_URL")
        if pubsub_url:
            return pubsub_url
        return "http://localhost:5000"
    
    async def broadcast_to_llms(self, message: str) -> bool:
        """Send broadcast that only reaches LLM agents"""
        try:
            if not self.hexaeight_agent or not self.pubsub_url:
                return False
            
            return await self.hexaeight_agent.publish_broadcast(self.pubsub_url, message)
        except Exception as e:
            logger.error(f"Error broadcasting to LLMs: {e}")
            return False
    
    async def request_task_from_llms(self, task_description: str) -> bool:
        """Request task creation from available LLM agents"""
        task_request = {
            "type": "task_request",
            "description": task_description,
            "requester": self.agent_name,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return await self.broadcast_to_llms(json.dumps(task_request))
