from fastmcp import FastMCP
from starlette.responses import JSONResponse

# Initialise Server
mcp = FastMCP(name="Remote MCP Example")

@mcp.tool
def greet(name:str)->str:
    """greet the user by name"""
    return f"Hello, {name}!"

# Add Standard HTTP route for Kubernetes health checks
# This bypasses the MCP protocol requirements for the probe
@mcp.custom_route("/health",methods=["GET"])
async def health_check(request):
    return JSONResponse({"status": "ok"})

if __name__=="__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8080,
        stateless_http=True,
        json_response=True
        )
