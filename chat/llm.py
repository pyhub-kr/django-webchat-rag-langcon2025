from typing import Optional, List, Dict
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LLM:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,
        max_tokens: int = 1000,
        system_prompt: str = "",
        initial_messages: Optional[List[Dict]] = None,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_prompt = system_prompt
        self.history = initial_messages or []

    def make_reply(self, human_message: Optional[str] = None):
        current_messages = [
            *self.history,
        ]

        if human_message is not None:
            current_messages.append({"role": "user", "content": human_message})

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self.system_prompt,
                    },
                ]
                + current_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            ai_message = response.choices[0].message.content
        except Exception as e:
            return f"API 호출에서 오류가 발생했습니다: {str(e)}"
        else:
            self.history.extend(
                [
                    {"role": "user", "content": human_message},
                    {"role": "assistant", "content": ai_message},
                ]
            )
            return ai_message
