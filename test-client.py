import requests
import json
import sys
from urllib.parse import urlparse, urlunparse
import urllib3

# Supress only the InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def test_health_endpoint(base_url):
    """Verifies the K8s health check endpoint returns 200 OK"""
    parsed = urlparse(base_url)
    
    # Correctly extracting the scheme string and netloc string
    # components: (scheme, netloc, path, params, query, fragment)
    health_url = urlunparse((parsed.scheme, parsed.netloc, '/health', '', '', ''))
    
    print(f"--- Verifying Health Check: {health_url} ---")
    try:
        response = requests.get(health_url, timeout=5,verify=False)
        if response.status_code == 200:
            print(f"✅ Health Check Passed: {response.json()}\n")
        else:
            print(f"❌ Health Check Failed: Status {response.status_code}\n")
    except Exception as e:
        print(f"❌ Health Check Error: {e}\n")

def test_greet_tool(name, use_ingress=False):
    # Determine base URL
    if use_ingress:
        base_url = "https://mcp.local/mcp"
    else:
        # Default for local Docker Desktop / Compose
        base_url = "http://localhost:8081/mcp"

    # 1. Run the health check first
    test_health_endpoint(base_url)

    # 2. Run the tool call
    print(f"--- Testing Tool Call: {base_url} ---")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": "greet",
            "arguments": {"name": name}
        }
    }

    try:
        response = requests.post(base_url, headers=headers, json=payload,verify=False)
        response.raise_for_status()
        
        data = response.json()
        print("Response Status: ", response.status_code)
        print("Result Summary: ", data.get("result", {}).get("content", [{}])[0].get("text", "No response text"))
        print("\nFull JSON Result:")
        print(json.dumps(data, indent=2))
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {base_url}. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    user_name = "Dhiraj"
    
    # Check if 'ingress' was passed as a command line argument
    ingress_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "ingress"
    
    test_greet_tool(user_name, use_ingress=ingress_mode)
