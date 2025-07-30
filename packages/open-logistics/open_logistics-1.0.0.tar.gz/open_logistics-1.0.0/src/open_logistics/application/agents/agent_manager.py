"""
Agent Manager for OpenAI Agents SDK Integration.

This module provides centralized management of AI agents for the Open Logistics platform,
including lifecycle management, configuration, and monitoring.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from loguru import logger
from pydantic import BaseModel, Field

from open_logistics.core.config import get_settings


class AgentConfig(BaseModel):
    """Configuration for an AI agent."""
    name: str = Field(..., description="Agent name")
    type: str = Field(..., description="Agent type")
    model: str = Field("gpt-4", description="OpenAI model to use")
    temperature: float = Field(0.7, description="Model temperature")
    max_tokens: int = Field(2000, description="Maximum tokens")
    system_prompt: str = Field("", description="System prompt for the agent")
    tools: List[str] = Field(default_factory=list, description="Available tools")
    enabled: bool = Field(True, description="Whether agent is enabled")


class AgentStatus(BaseModel):
    """Status information for an AI agent."""
    name: str
    type: str
    status: str  # "active", "standby", "inactive", "error"
    last_activity: Optional[datetime] = None
    messages_processed: int = 0
    errors: int = 0
    uptime_seconds: float = 0.0


class AgentManager:
    """
    Manages OpenAI Agents SDK integration for the Open Logistics platform.
    
    Provides centralized management of AI agents including:
    - Agent lifecycle management (start, stop, restart)
    - Configuration management
    - Status monitoring and health checks
    - Message routing and processing
    - Error handling and recovery
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.agents: Dict[str, Any] = {}
        self.agent_configs: Dict[str, AgentConfig] = {}
        self.agent_status: Dict[str, AgentStatus] = {}
        self._running = False
        
    async def initialize(self) -> None:
        """Initialize the agent manager and load configurations."""
        logger.info("Initializing OpenAI Agents SDK integration")
        
        # Load agent configurations
        await self._load_agent_configurations()
        
        # Initialize agent status tracking
        for agent_name, config in self.agent_configs.items():
            self.agent_status[agent_name] = AgentStatus(
                name=agent_name,
                type=config.type,
                status="inactive"
            )
        
        self._running = True
        logger.info(f"Agent manager initialized with {len(self.agent_configs)} agents")
    
    async def start_agent(self, agent_name: str, config_override: Optional[Dict[str, Any]] = None) -> bool:
        """Start a specific AI agent."""
        if agent_name not in self.agent_configs:
            logger.error(f"Agent {agent_name} not found in configurations")
            return False
        
        if agent_name in self.agents:
            logger.warning(f"Agent {agent_name} is already running")
            return True
        
        try:
            config = self.agent_configs[agent_name]
            if config_override:
                # Apply configuration overrides
                config = config.model_copy(update=config_override)
            
            # Create and start the agent based on type
            agent = await self._create_agent(config)
            if agent:
                self.agents[agent_name] = agent
                self.agent_status[agent_name].status = "active"
                self.agent_status[agent_name].last_activity = datetime.now()
                
                logger.info(f"Started agent: {agent_name}")
                return True
            else:
                logger.error(f"Failed to create agent: {agent_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting agent {agent_name}: {e}")
            self.agent_status[agent_name].status = "error"
            self.agent_status[agent_name].errors += 1
            return False
    
    async def stop_agent(self, agent_name: str) -> bool:
        """Stop a specific AI agent."""
        if agent_name not in self.agents:
            logger.warning(f"Agent {agent_name} is not running")
            return True
        
        try:
            agent = self.agents[agent_name]
            await self._stop_agent_instance(agent)
            
            del self.agents[agent_name]
            self.agent_status[agent_name].status = "inactive"
            
            logger.info(f"Stopped agent: {agent_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error stopping agent {agent_name}: {e}")
            return False
    
    async def restart_agent(self, agent_name: str) -> bool:
        """Restart a specific AI agent."""
        await self.stop_agent(agent_name)
        return await self.start_agent(agent_name)
    
    async def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, AgentStatus]:
        """Get status information for agents."""
        if agent_name:
            status = self.agent_status.get(agent_name)
            return {agent_name: status} if status else {}
        return self.agent_status.copy()
    
    async def list_agents(self) -> List[Dict[str, Any]]:
        """List all available agents and their configurations."""
        agents = []
        for name, config in self.agent_configs.items():
            status = self.agent_status.get(name)
            agents.append({
                "name": name,
                "type": config.type,
                "status": status.status if status else "unknown",
                "enabled": config.enabled,
                "model": config.model,
                "last_activity": status.last_activity if status else None
            })
        return agents
    
    async def send_message(self, agent_name: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a message to a specific agent for processing."""
        if agent_name not in self.agents:
            return {"error": f"Agent {agent_name} is not running"}
        
        try:
            agent = self.agents[agent_name]
            response = await self._process_agent_message(agent, message, context)
            
            # Update status
            self.agent_status[agent_name].messages_processed += 1
            self.agent_status[agent_name].last_activity = datetime.now()
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message for agent {agent_name}: {e}")
            self.agent_status[agent_name].errors += 1
            return {"error": str(e)}
    
    async def configure_agent(self, agent_name: str, config: Dict[str, Any]) -> bool:
        """Update configuration for a specific agent."""
        if agent_name not in self.agent_configs:
            return False
        
        try:
            # Update configuration
            self.agent_configs[agent_name] = AgentConfig(**config)
            
            # Restart agent if it's running
            if agent_name in self.agents:
                await self.restart_agent(agent_name)
            
            logger.info(f"Updated configuration for agent: {agent_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error configuring agent {agent_name}: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all agents."""
        health_status = {
            "manager_status": "healthy" if self._running else "unhealthy",
            "total_agents": len(self.agent_configs),
            "active_agents": len(self.agents),
            "agent_health": {}
        }
        
        for name, status in self.agent_status.items():
            health_status["agent_health"][name] = {
                "status": status.status,
                "messages_processed": status.messages_processed,
                "errors": status.errors,
                "error_rate": status.errors / max(status.messages_processed, 1),
                "last_activity": status.last_activity
            }
        
        return health_status
    
    async def shutdown(self) -> None:
        """Shutdown the agent manager and all agents."""
        logger.info("Shutting down agent manager")
        
        # Stop all running agents
        for agent_name in list(self.agents.keys()):
            await self.stop_agent(agent_name)
        
        self._running = False
        logger.info("Agent manager shutdown complete")
    
    async def _load_agent_configurations(self) -> None:
        """Load agent configurations from files or defaults."""
        # Default agent configurations
        default_configs = {
                         "supply-chain": AgentConfig(
                 name="supply-chain",
                 type="supply-chain",
                 model="gpt-4",
                 temperature=0.3,
                 max_tokens=2000,
                 system_prompt="You are a supply chain optimization expert. Analyze logistics data and provide optimization recommendations.",
                 tools=["supply_chain_optimizer", "inventory_analyzer", "demand_forecaster"],
                 enabled=True
             ),
             "threat-assessment": AgentConfig(
                 name="threat-assessment",
                 type="threat-assessment",
                 model="gpt-4",
                 temperature=0.2,
                 max_tokens=2000,
                 system_prompt="You are a threat assessment specialist. Analyze security risks and provide mitigation strategies.",
                 tools=["threat_analyzer", "risk_assessor", "security_scanner"],
                 enabled=True
             ),
             "resource-optimizer": AgentConfig(
                 name="resource-optimizer",
                 type="resource-optimizer",
                 model="gpt-4",
                 temperature=0.4,
                 max_tokens=2000,
                 system_prompt="You are a resource optimization expert. Optimize resource allocation and utilization.",
                 tools=["resource_allocator", "capacity_planner", "utilization_optimizer"],
                 enabled=True
             ),
             "mission-coordinator": AgentConfig(
                 name="mission-coordinator",
                 type="mission-coordinator",
                 model="gpt-4",
                 temperature=0.5,
                 max_tokens=2000,
                 system_prompt="You are a mission coordination specialist. Coordinate complex logistics operations.",
                 tools=["mission_planner", "task_coordinator", "status_monitor"],
                 enabled=False
             )
        }
        
        # Load configurations from files if they exist
        config_dir = Path("config/agents")
        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                        agent_name = config_file.stem
                        self.agent_configs[agent_name] = AgentConfig(**config_data)
                except Exception as e:
                    logger.warning(f"Failed to load config from {config_file}: {e}")
        
        # Use defaults for any missing configurations
        for name, config in default_configs.items():
            if name not in self.agent_configs:
                self.agent_configs[name] = config
    
    async def _create_agent(self, config: AgentConfig) -> Optional[Any]:
        """Create an agent instance based on configuration."""
        try:
            # Import the appropriate agent class
            if config.type == "supply-chain":
                from .supply_chain_agent import SupplyChainAgent
                return SupplyChainAgent(config)
            elif config.type == "threat-assessment":
                from .threat_assessment_agent import ThreatAssessmentAgent
                return ThreatAssessmentAgent(config)
            elif config.type == "resource-optimizer":
                from .resource_optimizer_agent import ResourceOptimizerAgent
                return ResourceOptimizerAgent(config)
            elif config.type == "mission-coordinator":
                from .mission_coordinator_agent import MissionCoordinatorAgent
                return MissionCoordinatorAgent(config)
            else:
                logger.error(f"Unknown agent type: {config.type}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to create agent of type {config.type}: {e}")
            return None
    
    async def _stop_agent_instance(self, agent: Any) -> None:
        """Stop a specific agent instance."""
        if hasattr(agent, 'stop'):
            await agent.stop()
    
    async def _process_agent_message(self, agent: Any, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a message through an agent."""
        if hasattr(agent, 'process_message'):
            return await agent.process_message(message, context)
        else:
            return {"error": "Agent does not support message processing"} 