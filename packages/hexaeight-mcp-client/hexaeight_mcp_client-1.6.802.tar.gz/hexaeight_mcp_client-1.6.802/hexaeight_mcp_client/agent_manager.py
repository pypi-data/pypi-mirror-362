"""
Enhanced HexaEight Agent Manager - Creates and manages agents with auto-configuration
"""

import os
import subprocess
import asyncio
import logging
import json
from typing import Dict, List, Optional, Tuple, Union, Literal
from dataclasses import dataclass

try:
    from hexaeight_agent import get_create_scripts_path, HexaEightAgent
except ImportError:
    raise ImportError("hexaeight-agent is required. Install with: pip install hexaeight-agent")

from .client import (
    HexaEightMCPClient, HexaEightLLMAgent, HexaEightToolAgent, HexaEightUserAgent,
    HexaEightAgentConfig, AgentTypeStr, FrameworkStr
)
from .exceptions import (
    AgentCreationError, DotnetScriptError, ConfigurationError, 
    PasswordRequiredError, AgentTypeMismatchError
)

# LLM Configuration Protection
class LLMConfigProtector:
    """
    🔐 LLM Configuration Protection System
    Encrypts and decrypts sensitive LLM configuration data (API keys, endpoints)
    using HexaEight's ProtectMessage and DechipherMessage capabilities
    """
    
    def __init__(self, hexaeight_agent=None):
        self.hexaeight_agent = hexaeight_agent
    
    def protect_llm_config(self, config_data: Dict[str, Any]) -> str:
        """
        Encrypt LLM configuration data for secure local storage
        
        Args:
            config_data: Dictionary containing LLM config (API keys, endpoints, etc.)
            
        Returns:
            Encrypted configuration string
        """
        try:
            if not self.hexaeight_agent:
                raise ConfigurationError("HexaEight agent required for config protection")
            
            # Convert config to JSON string
            config_json = json.dumps(config_data)
            
            # Use HexaEight's ProtectMessage for encryption
            encrypted_config = self.hexaeight_agent.Session.ProtectMessage(config_json)
            
            if not encrypted_config:
                raise ConfigurationError("Failed to encrypt LLM configuration")
            
            logger.info("✅ LLM configuration encrypted successfully")
            return encrypted_config
            
        except Exception as e:
            logger.error(f"❌ Failed to protect LLM config: {e}")
            raise ConfigurationError(f"LLM config protection failed: {e}")
    
    def decipher_llm_config(self, encrypted_config: str) -> Dict[str, Any]:
        """
        Decrypt LLM configuration data from secure storage
        
        Args:
            encrypted_config: Encrypted configuration string
            
        Returns:
            Decrypted configuration dictionary
        """
        try:
            if not self.hexaeight_agent:
                raise ConfigurationError("HexaEight agent required for config decryption")
            
            # Use HexaEight's DechipherMessage for decryption
            decrypted_json = self.hexaeight_agent.Session.DechipherMessage(encrypted_config)
            
            if not decrypted_json:
                raise ConfigurationError("Failed to decrypt LLM configuration")
            
            # Parse JSON back to dictionary
            config_data = json.loads(decrypted_json)
            
            logger.info("✅ LLM configuration decrypted successfully")
            return config_data
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid encrypted config format: {e}")
            raise ConfigurationError(f"Invalid encrypted config format: {e}")
        except Exception as e:
            logger.error(f"❌ Failed to decipher LLM config: {e}")
            raise ConfigurationError(f"LLM config decryption failed: {e}")
    
    def save_protected_config(self, config_data: Dict[str, Any], filename: str = "llm_config.enc") -> str:
        """
        Encrypt and save LLM configuration to file
        
        Args:
            config_data: LLM configuration dictionary
            filename: File to save encrypted config
            
        Returns:
            Path to saved encrypted config file
        """
        try:
            encrypted_config = self.protect_llm_config(config_data)
            
            with open(filename, 'w') as f:
                f.write(encrypted_config)
            
            logger.info(f"✅ Protected LLM config saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Failed to save protected config: {e}")
            raise ConfigurationError(f"Failed to save protected config: {e}")
    
    def load_protected_config(self, filename: str = "llm_config.enc") -> Dict[str, Any]:
        """
        Load and decrypt LLM configuration from file
        
        Args:
            filename: File containing encrypted config
            
        Returns:
            Decrypted configuration dictionary
        """
        try:
            if not os.path.exists(filename):
                raise ConfigurationError(f"Protected config file not found: {filename}")
            
            with open(filename, 'r') as f:
                encrypted_config = f.read().strip()
            
            config_data = self.decipher_llm_config(encrypted_config)
            
            logger.info(f"✅ Protected LLM config loaded from: {filename}")
            return config_data
            
        except Exception as e:
            logger.error(f"❌ Failed to load protected config: {e}")
            raise ConfigurationError(f"Failed to load protected config: {e}")

# Add LLM config protection to existing classes

logger = logging.getLogger(__name__)

@dataclass
class AgentCreationResult:
    """Result of agent creation operation"""
    success: bool
    agent: Optional[Union[HexaEightLLMAgent, HexaEightToolAgent, HexaEightUserAgent]] = None
    agent_name: Optional[str] = None
    agent_type: Optional[str] = None
    config_file: Optional[str] = None
    error: Optional[str] = None
    initialization_time: float = 0.0

class HexaEightAutoConfig:
    """Auto-configuration factory for HexaEight agents with LLM config protection"""
    
    @staticmethod
    def discover_pubsub_url() -> str:
        """Auto-discover PubSub server URL"""
        # Check environment variable first
        pubsub_url = os.environ.get("HEXAEIGHT_PUBSUB_URL")
        if pubsub_url:
            logger.info(f"Found PubSub URL from environment: {pubsub_url}")
            return pubsub_url
        
        # Check for local configuration files
        config_files = [
            "pubsub_config.json",
            "hexaeight_config.json", 
            ".env",
            "config.json"
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        if config_file.endswith('.json'):
                            import json
                            config = json.load(f)
                            if 'pubsub_url' in config:
                                logger.info(f"Found PubSub URL in {config_file}")
                                return config['pubsub_url']
                        else:
                            # Handle .env files
                            for line in f:
                                if line.startswith('HEXAEIGHT_PUBSUB_URL='):
                                    url = line.split('=', 1)[1].strip().strip('"\'')
                                    logger.info(f"Found PubSub URL in {config_file}")
                                    return url
                except Exception as e:
                    logger.warning(f"Error reading {config_file}: {e}")
        
        # Default to localhost
        default_url = "http://localhost:5000"
        logger.info(f"Using default PubSub URL: {default_url}")
        return default_url
    
    @staticmethod
    def validate_config_file(config_file: str, agent_type: AgentTypeStr) -> bool:
        """Validate that config file exists and matches agent type"""
        if not os.path.exists(config_file):
            raise ConfigurationError(f"Configuration file not found: {config_file}")
        
        # Check if config file name matches agent type expectation
        filename = os.path.basename(config_file)
        
        if agent_type in ["parent", "parentLLM", "parentTOOL"]:
            if "child" in filename.lower() and "parent" not in filename.lower():
                logger.warning(f"Using child config file for parent agent type: {agent_type}")
        elif agent_type in ["child", "childLLM", "childTOOL"]:
            if "parent" in filename.lower() and "child" not in filename.lower():
                logger.warning(f"Using parent config file for child agent type: {agent_type}")
        
        return True
    
    @staticmethod
    def create_llm_config_protector(hexaeight_agent) -> LLMConfigProtector:
        """Create LLM configuration protector for encrypting sensitive data"""
        return LLMConfigProtector(hexaeight_agent)
    
    @staticmethod
    async def create_llm_agent_with_protected_config(
        agent_type: Literal["parentLLM", "childLLM", "parent", "child"],
        config_file: str,
        llm_config: Optional[Dict[str, Any]] = None,
        encrypted_llm_config_file: Optional[str] = None,
        password: Optional[str] = None,
        framework: FrameworkStr = "autogen",
        **kwargs
    ) -> 'HexaEightLLMAgent':
        """
        Create LLM agent with encrypted LLM configuration support
        
        Args:
            agent_type: Type of agent to create
            config_file: HexaEight agent configuration file
            llm_config: LLM configuration dict (will be encrypted if provided)
            encrypted_llm_config_file: Path to encrypted LLM config file
            password: Password for child agents
            framework: Framework to use
            **kwargs: Additional configuration
            
        Returns:
            Configured LLM agent with encrypted LLM config support
        """
        
        # First create the basic agent
        agent = await HexaEightAutoConfig.create_llm_agent(
            agent_type=agent_type,
            config_file=config_file,
            password=password,
            framework=framework,
            **kwargs
        )
        
        # Add LLM config protector
        config_protector = HexaEightAutoConfig.create_llm_config_protector(agent.hexaeight_agent)
        agent.llm_config_protector = config_protector
        
        # Handle LLM configuration encryption/decryption
        if llm_config:
            # Encrypt and save new LLM config
            encrypted_file = encrypted_llm_config_file or f"{framework}_llm_config.enc"
            config_protector.save_protected_config(llm_config, encrypted_file)
            agent.encrypted_llm_config_file = encrypted_file
            agent.llm_config = llm_config
            logger.info(f"✅ LLM config encrypted and saved to: {encrypted_file}")
        
        elif encrypted_llm_config_file and os.path.exists(encrypted_llm_config_file):
            # Load existing encrypted LLM config
            agent.llm_config = config_protector.load_protected_config(encrypted_llm_config_file)
            agent.encrypted_llm_config_file = encrypted_llm_config_file
            logger.info(f"✅ LLM config loaded from encrypted file: {encrypted_llm_config_file}")
        
        return agent
    
    @staticmethod
    async def create_llm_agent(
        agent_type: Literal["parentLLM", "childLLM", "parent", "child"],
        config_file: str,
        password: Optional[str] = None,
        framework: FrameworkStr = "autogen",
        client_id: Optional[str] = None,
        token_server_url: Optional[str] = None,
        pubsub_url: Optional[str] = None,
        **kwargs
    ) -> HexaEightLLMAgent:
        """Create and initialize LLM agent with auto-configuration"""
        
        # Validate configuration
        HexaEightAutoConfig.validate_config_file(config_file, agent_type)
        
        # Validate child agent password requirement
        if agent_type in ["child", "childLLM"] and not password:
            raise PasswordRequiredError(f"Password required for child agent type: {agent_type}")
        
        # Auto-discover PubSub URL if not provided
        if not pubsub_url:
            pubsub_url = HexaEightAutoConfig.discover_pubsub_url()
        
        # Create configuration
        config = HexaEightAgentConfig(
            agent_type=agent_type,
            config_file=config_file,
            password=password,
            framework=framework,
            client_id=client_id,
            token_server_url=token_server_url,
            pubsub_url=pubsub_url,
            **kwargs
        )
        
        # Create and initialize agent
        agent = HexaEightLLMAgent(config)
        
        success = await agent.auto_initialize()
        if not success:
            raise AgentCreationError("Failed to initialize LLM agent")
        
        logger.info(f"Successfully created LLM agent: {agent.agent_name} ({agent_type})")
        return agent
    
    @staticmethod
    async def create_tool_agent(
        agent_type: Literal["parentTOOL", "childTOOL"],
        config_file: str,
        service_formats: List[str],
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        token_server_url: Optional[str] = None,
        pubsub_url: Optional[str] = None,
        **kwargs
    ) -> HexaEightToolAgent:
        """Create and initialize tool agent with auto-configuration"""
        
        # Validate configuration
        HexaEightAutoConfig.validate_config_file(config_file, agent_type)
        
        if not service_formats:
            raise ConfigurationError("service_formats required for tool agent")
        
        # Validate child agent password requirement
        if agent_type == "childTOOL" and not password:
            raise PasswordRequiredError(f"Password required for child tool agent")
        
        # Auto-discover PubSub URL if not provided
        if not pubsub_url:
            pubsub_url = HexaEightAutoConfig.discover_pubsub_url()
        
        # Create configuration
        config = HexaEightAgentConfig(
            agent_type=agent_type,
            config_file=config_file,
            password=password,
            service_formats=service_formats,
            client_id=client_id,
            token_server_url=token_server_url,
            pubsub_url=pubsub_url,
            **kwargs
        )
        
        # Create and initialize agent
        agent = HexaEightToolAgent(config)
        
        success = await agent.auto_initialize()
        if not success:
            raise AgentCreationError("Failed to initialize tool agent")
        
        logger.info(f"Successfully created tool agent: {agent.agent_name} ({agent_type})")
        return agent
    
    @staticmethod
    async def create_user_agent(
        config_file: str,
        password: Optional[str] = None,
        client_id: Optional[str] = None,
        token_server_url: Optional[str] = None,
        pubsub_url: Optional[str] = None,
        **kwargs
    ) -> HexaEightUserAgent:
        """Create and initialize user agent with auto-configuration"""
        
        # Validate configuration
        HexaEightAutoConfig.validate_config_file(config_file, "USER")
        
        # Auto-discover PubSub URL if not provided
        if not pubsub_url:
            pubsub_url = HexaEightAutoConfig.discover_pubsub_url()
        
        # Create configuration
        config = HexaEightAgentConfig(
            agent_type="USER",
            config_file=config_file,
            password=password,
            client_id=client_id,
            token_server_url=token_server_url,
            pubsub_url=pubsub_url,
            **kwargs
        )
        
        # Create and initialize agent
        agent = HexaEightUserAgent(config)
        
        success = await agent.auto_initialize()
        if not success:
            raise AgentCreationError("Failed to initialize user agent")
        
        logger.info(f"Successfully created user agent: {agent.agent_name}")
        return agent

class HexaEightAgentManager:
    """
    Enhanced HexaEight agent manager with agent type support
    Manages agent creation using both auto-config and dotnet scripts
    """
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.scripts_path = get_create_scripts_path()
        self.created_agents: Dict[str, Union[HexaEightLLMAgent, HexaEightToolAgent, HexaEightUserAgent]] = {}
        
        # Verify dotnet is available
        self._check_dotnet_availability()
        
        # Verify scripts exist
        self._verify_scripts()
    
    def _check_dotnet_availability(self) -> bool:
        """Check if dotnet is available and working"""
        try:
            result = subprocess.run(
                ["dotnet", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                if self.debug:
                    logger.info(f"✅ .NET available: {result.stdout.strip()}")
                return True
            else:
                raise DotnetScriptError(f"dotnet command failed: {result.stderr}")
                
        except FileNotFoundError:
            raise DotnetScriptError(
                "dotnet command not found. Install .NET SDK: https://dotnet.microsoft.com/download"
            )
        except subprocess.TimeoutExpired:
            raise DotnetScriptError("dotnet command timed out")
    
    def _verify_scripts(self):
        """Verify that required scripts exist"""
        required_scripts = [
            "create_parent_agent.csx",
            "create_child_agent.csx"
        ]
        
        for script in required_scripts:
            script_path = os.path.join(self.scripts_path, script)
            if not os.path.exists(script_path):
                logger.warning(f"Script not found: {script_path}")
    
    async def create_llm_agent_with_config(
        self,
        agent_type: Literal["parentLLM", "childLLM"],
        config_file: str,
        password: Optional[str] = None,
        framework: FrameworkStr = "autogen",
        **kwargs
    ) -> AgentCreationResult:
        """Create LLM agent using existing configuration"""
        import time
        start_time = time.time()
        
        try:
            agent = await HexaEightAutoConfig.create_llm_agent(
                agent_type=agent_type,
                config_file=config_file,
                password=password,
                framework=framework,
                **kwargs
            )
            
            # Store created agent
            self.created_agents[agent.agent_name] = agent
            
            return AgentCreationResult(
                success=True,
                agent=agent,
                agent_name=agent.agent_name,
                agent_type=agent_type,
                config_file=config_file,
                initialization_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Failed to create LLM agent: {e}")
            return AgentCreationResult(
                success=False,
                error=str(e),
                initialization_time=time.time() - start_time
            )
    
    async def create_tool_agent_with_config(
        self,
        agent_type: Literal["parentTOOL", "childTOOL"],
        config_file: str,
        service_formats: List[str],
        password: Optional[str] = None,
        **kwargs
    ) -> AgentCreationResult:
        """Create tool agent using existing configuration"""
        import time
        start_time = time.time()
        
        try:
            agent = await HexaEightAutoConfig.create_tool_agent(
                agent_type=agent_type,
                config_file=config_file,
                service_formats=service_formats,
                password=password,
                **kwargs
            )
            
            # Store created agent
            self.created_agents[agent.agent_name] = agent
            
            return AgentCreationResult(
                success=True,
                agent=agent,
                agent_name=agent.agent_name,
                agent_type=agent_type,
                config_file=config_file,
                initialization_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Failed to create tool agent: {e}")
            return AgentCreationResult(
                success=False,
                error=str(e),
                initialization_time=time.time() - start_time
            )
    
    async def create_user_agent_with_config(
        self,
        config_file: str,
        password: Optional[str] = None,
        **kwargs
    ) -> AgentCreationResult:
        """Create user agent using existing configuration"""
        import time
        start_time = time.time()
        
        try:
            agent = await HexaEightAutoConfig.create_user_agent(
                config_file=config_file,
                password=password,
                **kwargs
            )
            
            # Store created agent
            self.created_agents[agent.agent_name] = agent
            
            return AgentCreationResult(
                success=True,
                agent=agent,
                agent_name=agent.agent_name,
                agent_type="USER",
                config_file=config_file,
                initialization_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Failed to create user agent: {e}")
            return AgentCreationResult(
                success=False,
                error=str(e),
                initialization_time=time.time() - start_time
            )
    
    def get_agent(self, agent_name: str) -> Optional[Union[HexaEightLLMAgent, HexaEightToolAgent, HexaEightUserAgent]]:
        """Get created agent by name"""
        return self.created_agents.get(agent_name)
    
    def list_agents(self) -> Dict[str, str]:
        """List all created agents with their types"""
        return {
            name: agent.config.agent_type 
            for name, agent in self.created_agents.items()
        }
    
    async def shutdown_agent(self, agent_name: str) -> bool:
        """Shutdown and remove agent"""
        agent = self.created_agents.get(agent_name)
        if agent and agent.hexaeight_agent:
            try:
                agent.hexaeight_agent.stop_event_processing()
                agent.hexaeight_agent.disconnect_from_pubsub()
                agent.hexaeight_agent.dispose()
                del self.created_agents[agent_name]
                logger.info(f"Shutdown agent: {agent_name}")
                return True
            except Exception as e:
                logger.error(f"Error shutting down agent {agent_name}: {e}")
                return False
        return False
    
    async def shutdown_all_agents(self):
        """Shutdown all created agents"""
        for agent_name in list(self.created_agents.keys()):
            await self.shutdown_agent(agent_name)

# Simple Developer API Functions

async def quick_autogen_llm(
    config_file: str, 
    agent_type: Literal["parentLLM", "childLLM"] = "parentLLM",
    password: Optional[str] = None,
    **kwargs
) -> HexaEightLLMAgent:
    """Create AutoGen LLM agent with one call"""
    try:
        from .adapters import AutogenAdapter
        
        agent = await HexaEightAutoConfig.create_llm_agent(
            agent_type=agent_type,
            config_file=config_file,
            password=password,
            framework="autogen",
            **kwargs
        )
        
        logger.info(f"Created AutoGen LLM agent: {agent.agent_name}")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create AutoGen LLM agent: {e}")
        raise AgentCreationError(f"AutoGen LLM agent creation failed: {e}")

async def quick_crewai_llm(
    config_file: str,
    agent_type: Literal["parentLLM", "childLLM"] = "parentLLM", 
    password: Optional[str] = None,
    **kwargs
) -> HexaEightLLMAgent:
    """Create CrewAI LLM agent with one call"""
    try:
        agent = await HexaEightAutoConfig.create_llm_agent(
            agent_type=agent_type,
            config_file=config_file,
            password=password,
            framework="crewai",
            **kwargs
        )
        
        logger.info(f"Created CrewAI LLM agent: {agent.agent_name}")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create CrewAI LLM agent: {e}")
        raise AgentCreationError(f"CrewAI LLM agent creation failed: {e}")

async def quick_langchain_llm(
    config_file: str,
    agent_type: Literal["parentLLM", "childLLM"] = "parentLLM",
    password: Optional[str] = None,
    **kwargs
) -> HexaEightLLMAgent:
    """Create LangChain LLM agent with one call"""
    try:
        agent = await HexaEightAutoConfig.create_llm_agent(
            agent_type=agent_type,
            config_file=config_file,
            password=password,
            framework="langchain",
            **kwargs
        )
        
        logger.info(f"Created LangChain LLM agent: {agent.agent_name}")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create LangChain LLM agent: {e}")
        raise AgentCreationError(f"LangChain LLM agent creation failed: {e}")

async def quick_tool_agent(
    config_file: str, 
    service_formats: List[str],
    agent_type: Literal["parentTOOL", "childTOOL"] = "parentTOOL",
    password: Optional[str] = None,
    **kwargs
) -> HexaEightToolAgent:
    """Create tool agent with one call"""
    try:
        agent = await HexaEightAutoConfig.create_tool_agent(
            agent_type=agent_type,
            config_file=config_file,
            service_formats=service_formats,
            password=password,
            **kwargs
        )
        
        logger.info(f"Created tool agent: {agent.agent_name} with formats: {service_formats}")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create tool agent: {e}")
        raise AgentCreationError(f"Tool agent creation failed: {e}")

async def quick_user_agent(
    config_file: str, 
    password: Optional[str] = None,
    **kwargs
) -> HexaEightUserAgent:
    """Create user agent with one call"""
    try:
        agent = await HexaEightAutoConfig.create_user_agent(
            config_file=config_file,
            password=password,
            **kwargs
        )
        
        logger.info(f"Created user agent: {agent.agent_name}")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create user agent: {e}")
        raise AgentCreationError(f"User agent creation failed: {e}")

# Legacy compatibility functions for existing dotnet script functionality
class LegacyAgentCreator:
    """Legacy agent creation using dotnet scripts (for backward compatibility)"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.scripts_path = get_create_scripts_path()
    
    async def create_parent_agent_with_script(
        self, 
        filename: str, 
        client_id: str = "", 
        token_server_url: str = ""
    ) -> AgentCreationResult:
        """Create parent agent using dotnet script"""
        # Implementation for backward compatibility with existing dotnet scripts
        # This can be implemented if needed for specific use cases
        pass
    
    async def create_child_agent_with_script(
        self, 
        agent_password: str, 
        filename: str,
        client_id: str = "", 
        token_server_url: str = ""
    ) -> AgentCreationResult:
        """Create child agent using dotnet script"""
        # Implementation for backward compatibility with existing dotnet scripts
        # This can be implemented if needed for specific use cases
        pass"""
