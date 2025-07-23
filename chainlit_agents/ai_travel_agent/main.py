from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
from travel_tool import get_flight, suggest_hotel
import chainlit as cl

load_dotenv() 
set_tracing_disabled(True) 
 
provider = AsyncOpenAI( 
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
) 
 
model = OpenAIChatCompletionsModel( 
    model="gemini-2.0-flash-exp", 
    openai_client=provider, 
)
destinationAgent = Agent(
    name="destination agent",
    instructions="your task is to recommend traveller to find places based on their mood",
    model= model,
    handoff_description="handoff to destination agent if the task is related to destination agent"

)
bookingAgent= Agent(
    name="booking agent",
    instructions="you give flight info and hotel info using tools",
    model= model,
    handoff_description="handoff to booking agent if the task is related to booking agent",
    tools=[get_flight, suggest_hotel]
)
exploreAgent = Agent(
    name="exploring agent",
    instructions="your work is to suggest attractions and food in the destination",
    model= model,
    handoff_description="handoff to explore agent if the task is related to explore"
)
mainAgent = Agent(
    name="manager",
    instructions= "ask user whats your travel mood(relaxing/adventure/etc) or destination agent ko kaho" \
    "ky phir destination suggest kre or phir booking agent booking info dy or phir explore agent exploring " \
    "tip bhi dy tumhara kam handoff krna hai task jo user dy"
   ,
model=model,
handoff_description=[destinationAgent,bookingAgent,exploreAgent]
)

@cl.on_chat_start
async def start():
    cl.user_session.set("history",[])
    await cl.Message(content="wellcome to ai travel agent").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user" , "content": message.content})
    result = await Runner.run(
        mainAgent, input=history
    )
    history.append({"role":"assistant", "content": result.final_output})
    history = cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()
