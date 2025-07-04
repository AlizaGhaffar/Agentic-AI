from agent import myAgent
import chainlit as cl
import asyncio

@cl.on_chat_start
async def start():
    await cl.Message(
        content = "wellcome to the multi agent system! how can i asist you").send()

@cl.on_message
async def main(message: cl.Message):
    user_input =message.content
    response = asyncio.run(myAgent(user_input))
    await cl.Message(
        content=f"{response}"
    ).send()
