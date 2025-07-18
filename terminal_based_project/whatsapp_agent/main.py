from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from whatsapp import send_whatsapp_message
from openai import AsyncOpenAI
import os

load_dotenv()
set_tracing_disabled(True)

API_KEY = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def get_user_data(min_age: int) -> list[dict]:
    girls = [
        {"name": "Areeba", "age": 18},
        {"name": "Rumaisa", "age": 20},
        {"name": "Zainab", "age": 26},
        {"name": "Mehwish", "age": 28},
        {"name": "Iqra", "age": 36},
    ]
    return [girl for girl in girls if girl["age"] >= min_age]


# 🤖 Rishty Wali AI Agent
rishty_agent = Agent(
    name="Terminal Rishty Aunty 💖",
    instructions="""
        Tum AI Rishtay Wali Aunty ho 👵
        Tumhe users se unki age aur WhatsApp number lena hai.
        get_user_data se rishta filter karo, aur agar user WhatsApp number de to send_whatsapp_message use karo.
        Tumhara tone masti bhara ho, emojis use karo, aur har jawab mein thoda aunty swag ho 💅
    """,
    model=model,
    tools=[get_user_data, send_whatsapp_message]
)

def main():
    print("👵 Assalamualaikum beta! Main hoon *AI Rishtay Wali Aunty* 🤖💖")
    print("Kya chahiye? Rishta, info, ya WhatsApp pe message? Mujhe sab aata hai 😌")
    print("💡 Type 'exit' ya 'quit' to leave Aunty's office.\n")

    history = []

    while True:
        user_input = input("🧑 Aap: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👵 Aunty: Allah Hafiz beta! Tumhara rishta likhwaya gaya hai arsh par 😇")
            break

        history.append({"role": "user", "content": user_input})

        try:
            result = Runner.run_sync(starting_agent=rishty_agent, input=history)
            response = result.final_output
        except Exception as e:
            response = f"❌ Aunty ko gussa aaya: {str(e)}"

        print(f"👵 Aunty: {response}\n")
        history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

