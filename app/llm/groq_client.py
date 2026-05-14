import os

from groq import Groq

from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def call_groq(
    prompt: str,
    model: str = "llama-3.3-70b-versatile"
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a medical insurance "
                    "document extraction engine."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content