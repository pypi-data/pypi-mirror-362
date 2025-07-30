"""Agent tools for Hanzo AI.

This module provides tools that allow Claude to delegate tasks to sub-agents,
enabling concurrent execution of multiple operations and specialized processing.
"""

from mcp.server import FastMCP

from hanzo_mcp.tools.agent.agent_tool import AgentTool
from hanzo_mcp.tools.common.base import BaseTool, ToolRegistry

from hanzo_mcp.tools.common.permissions import PermissionManager


def register_agent_tools(
    mcp_server: FastMCP,
    permission_manager: PermissionManager,
    agent_model: str | None = None,
    agent_max_tokens: int | None = None,
    agent_api_key: str | None = None,
    agent_base_url: str | None = None,
    agent_max_iterations: int = 10,
    agent_max_tool_uses: int = 30,
) -> list[BaseTool]:
    """Register agent tools with the MCP server.

    Args:
        mcp_server: The FastMCP server instance

        permission_manager: Permission manager for access control
        agent_model: Optional model name for agent tool in LiteLLM format
        agent_max_tokens: Optional maximum tokens for agent responses
        agent_api_key: Optional API key for the LLM provider
        agent_base_url: Optional base URL for the LLM provider API endpoint
        agent_max_iterations: Maximum number of iterations for agent (default: 10)
        agent_max_tool_uses: Maximum number of total tool uses for agent (default: 30)

    Returns:
        List of registered tools
    """
    # Create agent tool
    agent_tool = AgentTool(
        permission_manager=permission_manager,
        model=agent_model,
        api_key=agent_api_key,
        base_url=agent_base_url,
        max_tokens=agent_max_tokens,
        max_iterations=agent_max_iterations,
        max_tool_uses=agent_max_tool_uses,
    )

    # Register agent tool
    ToolRegistry.register_tool(mcp_server, agent_tool)

    # Return list of registered tools
    return [agent_tool]
