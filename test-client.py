import requests
import json
import sys

def test_greet_tool(name, use_ingress=False):
    # LOCAL: Use localhost:8081 (Docker/Compose)
    # INGRESS: Use mcp.local (Minikube Ingress)
    if use_ingress:
        url = "http://mcp.local/mcp"
        print(f"--- Testing via K8s Ingress: {url} ---")
    else:
        url = "http://localhost:8081/mcp"
        print(f"--- Testing via Local Docker: {url} ---")

    # Specific headers required by FastMCP v2.0+
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # The JSON-RPC 2.0 payload
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
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse result
        data = response.json()
        print("Response Status: ", response.status_code)
        print("Result Summary: ", data.get("result", {}).get("content", [{}])[0].get("text", "No response text"))
        print("\nFull JSON Result:")
        print(json.dumps(data, indent=2))
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to {url}. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Default test
    user_name = "Dhiraj"
    
    # Logic to check if user wants to test Ingress via command line argument
    # Run: python3 test_client.py ingress
    ingress_mode = len(sys.argv) > 1 and sys.argv[1].lower() == "ingress"
    
    test_greet_tool(user_name, use_ingress=ingress_mode)