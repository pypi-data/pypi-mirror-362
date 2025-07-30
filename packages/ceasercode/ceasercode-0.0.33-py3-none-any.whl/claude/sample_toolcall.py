import asyncio

from llm import Ollama
from ollama._types import ChatResponse,Message

client = Ollama(host="http://192.168.170.76:11434")
from tools import tools,tools_dict
messages = [
    {'role':"user",'content':"read /home/ntlpt59/master/own/claude/claude/sample_toolcall.py"}
]
response = client.chat(messages=messages,tools=tools,model="qwen3:4b")

res = str(asyncio.run(tools_dict[response.message.tool_calls[0].function.name](**response.message.tool_calls[0].function.arguments)))
messages.append(response.message)
messages.append({'role':'tool','content':res,'tool_name':response.message.tool_calls[0].function.name})
messages.append({'role':'user','content':'explain it'})
response = client.chat(messages=messages,tools=tools,model="qwen3:4b")
print(response)




# tcs = []
# res = ""
# for x in client(prompt="read app.py",tools=tools,model="qwen3:4b"):
#     if x.message.tool_calls:
#         tcs.extend(x.message.tool_calls)
#     res+=x.message.content
# pp = ChatResponse(message=Message(content=res,role='assistant',tool_calls=tcs))
