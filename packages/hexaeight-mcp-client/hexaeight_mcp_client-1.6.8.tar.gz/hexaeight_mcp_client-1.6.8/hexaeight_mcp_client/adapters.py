"""
Enhanced framework adapters with agent type awareness and capability discovery
"""

import asyncio
import json
import inspect
import concurrent.futures
from typing import Dict, List, Any, Optional, Callable, Union, Type
from abc import ABC, abstractmethod

from .client import HexaEightMCPClient, HexaEightLLMAgent, HexaEightToolAgent, ToolResult
from .exceptions import HexaEightMCPError, AgentTypeMismatchError

class BaseAdapter(ABC):
    """Enhanced base adapter for all framework integrations with agent type awareness"""
    
    def __init__(self, agent: Union[HexaEightLLMAgent, HexaEightToolAgent]):
        self.agent = agent
        self.agent_type = agent.config.agent_type if hasattr(agent, 'config') else "unknown"
        self.framework_name = self.__class__.__name__.replace("Adapter", "").lower()
        
        # Validate agent type compatibility
        self._validate_agent_compatibility()
    
    def _validate_agent_compatibility(self):
        """Validate that agent type is compatible with this adapter"""
        # Most adapters expect LLM agents, tool adapters should override this
        if not isinstance(self.agent, HexaEightLLMAgent):
            if not (hasattr(self, 'supports_tool_agents') and self.supports_tool_agents):
                raise AgentTypeMismatchError(
                    f"{self.framework_name} adapter requires LLM agent, got {type(self.agent)}"
                )
    
    @abstractmethod
    def get_tools(self) -> Any:
        """Get tools in framework-specific format"""
        pass
    
    async def get_dynamic_capabilities(self) -> Dict[str, Any]:
        """Get current capabilities including from child agents"""
        if isinstance(self.agent, HexaEightLLMAgent):
            try:
                return await self.agent.capability_discovery.discover_ecosystem_capabilities(timeout=10.0)
            except Exception as e:
                # Return basic capabilities if discovery fails
                return {
                    "llm_capabilities": {
                        "reasoning": True,
                        "coordination": True,
                        "framework": self.framework_name
                    },
                    "tool_capabilities": {},
                    "error": f"Capability discovery failed: {e}"
                }
        return {}

def _run_async_tool(coro):
    """Helper to run async tool in sync context"""
    try:
        # Check if we're already in an event loop
        loop = asyncio.get_running_loop()
        # If we're in a loop, use a thread pool to run the coroutine
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    except RuntimeError:
        # No running loop, create a new one
        return asyncio.run(coro)

class AutogenAdapter(BaseAdapter):
    """Enhanced adapter for Microsoft Autogen framework with capability discovery"""
    
    def __init__(self, llm_agent: HexaEightLLMAgent):
        super().__init__(llm_agent)
        self._autogen_tools = None
        self._last_capability_update = None
        
        # Setup verification response handler
        if isinstance(self.agent, HexaEightLLMAgent):
            self._setup_autogen_verification_responses()
    
    def _setup_autogen_verification_responses(self):
        """Setup AutoGen-specific verification responses"""
        autogen_responses = {
            "capabilities": "I am an AutoGen conversational agent with multi-agent coordination capabilities. "
                          "I can manage conversations, coordinate with other agents, create and manage tasks, "
                          "and integrate with various tools and services through the HexaEight platform.",
            "tools": "I have access to HexaEight coordination tools for messaging, task creation, and agent "
                    "coordination. I can also discover and utilize tools from child agents in my ecosystem.",
            "domain": "I specialize in AutoGen framework integration with multi-agent coordination and "
                     "conversational AI workflows."
        }
        
        self.agent.verification_responses.update(autogen_responses)
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get tools formatted for Autogen with dynamic capability discovery"""
        # Check if we need to refresh capabilities
        current_time = asyncio.get_event_loop().time()
        if (self._autogen_tools is None or 
            self._last_capability_update is None or 
            current_time - self._last_capability_update > 300):  # 5 minutes
            
            self._refresh_autogen_tools()
        
        return self._autogen_tools or []
    
    def _refresh_autogen_tools(self):
        """Refresh AutoGen tools with current capabilities"""
        try:
            self._autogen_tools = []
            
            # Add core HexaEight tools
            for tool_name, tool_schema in self.agent.get_available_tools().items():
                self._autogen_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "description": tool_schema["description"],
                        "parameters": tool_schema["inputSchema"]
                    }
                })
            
            # Add dynamic capability discovery tool
            self._autogen_tools.append({
                "type": "function",
                "function": {
                    "name": "discover_ecosystem_capabilities",
                    "description": "Discover current capabilities from all connected child agents",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timeout": {
                                "type": "number",
                                "description": "Timeout in seconds for capability discovery",
                                "default": 15.0
                            }
                        },
                        "required": []
                    }
                }
            })
            
            self._last_capability_update = asyncio.get_event_loop().time()
            
        except Exception as e:
            # Fallback to basic tools if refresh fails
            self._autogen_tools = []
            for tool_name, tool_schema in self.agent.get_available_tools().items():
                self._autogen_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "description": tool_schema["description"],
                        "parameters": tool_schema["inputSchema"]
                    }
                })
    
    async def execute_tool(self, tool_name: str, **kwargs) -> str:
        """Execute tool and return Autogen-compatible result"""
        if tool_name == "discover_ecosystem_capabilities":
            try:
                capabilities = await self.agent.capability_discovery.discover_ecosystem_capabilities(
                    kwargs.get("timeout", 15.0)
                )
                return json.dumps(capabilities, indent=2)
            except Exception as e:
                return json.dumps({"error": f"Capability discovery failed: {e}"}, indent=2)
        
        result = await self.agent.call_tool(tool_name, **kwargs)
        return json.dumps(result.to_dict(), indent=2)
    
    async def create_conversable_agent(self, name: str = None, 
                                     system_message: str = None,
                                     **autogen_kwargs):
        """Create an Autogen agent with full HexaEight integration"""
        try:
            from autogen import ConversableAgent
        except ImportError:
            raise ImportError("autogen required: pip install pyautogen")
        
        # Use agent name from HexaEight if not provided
        if name is None:
            name = self.agent.agent_name or "HexaEightAutogenAgent"
        
        # Create default system message if not provided
        if system_message is None:
            capabilities = await self.get_dynamic_capabilities()
            tool_count = len(capabilities.get("tool_capabilities", {}))
            
            system_message = (
                f"You are {name}, an AI agent with HexaEight multi-agent coordination capabilities. "
                f"You can coordinate with other agents, create and manage tasks, and access "
                f"{tool_count} specialized tools from child agents. "
                f"Use the available tools to accomplish complex tasks through agent coordination."
            )
        
        class HexaEightAutogenAgent(ConversableAgent):
            def __init__(self, adapter, **kwargs):
                super().__init__(**kwargs)
                self.hexaeight_adapter = adapter
                self._register_hexaeight_tools()
            
            def _register_hexaeight_tools(self):
                """Register HexaEight tools with Autogen"""
                tools = self.hexaeight_adapter.get_tools()
                for tool in tools:
                    function_name = tool["function"]["name"]
                    
                    # Create wrapper function with proper closure
                    def create_tool_wrapper(tool_name):
                        def tool_wrapper(**tool_kwargs):
                            # Use sync version for Autogen
                            coro = self.hexaeight_adapter.execute_tool(tool_name, **tool_kwargs)
                            return _run_async_tool(coro)
                        return tool_wrapper
                    
                    # Register with Autogen
                    self.register_function(
                        function_schema=tool,
                        function=create_tool_wrapper(function_name)
                    )
        
        # Create and return the agent
        autogen_agent = HexaEightAutogenAgent(
            adapter=self,
            name=name,
            system_message=system_message,
            **autogen_kwargs
        )
        
        return autogen_agent
    
    def get_verification_response(self, question: str) -> str:
        """Generate AutoGen-appropriate verification responses"""
        return self.agent.handle_verification_question(question)

class CrewAIAdapter(BaseAdapter):
    """Enhanced adapter for CrewAI framework with capability discovery"""
    
    def __init__(self, llm_agent: HexaEightLLMAgent):
        super().__init__(llm_agent)
        self._crewai_tools = None
        self._last_capability_update = None
        
        # Setup verification response handler
        if isinstance(self.agent, HexaEightLLMAgent):
            self._setup_crewai_verification_responses()
    
    def _setup_crewai_verification_responses(self):
        """Setup CrewAI-specific verification responses"""
        crewai_responses = {
            "capabilities": "I am a CrewAI agent with specialized role-based capabilities and multi-agent "
                          "coordination through the HexaEight platform. I can work in crews, execute tasks, "
                          "and coordinate with other agents to achieve complex goals.",
            "tools": "I have access to HexaEight coordination tools and can discover and utilize specialized "
                    "tools from child agents based on the crew's needs.",
            "domain": "I specialize in CrewAI framework integration with role-based agent coordination and "
                     "collaborative task execution."
        }
        
        self.agent.verification_responses.update(crewai_responses)
    
    def get_tools(self) -> List[Callable]:
        """Get tools formatted for CrewAI with dynamic capability discovery"""
        # Check if we need to refresh capabilities
        current_time = asyncio.get_event_loop().time()
        if (self._crewai_tools is None or 
            self._last_capability_update is None or 
            current_time - self._last_capability_update > 300):  # 5 minutes
            
            self._refresh_crewai_tools()
        
        return self._crewai_tools or []
    
    def _refresh_crewai_tools(self):
        """Refresh CrewAI tools with current capabilities"""
        try:
            self._crewai_tools = []
            
            # Add core HexaEight tools
            for tool_name, tool_schema in self.agent.get_available_tools().items():
                def create_tool_function(name: str, schema: Dict[str, Any]):
                    def tool_function(**kwargs):
                        """CrewAI tool function (synchronous)"""
                        coro = self.agent.call_tool(name, **kwargs)
                        result = _run_async_tool(coro)
                        return json.dumps(result.to_dict(), indent=2)
                    
                    tool_function.__name__ = name
                    tool_function.__doc__ = schema["description"]
                    return tool_function
                
                self._crewai_tools.append(create_tool_function(tool_name, tool_schema))
            
            # Add capability discovery tool
            def discover_ecosystem_capabilities(timeout: float = 15.0):
                """Discover current capabilities from all connected child agents"""
                coro = self.agent.capability_discovery.discover_ecosystem_capabilities(timeout)
                result = _run_async_tool(coro)
                return json.dumps(result, indent=2)
            
            self._crewai_tools.append(discover_ecosystem_capabilities)
            self._last_capability_update = asyncio.get_event_loop().time()
            
        except Exception as e:
            # Fallback to basic tools
            self._crewai_tools = []
            for tool_name, tool_schema in self.agent.get_available_tools().items():
                def create_basic_tool_function(name: str, schema: Dict[str, Any]):
                    def tool_function(**kwargs):
                        coro = self.agent.call_tool(name, **kwargs)
                        result = _run_async_tool(coro)
                        return json.dumps(result.to_dict(), indent=2)
                    
                    tool_function.__name__ = name
                    tool_function.__doc__ = schema["description"]
                    return tool_function
                
                self._crewai_tools.append(create_basic_tool_function(tool_name, tool_schema))
    
    async def create_crew_agent(self, role: str = None, goal: str = None, 
                               backstory: str = None, **crewai_kwargs):
        """Create a CrewAI agent with HexaEight integration"""
        try:
            from crewai import Agent
        except ImportError:
            raise ImportError("crewai required: pip install crewai")
        
        # Use agent name for role if not provided
        if role is None:
            role = self.agent.agent_name or "HexaEight Coordination Agent"
        
        # Create default goal if not provided
        if goal is None:
            capabilities = await self.get_dynamic_capabilities()
            tool_count = len(capabilities.get("tool_capabilities", {}))
            goal = (
                f"Coordinate with other agents and utilize {tool_count} specialized tools "
                f"to accomplish complex tasks through multi-agent collaboration."
            )
        
        # Create default backstory if not provided
        if backstory is None:
            backstory = (
                f"You are an experienced agent in the HexaEight multi-agent ecosystem. "
                f"You have access to coordination tools and can work with specialized child agents "
                f"to accomplish complex tasks that require diverse capabilities."
            )
        
        # Create CrewAI agent with HexaEight tools
        crew_agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=self.get_tools(),
            **crewai_kwargs
        )
        
        return crew_agent
    
    def get_verification_response(self, question: str) -> str:
        """Generate CrewAI-appropriate verification responses"""
        return self.agent.handle_verification_question(question)

class LangChainAdapter(BaseAdapter):
    """Enhanced adapter for LangChain framework with capability discovery"""
    
    def __init__(self, llm_agent: HexaEightLLMAgent):
        super().__init__(llm_agent)
        self._langchain_tools = None
        self._last_capability_update = None
        
        # Setup verification response handler
        if isinstance(self.agent, HexaEightLLMAgent):
            self._setup_langchain_verification_responses()
    
    def _setup_langchain_verification_responses(self):
        """Setup LangChain-specific verification responses"""
        langchain_responses = {
            "capabilities": "I am a LangChain agent with chain-based reasoning capabilities and multi-agent "
                          "coordination through the HexaEight platform. I can create complex reasoning chains, "
                          "coordinate with other agents, and integrate various tools and data sources.",
            "tools": "I have access to HexaEight coordination tools and can discover and chain together "
                    "specialized tools from child agents to create powerful reasoning workflows.",
            "domain": "I specialize in LangChain framework integration with chain-based reasoning and "
                     "multi-agent tool coordination."
        }
        
        self.agent.verification_responses.update(langchain_responses)
    
    def get_tools(self) -> List[Any]:
        """Get tools formatted for LangChain with dynamic capability discovery"""
        # Check if we need to refresh capabilities
        current_time = asyncio.get_event_loop().time()
        if (self._langchain_tools is None or 
            self._last_capability_update is None or 
            current_time - self._last_capability_update > 300):  # 5 minutes
            
            self._refresh_langchain_tools()
        
        return self._langchain_tools or []
    
    def _refresh_langchain_tools(self):
        """Refresh LangChain tools with current capabilities"""
        try:
            from langchain.tools import Tool
            
            self._langchain_tools = []
            
            # Add core HexaEight tools
            for tool_name, tool_schema in self.agent.get_available_tools().items():
                def create_langchain_tool(name: str, schema: Dict[str, Any]):
                    def tool_function(input_str: str):
                        """LangChain tool function"""
                        try:
                            # Parse input if it's JSON
                            if input_str.strip().startswith('{'):
                                kwargs = json.loads(input_str)
                            else:
                                kwargs = {"input": input_str}
                            
                            coro = self.agent.call_tool(name, **kwargs)
                            result = _run_async_tool(coro)
                            return json.dumps(result.to_dict(), indent=2)
                        except Exception as e:
                            return f"Error executing tool: {e}"
                    
                    return Tool(
                        name=name,
                        description=schema["description"],
                        func=tool_function
                    )
                
                self._langchain_tools.append(create_langchain_tool(tool_name, tool_schema))
            
            # Add capability discovery tool
            def capability_discovery_function(timeout_str: str = "15.0"):
                """Discover current capabilities from all connected child agents"""
                try:
                    timeout = float(timeout_str)
                    coro = self.agent.capability_discovery.discover_ecosystem_capabilities(timeout)
                    result = _run_async_tool(coro)
                    return json.dumps(result, indent=2)
                except Exception as e:
                    return f"Capability discovery failed: {e}"
            
            capability_tool = Tool(
                name="discover_ecosystem_capabilities",
                description="Discover current capabilities from all connected child agents",
                func=capability_discovery_function
            )
            
            self._langchain_tools.append(capability_tool)
            self._last_capability_update = asyncio.get_event_loop().time()
            
        except ImportError:
            # LangChain not available, return basic tools
            self._langchain_tools = []
            # Could implement basic tool wrappers here if needed
    
    async def create_langchain_agent(self, **langchain_kwargs):
        """Create a LangChain agent with HexaEight integration"""
        try:
            from langchain.agents import initialize_agent, AgentType
            from langchain.llms.base import LLM
            
            # This would need to be implemented based on specific LangChain requirements
            # For now, return the tools that can be used with LangChain
            return self.get_tools()
            
        except ImportError:
            raise ImportError("langchain required: pip install langchain")
    
    def get_verification_response(self, question: str) -> str:
        """Generate LangChain-appropriate verification responses"""
        return self.agent.handle_verification_question(question)

class GenericFrameworkAdapter(BaseAdapter):
    """Enhanced generic adapter for unknown or custom frameworks"""
    
    def __init__(self, agent: Union[HexaEightLLMAgent, HexaEightToolAgent]):
        super().__init__(agent)
        self.supports_tool_agents = True  # Generic adapter supports both LLM and tool agents
    
    def get_tools(self) -> Dict[str, Any]:
        """Get tools in generic dictionary format"""
        tools = {}
        
        if hasattr(self.agent, 'get_available_tools'):
            tools.update(self.agent.get_available_tools())
        
        # Add capability discovery for LLM agents
        if isinstance(self.agent, HexaEightLLMAgent):
            tools["discover_ecosystem_capabilities"] = {
                "name": "discover_ecosystem_capabilities",
                "description": "Discover current capabilities from all connected child agents",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "timeout": {
                            "type": "number",
                            "description": "Timeout in seconds",
                            "default": 15.0
                        }
                    }
                }
            }
        
        return tools
    
    async def execute_tool(self, tool_name: str, **kwargs) -> ToolResult:
        """Execute tool in generic format"""
        if tool_name == "discover_ecosystem_capabilities" and isinstance(self.agent, HexaEightLLMAgent):
            try:
                capabilities = await self.agent.capability_discovery.discover_ecosystem_capabilities(
                    kwargs.get("timeout", 15.0)
                )
                return ToolResult(True, capabilities)
            except Exception as e:
                return ToolResult(False, None, f"Capability discovery failed: {e}")
        
        return await self.agent.call_tool(tool_name, **kwargs)

class FrameworkDetector:
    """Enhanced framework detection with agent type awareness"""
    
    @staticmethod
    def detect_available_frameworks() -> Dict[str, bool]:
        """Detect which AI frameworks are available"""
        frameworks = {}
        
        try:
            import autogen
            frameworks["autogen"] = True
        except ImportError:
            frameworks["autogen"] = False
        
        try:
            import crewai
            frameworks["crewai"] = True
        except ImportError:
            frameworks["crewai"] = False
        
        try:
            import langchain
            frameworks["langchain"] = True
        except ImportError:
            frameworks["langchain"] = False
        
        try:
            import semantic_kernel
            frameworks["semantic_kernel"] = True
        except ImportError:
            frameworks["semantic_kernel"] = False
        
        return frameworks
    
    @staticmethod
    def get_recommended_adapter(agent: Union[HexaEightLLMAgent, HexaEightToolAgent]):
        """Get recommended adapter based on available frameworks and agent type"""
        if not isinstance(agent, (HexaEightLLMAgent, HexaEightToolAgent)):
            return GenericFrameworkAdapter(agent)
        
        available = FrameworkDetector.detect_available_frameworks()
        
        # For LLM agents, prefer framework-specific adapters
        if isinstance(agent, HexaEightLLMAgent):
            framework = agent.config.framework if hasattr(agent, 'config') else None
            
            if framework == "autogen" and available["autogen"]:
                return AutogenAdapter(agent)
            elif framework == "crewai" and available["crewai"]:
                return CrewAIAdapter(agent)
            elif framework == "langchain" and available["langchain"]:
                return LangChainAdapter(agent)
            elif available["autogen"]:
                return AutogenAdapter(agent)
            elif available["crewai"]:
                return CrewAIAdapter(agent)
            elif available["langchain"]:
                return LangChainAdapter(agent)
        
        # For tool agents or when no specific framework is available
        return GenericFrameworkAdapter(agent)
    
    @staticmethod
    def print_framework_status():
        """Print status of available frameworks"""
        available = FrameworkDetector.detect_available_frameworks()
        
        print("🔍 Framework Detection Results:")
        print("=" * 35)
        
        for framework, is_available in available.items():
            status = "✅ Available" if is_available else "❌ Not installed"
            print(f"{framework.ljust(15)}: {status}")
        
        if not any(available.values()):
            print("\n📦 Install frameworks:")
            print("  pip install pyautogen    # Microsoft Autogen")
            print("  pip install crewai       # CrewAI")
            print("  pip install langchain    # LangChain")

def create_adapter_for_framework(framework_name: str, agent: Union[HexaEightLLMAgent, HexaEightToolAgent]):
    """Factory function to create adapter for specific framework"""
    adapters = {
        "autogen": AutogenAdapter,
        "crewai": CrewAIAdapter,
        "langchain": LangChainAdapter,
        "generic": GenericFrameworkAdapter
    }
    
    if framework_name.lower() not in adapters:
        raise ValueError(f"Unsupported framework: {framework_name}")
    
    adapter_class = adapters[framework_name.lower()]
    
    # Validate agent type for specific adapters
    if framework_name.lower() in ["autogen", "crewai", "langchain"]:
        if not isinstance(agent, HexaEightLLMAgent):
            raise AgentTypeMismatchError(
                f"{framework_name} adapter requires HexaEightLLMAgent, got {type(agent)}"
            )
    
    return adapter_class(agent)

def auto_detect_and_create_adapter(agent: Union[HexaEightLLMAgent, HexaEightToolAgent]):
    """Automatically detect best framework and create adapter"""
    return FrameworkDetector.get_recommended_adapter(agent)

# Enhanced convenience functions for creating framework-specific agents

async def create_autogen_agent_with_hexaeight(
    config_file: str,
    agent_type: str = "parentLLM",
    password: Optional[str] = None,
    name: Optional[str] = None,
    system_message: Optional[str] = None,
    **autogen_kwargs
):
    """Create AutoGen agent with HexaEight integration"""
    from .agent_manager import HexaEightAutoConfig
    
    # Create HexaEight LLM agent
    hexaeight_agent = await HexaEightAutoConfig.create_llm_agent(
        agent_type=agent_type,
        config_file=config_file,
        password=password,
        framework="autogen"
    )
    
    # Create AutoGen adapter and agent
    adapter = AutogenAdapter(hexaeight_agent)
    autogen_agent = await adapter.create_conversable_agent(
        name=name,
        system_message=system_message,
        **autogen_kwargs
    )
    
    return autogen_agent, hexaeight_agent

async def create_crewai_agent_with_hexaeight(
    config_file: str,
    agent_type: str = "parentLLM",
    password: Optional[str] = None,
    role: Optional[str] = None,
    goal: Optional[str] = None,
    backstory: Optional[str] = None,
    **crewai_kwargs
):
    """Create CrewAI agent with HexaEight integration"""
    from .agent_manager import HexaEightAutoConfig
    
    # Create HexaEight LLM agent
    hexaeight_agent = await HexaEightAutoConfig.create_llm_agent(
        agent_type=agent_type,
        config_file=config_file,
        password=password,
        framework="crewai"
    )
    
    # Create CrewAI adapter and agent
    adapter = CrewAIAdapter(hexaeight_agent)
    crewai_agent = await adapter.create_crew_agent(
        role=role,
        goal=goal,
        backstory=backstory,
        **crewai_kwargs
    )
    
    return crewai_agent, hexaeight_agent
