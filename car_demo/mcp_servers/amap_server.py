import os
import sys

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp.server.fastmcp import FastMCP
from qwen_agent.agents import Assistant
from utils import load_json_file



LLM_CONFIG_FILE = "./configs/llm_config.json"
TOOL_CONFIG_FILE = "./configs/amap_agent_tool_config.json"

mcp = FastMCP(name="amap_agent_mcp")

@mcp.tool()
def handle_prompt(prompt: str) -> str:
    # Lazy-load agent when tool is invoked
    llm_cfg = load_json_file(LLM_CONFIG_FILE)
    tool_cfg = load_json_file(TOOL_CONFIG_FILE)
    tools = [tool_cfg, 'code_interpreter']

    agent = Assistant(llm=llm_cfg, function_list=tools)
    # # Example: 
    # msg = [{'role': 'user', 'content': "list what tools are available."}]
    # for rsps in agent.run(messages=msg):
    #     pass
    # print("rsps[-1]['content']",rsps[-1]['content'])
    
    print("***AMAP AGENT SERVER LOADED COMPLETE.***")
    msg = [{'role': 'user', 'content': prompt}]
    with open("amap_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    
    for rsps in agent.run(messages=msg):
        pass
    with open("amap_response.txt", "w", encoding="utf-8") as f:
        f.write(rsps[-1]["content"])
    return rsps[-1]["content"]

if __name__ == "__main__":
    mcp.run()
