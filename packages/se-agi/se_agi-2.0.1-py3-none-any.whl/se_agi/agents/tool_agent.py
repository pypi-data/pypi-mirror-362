"""
Tool Agent for SE-AGI System

The ToolAgent specializes in tool management, integration, and execution.
It can discover, utilize, and orchestrate various external tools and APIs.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable, Union
from datetime import datetime
import json
import subprocess
import inspect
from .base import BaseAgent
from ..core.config import AgentConfig


class ToolAgent(BaseAgent):
    """
    Tool Agent specializing in tool management and execution.
    
    Capabilities:
    - Tool discovery and registration
    - API integration
    - Command execution
    - Tool chaining and orchestration
    - External service interaction
    - Tool performance monitoring
    """
    
    def __init__(self, config: AgentConfig, **kwargs):
        super().__init__(config, **kwargs)
        self.registered_tools = {}
        self.tool_history = []
        self.api_clients = {}
        self.tool_categories = {
            "system": [],
            "web": [],
            "data": [],
            "ml": [],
            "utility": [],
            "custom": []
        }
        
    async def initialize(self) -> None:
        """Initialize the tool agent"""
        await super().initialize()
        
        # Register built-in tools
        await self._register_builtin_tools()
        
        # Initialize API clients
        await self._initialize_api_clients()
        
        self.logger.info(f"ToolAgent initialized with {len(self.registered_tools)} tools")
    
    async def _register_builtin_tools(self) -> None:
        """Register built-in tools"""
        # System tools
        await self.register_tool(
            "execute_command",
            self._execute_command,
            category="system",
            description="Execute system commands",
            parameters={"command": "str", "timeout": "int"}
        )
        
        await self.register_tool(
            "file_operations",
            self._file_operations,
            category="system",
            description="Perform file operations",
            parameters={"operation": "str", "path": "str", "content": "str"}
        )
        
        # Web tools
        await self.register_tool(
            "http_request",
            self._http_request,
            category="web",
            description="Make HTTP requests",
            parameters={"url": "str", "method": "str", "data": "dict"}
        )
        
        await self.register_tool(
            "web_scraper",
            self._web_scraper,
            category="web",
            description="Scrape web content",
            parameters={"url": "str", "selector": "str"}
        )
        
        # Data tools
        await self.register_tool(
            "data_processor",
            self._data_processor,
            category="data",
            description="Process and transform data",
            parameters={"data": "any", "operation": "str"}
        )
        
        # Utility tools
        await self.register_tool(
            "text_processor",
            self._text_processor,
            category="utility",
            description="Process text data",
            parameters={"text": "str", "operation": "str"}
        )
    
    async def _initialize_api_clients(self) -> None:
        """Initialize API clients for external services"""
        # Placeholder for API client initialization
        self.api_clients = {
            "openai": None,  # Would initialize OpenAI client
            "github": None,  # Would initialize GitHub client
            "slack": None,   # Would initialize Slack client
            "email": None    # Would initialize email client
        }
    
    async def register_tool(
        self,
        name: str,
        function: Callable,
        category: str = "custom",
        description: str = "",
        parameters: Dict[str, str] = None,
        metadata: Dict[str, Any] = None
    ) -> bool:
        """
        Register a new tool
        
        Args:
            name: Tool name
            function: Tool function
            category: Tool category
            description: Tool description
            parameters: Parameter specifications
            metadata: Additional metadata
            
        Returns:
            Registration success status
        """
        try:
            if name in self.registered_tools:
                self.logger.warning(f"Tool {name} already registered, updating...")
            
            # Analyze function signature
            sig = inspect.signature(function)
            param_info = {
                param_name: {
                    "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty else "any",
                    "default": param.default if param.default != inspect.Parameter.empty else None
                }
                for param_name, param in sig.parameters.items()
            }
            
            tool_info = {
                "name": name,
                "function": function,
                "category": category,
                "description": description,
                "parameters": parameters or {},
                "signature": param_info,
                "metadata": metadata or {},
                "registered_at": datetime.now(),
                "usage_count": 0,
                "last_used": None,
                "average_execution_time": 0.0
            }
            
            self.registered_tools[name] = tool_info
            
            # Add to category
            if category in self.tool_categories:
                if name not in self.tool_categories[category]:
                    self.tool_categories[category].append(name)
            else:
                self.tool_categories["custom"].append(name)
            
            self.logger.info(f"Tool '{name}' registered successfully in category '{category}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register tool '{name}': {str(e)}")
            return False
    
    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any] = None,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        Execute a registered tool
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters to pass to the tool
            timeout: Execution timeout in seconds
            
        Returns:
            Tool execution results
        """
        if tool_name not in self.registered_tools:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found",
                "available_tools": list(self.registered_tools.keys())
            }
        
        tool_info = self.registered_tools[tool_name]
        
        try:
            start_time = datetime.now()
            
            # Prepare parameters
            params = parameters or {}
            
            # Execute tool function
            if asyncio.iscoroutinefunction(tool_info["function"]):
                result = await asyncio.wait_for(
                    tool_info["function"](**params),
                    timeout=timeout
                )
            else:
                result = await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(
                        None, lambda: tool_info["function"](**params)
                    ),
                    timeout=timeout
                )
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Update tool statistics
            tool_info["usage_count"] += 1
            tool_info["last_used"] = end_time
            
            # Update average execution time
            if tool_info["average_execution_time"] == 0:
                tool_info["average_execution_time"] = execution_time
            else:
                tool_info["average_execution_time"] = (
                    tool_info["average_execution_time"] * 0.8 + execution_time * 0.2
                )
            
            # Log execution
            execution_record = {
                "tool_name": tool_name,
                "parameters": params,
                "execution_time": execution_time,
                "timestamp": end_time,
                "success": True,
                "result_preview": str(result)[:200] if result else "None"
            }
            self.tool_history.append(execution_record)
            
            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "tool_info": {
                    "name": tool_name,
                    "category": tool_info["category"],
                    "usage_count": tool_info["usage_count"]
                }
            }
            
        except asyncio.TimeoutError:
            self.logger.error(f"Tool '{tool_name}' execution timed out after {timeout}s")
            return {
                "success": False,
                "error": f"Tool execution timed out after {timeout}s",
                "tool_name": tool_name
            }
        except Exception as e:
            self.logger.error(f"Tool '{tool_name}' execution failed: {str(e)}")
            
            # Log failed execution
            execution_record = {
                "tool_name": tool_name,
                "parameters": parameters,
                "timestamp": datetime.now(),
                "success": False,
                "error": str(e)
            }
            self.tool_history.append(execution_record)
            
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name
            }
    
    async def chain_tools(self, tool_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a chain of tools where output of one feeds into the next
        
        Args:
            tool_chain: List of tool specifications with parameters
            
        Returns:
            Chain execution results
        """
        try:
            results = []
            current_output = None
            
            for i, tool_spec in enumerate(tool_chain):
                tool_name = tool_spec["tool"]
                params = tool_spec.get("parameters", {})
                
                # If this isn't the first tool, use previous output
                if i > 0 and "input_from_previous" in tool_spec:
                    input_key = tool_spec["input_from_previous"]
                    if current_output and "result" in current_output:
                        params[input_key] = current_output["result"]
                
                # Execute tool
                result = await self.execute_tool(tool_name, params)
                results.append({
                    "step": i + 1,
                    "tool": tool_name,
                    "result": result
                })
                
                if not result.get("success", False):
                    return {
                        "success": False,
                        "error": f"Tool chain failed at step {i + 1}: {result.get('error', 'Unknown error')}",
                        "partial_results": results
                    }
                
                current_output = result
            
            return {
                "success": True,
                "final_result": current_output,
                "chain_results": results,
                "steps_completed": len(results)
            }
            
        except Exception as e:
            self.logger.error(f"Tool chain execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "partial_results": results if 'results' in locals() else []
            }
    
    async def discover_tools(self, category: str = None) -> List[Dict[str, Any]]:
        """
        Discover available tools, optionally filtered by category
        
        Args:
            category: Optional category filter
            
        Returns:
            List of available tools
        """
        tools = []
        
        for name, tool_info in self.registered_tools.items():
            if category is None or tool_info["category"] == category:
                tools.append({
                    "name": name,
                    "category": tool_info["category"],
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"],
                    "usage_count": tool_info["usage_count"],
                    "average_execution_time": tool_info["average_execution_time"]
                })
        
        return sorted(tools, key=lambda x: x["usage_count"], reverse=True)
    
    # Built-in tool implementations
    async def _execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute system command"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            return {
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "return_code": process.returncode,
                "command": command
            }
            
        except Exception as e:
            return {"error": str(e), "command": command}
    
    async def _file_operations(self, operation: str, path: str, content: str = None) -> Dict[str, Any]:
        """Perform file operations"""
        try:
            if operation == "read":
                with open(path, 'r', encoding='utf-8') as f:
                    return {"content": f.read(), "operation": operation, "path": path}
            
            elif operation == "write":
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content or "")
                return {"success": True, "operation": operation, "path": path}
            
            elif operation == "append":
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(content or "")
                return {"success": True, "operation": operation, "path": path}
            
            elif operation == "exists":
                import os
                return {"exists": os.path.exists(path), "path": path}
            
            else:
                return {"error": f"Unknown operation: {operation}"}
                
        except Exception as e:
            return {"error": str(e), "operation": operation, "path": path}
    
    async def _http_request(self, url: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make HTTP request (simulated)"""
        # This would use aiohttp or similar in a real implementation
        return {
            "status": 200,
            "url": url,
            "method": method,
            "response": f"Simulated response for {method} {url}",
            "data_sent": data
        }
    
    async def _web_scraper(self, url: str, selector: str = None) -> Dict[str, Any]:
        """Scrape web content (simulated)"""
        # This would use BeautifulSoup or similar in a real implementation
        return {
            "url": url,
            "selector": selector,
            "content": f"Simulated scraped content from {url}",
            "elements_found": 5
        }
    
    async def _data_processor(self, data: Any, operation: str) -> Dict[str, Any]:
        """Process data"""
        try:
            if operation == "count":
                return {"count": len(data) if hasattr(data, '__len__') else 1, "operation": operation}
            
            elif operation == "type":
                return {"type": type(data).__name__, "operation": operation}
            
            elif operation == "serialize":
                return {"serialized": json.dumps(data, default=str), "operation": operation}
            
            else:
                return {"error": f"Unknown operation: {operation}"}
                
        except Exception as e:
            return {"error": str(e), "operation": operation}
    
    async def _text_processor(self, text: str, operation: str) -> Dict[str, Any]:
        """Process text"""
        try:
            if operation == "length":
                return {"length": len(text), "operation": operation}
            
            elif operation == "words":
                words = text.split()
                return {"word_count": len(words), "words": words, "operation": operation}
            
            elif operation == "uppercase":
                return {"result": text.upper(), "operation": operation}
            
            elif operation == "lowercase":
                return {"result": text.lower(), "operation": operation}
            
            elif operation == "reverse":
                return {"result": text[::-1], "operation": operation}
            
            else:
                return {"error": f"Unknown operation: {operation}"}
                
        except Exception as e:
            return {"error": str(e), "operation": operation}
    
    async def get_tool_statistics(self) -> Dict[str, Any]:
        """Get tool usage statistics"""
        total_tools = len(self.registered_tools)
        total_executions = sum(tool["usage_count"] for tool in self.registered_tools.values())
        
        # Most used tools
        most_used = sorted(
            self.registered_tools.items(),
            key=lambda x: x[1]["usage_count"],
            reverse=True
        )[:5]
        
        # Category distribution
        category_counts = {cat: len(tools) for cat, tools in self.tool_categories.items()}
        
        # Recent execution history
        recent_executions = self.tool_history[-10:] if self.tool_history else []
        
        return {
            "total_tools": total_tools,
            "total_executions": total_executions,
            "most_used_tools": [{"name": name, "usage_count": info["usage_count"]} for name, info in most_used],
            "category_distribution": category_counts,
            "recent_executions": recent_executions,
            "average_execution_time_by_tool": {
                name: info["average_execution_time"] 
                for name, info in self.registered_tools.items()
                if info["usage_count"] > 0
            }
        }
    
    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool-specific tasks"""
        task_type = task.get("type", "execute")
        
        if task_type == "execute":
            return await self.execute_tool(
                task.get("tool_name"),
                task.get("parameters", {})
            )
        elif task_type == "chain":
            return await self.chain_tools(task.get("tool_chain", []))
        elif task_type == "discover":
            tools = await self.discover_tools(task.get("category"))
            return {"tools": tools, "success": True}
        elif task_type == "register":
            # This would require special handling for security
            return {"error": "Tool registration not supported via task execution", "success": False}
        else:
            return await super().execute_task(task)
