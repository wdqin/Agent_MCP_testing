from qwen_agent.agents import Assistant
import json

class QwenAgentWrapper:
    def __init__(self, llm_cfg: dict, tool_cfg: list = None):
        """
        Initializes the wrapper with configuration but does NOT instantiate the Qwen agent yet.
        """
        self.llm_cfg = llm_cfg
        self.tool_cfg = tool_cfg if tool_cfg is not None else []
        self.agent = None
        
    def initialize_agent(self):
        """
        Instantiate the Qwen-Agent with stored configurations.
        """
        self.agent = Assistant(llm=self.llm_cfg, function_list=[self.tool_cfg,'code_interpreter'])
        print("***CAR AGENT LOADED***")

    @classmethod
    def from_json(cls, llm_cfg_path: str, tool_cfg_path: str = None):
        """
        Creates an instance by loading configurations from JSON files.
        """
        with open(llm_cfg_path, "r", encoding="utf-8") as f:
            llm_cfg = json.load(f)

        tool_cfg = []
        if tool_cfg_path:
            with open(tool_cfg_path, "r", encoding="utf-8") as f:
                tool_cfg = json.load(f)

        return cls(llm_cfg=llm_cfg, tool_cfg=tool_cfg)
        
    def chat(self, msg: str):
        """
        Sends messages to the initialized agent.
        """
        if self.agent is None:
            raise RuntimeError("Agent is not initialized. Call `initialize_agent()` first.")

        msg = [{'role': 'user', 'content': msg}]
        for rsps in self.agent.run(messages=msg):
            pass
            
        return rsps