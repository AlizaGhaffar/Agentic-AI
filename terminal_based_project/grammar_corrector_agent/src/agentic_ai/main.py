from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel,AsyncOpenAI, set_tracing_disabled 
import os 

def agent():
    load_dotenv()
    set_tracing_disabled(True)

    provider =AsyncOpenAI(
        api_key= os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    Model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash-exp",
        openai_client= provider
    )
    Agent1 = Agent(
        name = "assistant",
        instructions= "you are an helpful english grammar corrector assistant",
        model= Model
    )
    Responce = Runner.run_sync(
        starting_agent= Agent1 ,
        input= "he is a girl correct this sentence"
    )
    print(Responce.final_output)