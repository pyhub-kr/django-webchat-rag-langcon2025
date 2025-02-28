import os
import django
from openai import OpenAI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def make_ai_message(human_message: str) -> str:
    """
    OpenAI의 Chat Completion API를 사용하여 응답을 생성하는 함수
    """

    system_prompt = """
너는 번역가야.
한국어로 물어보면 한국어로 대답하며 영어 번역을 함께 제공해주고,
영어로 물어보면 영어로 대답하여 한글 번역을 함께 제공해줘.

예시:

<질문>안녕하세요.</질문>
<답변>반갑습니다. 저는 Tom 입니다. (영어: Nice to meet you. I am Tom.)</답변>

<질문>Hello.</질문>
<답변>Nice to meet you. I am Tom. (한국어: 안녕하세요. 저는 Tom 입니다.)</답변>
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 또는 "gpt-4o" 등 다른 모델 사용 가능
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": human_message},
            ],
            temperature=0.2,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API 호출에서 오류가 발생했습니다: {str(e)}"


def main():
    human_message = input("[Human] ").strip()

    ai_message = make_ai_message(human_message)
    print(f"[AI] {ai_message}")


if __name__ == "__main__":
    main()
