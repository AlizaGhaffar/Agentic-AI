from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, set_tracing_disabled 
import os 
from tool import roll_dice,generate_events
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
narrator_agent = Agent(
    name = "narrator_agent",
    instructions= "you narrate the adventure and ask for choice",
    model = model
)
monster_agent = Agent(
    name ="monster_agent",
    instructions="you handle monster encounter using roll dice and generate event",
    model = model,
    tools = [roll_dice, generate_events]
)
item_agent = Agent(
    name= "item agent",
    instructions="you provide rewards or item to the player",
    model= model
)
def main():
    print ("wellcome to fantasy game")
    choice = input("do you enter the forest or turn back ->")
    result1 = Runner.run_sync(narrator_agent, choice)
    print("story",result1.final_output)

    result2 = Runner.run_sync(monster_agent,"start encounter")
    print("encounter:", result2.final_output)

    result3 = Runner.run_sync(item_agent,"give rewards")
    print("rewards:", result3.final_output)
if __name__ =="__main__":
    main()

