# Agent_MCP_testing

**Step 1:**
This step installs Qwen-agent
`git clone https://github.com/QwenLM/Qwen-Agent.git`
`cd Qwen-Agent`
`pip install -e ./"[gui,rag,code_interpreter,mcp]"`
Or `pip install -e ./` for minimal requirements.

**Step 2:**
This step installs mcp-related packages and creates MCP servers to provide extra tools.
`pip install uv`
`pip install mcp`
`pip install openai`

Go to the code root directory (if not):
`cd ./Agent_MCP_testing/car_demo/`
Then run `python demo.py` to see if the agent LLM responds correctly.  

**Step 3:**
This step tests the code that loads the car status from .json files, and call amap APIs to complete a navigation route generation task. 
`cd ./Agent_MCP_testing/car_demo/`
create two instances in the server and run these separately:
`python amap_server.py`

