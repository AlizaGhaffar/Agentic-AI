import os
from agents import Agent,Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from agents.run import RunConfig
from roadmap_tool import get_career_roadmap
load_dotenv()

client = AsyncOpenAI(
    api_key= os.getenv("GEMINI_API_KEY"),
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/" 
)
model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash-exp",
    openai_client= client
)
config= RunConfig(
    model = model,
    tracing_disabled= True
)
career_agent = Agent(
    name="career agent",
    instructions = "you ask about interest and suggest a career field",
    model=model
)
skill_agent = Agent(
    name="skill agent",
    instructions= "you share roadmap using tool get_career_roadmap",
    model = model,
    tools= [get_career_roadmap]
)
job_agent= Agent(
    name= "jobAgent",
    instructions = "you suggest job title in the choosen career  ",
    model = model
)
def main():
    print("career mentor agent"),
    interest=input("enter career you are interested in: ->")
    result1=Runner.run_sync(career_agent, interest, run_config=config)
    field= result1.final_output.strip()
    print("/n suggest career",field)

    result2 = Runner.run_sync(skill_agent,field, run_config= config)
    print("/n required skill",result2.final_output)

    
    result3 = Runner.run_sync(job_agent,field, run_config= config)
    print("/n possible jobs",result3.final_output)
if __name__ == "__main__":
    main()