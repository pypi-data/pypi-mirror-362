"""
Supply Chain Agent with OpenAI Agents SDK Integration.

This module provides an intelligent agent for supply chain optimization,
leveraging OpenAI's capabilities for analysis and decision-making.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

import openai
from loguru import logger

from open_logistics.core.config import get_settings
from .agent_manager import AgentConfig


class SupplyChainAgent:
    """
    Intelligent supply chain optimization agent powered by OpenAI.
    
    This agent specializes in:
    - Supply chain analysis and optimization
    - Inventory management recommendations
    - Demand forecasting insights
    - Risk assessment and mitigation
    - Cost optimization strategies
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.settings = get_settings()
        self.client = openai.AsyncOpenAI()
        self.running = False
        self.conversation_history: List[Dict[str, Any]] = []
        
        # Initialize system message
        self.system_message = {
            "role": "system",
            "content": config.system_prompt or self._get_default_system_prompt()
        }
        
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for supply chain agent."""
        return """
        You are an expert supply chain optimization agent for the Open Logistics platform.
        
        Your expertise includes:
        - Supply chain analysis and optimization
        - Inventory management and forecasting
        - Demand prediction and planning
        - Risk assessment and mitigation
        - Cost optimization and efficiency improvements
        - Resource allocation and capacity planning
        
        You analyze logistics data and provide actionable recommendations for:
        - Optimizing supply chain operations
        - Reducing costs while maintaining service levels
        - Improving inventory turnover and reducing waste
        - Identifying bottlenecks and inefficiencies
        - Predicting and preventing supply chain disruptions
        
        Always provide specific, actionable recommendations with quantitative metrics when possible.
        Consider both short-term tactical and long-term strategic implications.
        """
    
    async def start(self) -> None:
        """Start the supply chain agent."""
        self.running = True
        logger.info(f"Supply Chain Agent '{self.config.name}' started")
    
    async def stop(self) -> None:
        """Stop the supply chain agent."""
        self.running = False
        logger.info(f"Supply Chain Agent '{self.config.name}' stopped")
    
    async def process_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a message through the supply chain agent.
        
        Args:
            message: The message to process
            context: Additional context for the message
            
        Returns:
            Dictionary containing the agent's response and metadata
        """
        if not self.running:
            return {"error": "Agent is not running"}
        
        try:
            # Prepare the conversation
            messages = [self.system_message]
            
            # Add context if provided
            if context:
                context_message = {
                    "role": "user",
                    "content": f"Context: {json.dumps(context, indent=2)}"
                }
                messages.append(context_message)
            
            # Add the user message
            user_message = {
                "role": "user",
                "content": message
            }
            messages.append(user_message)
            
            # Get response from OpenAI
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract the response
            assistant_response = response.choices[0].message.content
            
            # Store in conversation history
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user_message": message,
                "context": context,
                "assistant_response": assistant_response,
                "model": self.config.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            })
            
            return {
                "response": assistant_response,
                "agent_name": self.config.name,
                "agent_type": self.config.type,
                "timestamp": datetime.now().isoformat(),
                "model": self.config.model,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"Error processing message in supply chain agent: {e}")
            return {"error": str(e)}
    
    async def analyze_supply_chain(self, supply_chain_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze supply chain data and provide optimization recommendations.
        
        Args:
            supply_chain_data: Supply chain data to analyze
            
        Returns:
            Analysis results and recommendations
        """
        analysis_prompt = f"""
        Analyze the following supply chain data and provide detailed optimization recommendations:
        
        Supply Chain Data:
        {json.dumps(supply_chain_data, indent=2)}
        
        Please provide:
        1. Current state analysis
        2. Identified inefficiencies and bottlenecks
        3. Optimization opportunities
        4. Specific actionable recommendations
        5. Expected impact and ROI
        6. Implementation timeline
        7. Risk factors and mitigation strategies
        
        Format your response as structured JSON with clear sections.
        """
        
        response = await self.process_message(analysis_prompt)
        return response
    
    async def optimize_inventory(self, inventory_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize inventory levels and management strategies.
        
        Args:
            inventory_data: Current inventory data
            
        Returns:
            Inventory optimization recommendations
        """
        optimization_prompt = f"""
        Optimize the following inventory data:
        
        Inventory Data:
        {json.dumps(inventory_data, indent=2)}
        
        Provide recommendations for:
        1. Optimal inventory levels for each item
        2. Reorder points and quantities
        3. Safety stock recommendations
        4. Inventory turnover improvements
        5. Cost reduction opportunities
        6. Demand forecasting insights
        
        Include specific numbers and rationale for each recommendation.
        """
        
        response = await self.process_message(optimization_prompt)
        return response
    
    async def forecast_demand(self, historical_data: Dict[str, Any], forecast_horizon: int = 30) -> Dict[str, Any]:
        """
        Generate demand forecasts based on historical data.
        
        Args:
            historical_data: Historical demand and related data
            forecast_horizon: Number of days to forecast
            
        Returns:
            Demand forecast and analysis
        """
        forecast_prompt = f"""
        Generate demand forecasts based on the following historical data:
        
        Historical Data:
        {json.dumps(historical_data, indent=2)}
        
        Forecast Horizon: {forecast_horizon} days
        
        Please provide:
        1. Demand forecast for the next {forecast_horizon} days
        2. Confidence intervals and uncertainty analysis
        3. Seasonal patterns and trends identified
        4. Key factors influencing demand
        5. Recommendations for demand management
        6. Early warning indicators for demand changes
        
        Include both daily and weekly aggregate forecasts.
        """
        
        response = await self.process_message(forecast_prompt)
        return response
    
    async def assess_supply_risk(self, supply_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess supply chain risks and provide mitigation strategies.
        
        Args:
            supply_data: Supply chain and supplier data
            
        Returns:
            Risk assessment and mitigation recommendations
        """
        risk_prompt = f"""
        Assess supply chain risks based on the following data:
        
        Supply Data:
        {json.dumps(supply_data, indent=2)}
        
        Provide comprehensive risk assessment including:
        1. Identified risk factors and their severity
        2. Probability and impact analysis
        3. Risk mitigation strategies
        4. Contingency planning recommendations
        5. Supplier diversification opportunities
        6. Early warning systems and monitoring
        
        Prioritize risks by their potential impact on operations.
        """
        
        response = await self.process_message(risk_prompt)
        return response
    
    async def optimize_routes(self, route_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize transportation routes and logistics.
        
        Args:
            route_data: Route and transportation data
            
        Returns:
            Route optimization recommendations
        """
        route_prompt = f"""
        Optimize transportation routes based on the following data:
        
        Route Data:
        {json.dumps(route_data, indent=2)}
        
        Provide optimization recommendations for:
        1. Most efficient routes for each destination
        2. Load consolidation opportunities
        3. Transportation cost reduction
        4. Delivery time optimization
        5. Fuel efficiency improvements
        6. Alternative routing strategies
        
        Include specific route recommendations with expected savings.
        """
        
        response = await self.process_message(route_prompt)
        return response
    
    async def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the agent's conversation history."""
        return self.conversation_history.copy()
    
    async def clear_conversation_history(self) -> None:
        """Clear the agent's conversation history."""
        self.conversation_history.clear()
        logger.info(f"Cleared conversation history for agent '{self.config.name}'") 