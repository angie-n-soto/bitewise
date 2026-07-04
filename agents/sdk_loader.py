import sys

try:
    from google.antigravity import Agent, LocalAgentConfig
    from google.antigravity.types import McpStdioServer
    from google.antigravity.hooks import policy
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    
    # Provide stub classes so the scaffold loads cleanly when the SDK isn't installed yet.
    class LocalAgentConfig:
        def __init__(self, api_key=None, model=None, system_instructions=None, tools=None, mcp_servers=None, policies=None):
            self.api_key = api_key
            self.model = model
            self.system_instructions = system_instructions
            self.tools = tools or []
            self.mcp_servers = mcp_servers or []
            self.policies = policies or []

    class McpStdioServer:
        def __init__(self, name, command, args):
            self.name = name
            self.command = command
            self.args = args

    class policy:
        @staticmethod
        def allow_all():
            return "allow_all"
            
    class Agent:
        def __init__(self, config):
            self.config = config
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        async def chat(self, prompt):
            # Returns a dummy response object for testing
            class DummyResponse:
                async def text(self):
                    return "Mock response from agent."
                def __aiter__(self):
                    return self
                async def __anext__(self):
                    raise StopAsyncIteration
            return DummyResponse()
