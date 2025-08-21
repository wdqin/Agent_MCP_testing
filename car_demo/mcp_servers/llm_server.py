# mcp_servers/ollama_llm.py
import os
from mcp.server.fastmcp import FastMCP
from openai import OpenAI

mcp = FastMCP(name="gpt_llm_mcp")

@mcp.tool()
def llm_chat(prompt: str) -> str:
    """
    Send a prompt to the gpt-oss:20b and return the text reply.
    Args:
        prompt: message to send to the model
    """
    DEFAULT_MODEL = "gpt-oss:20b"  # Change to your model name
    DEFAULT_TEMP = 0.0         # Deterministic output
    
    mdl = DEFAULT_MODEL

    # Point to Ollama's OpenAI-compatible API
    client = OpenAI(
        base_url="http://localhost:11434/v1",  # Ollama endpoint
        api_key="ollama"                       # Ollama ignores API key but requires a string
    )

    with open("llm_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    
    resp = client.chat.completions.create(
        model=mdl,
        messages=[{"role": "user", "content": prompt}],
    )

    with open("llm_response.txt", "w", encoding="utf-8") as f:
        f.write(resp.choices[0].message.content)

    return resp.choices[0].message.content

if __name__ == "__main__":
    mcp.run()
    # response = llm_chat("How are you?")
    # print(response)
