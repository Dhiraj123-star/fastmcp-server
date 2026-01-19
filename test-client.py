import requests
import json

def test_greet_tool(name):
    url= "http://localhost:8081/mcp"

    # specific headers
    headers={
        "Content-Type":"application/json",
        "Accept":"application/json"
    }

    payload = {
        "jsonrpc":"2.0",
        "id":"1",
        "method":"tools/call",
        "params":{
            "name":"greet",
            "arguments":{"name":name}
        }
    }
    try:
        response = requests.post(url,headers=headers,json=payload)
        response.raise_for_status()
        print("Response Status: ",response.status_code)
        print("Result:",json.dumps(response.json(),indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__=="__main__":
    test_greet_tool("Dhiraj")