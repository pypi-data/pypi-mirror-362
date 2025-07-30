from openai import OpenAI


class ChatGPTClient:
    def __init__(self,api_key):
        self.openai = OpenAI(api_key=api_key)

    # === ChatGPTにエラー内容を投げる関数 ===
    def ask_chatgpt(self, error_trace):
        response = self.openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは優秀なPythonエンジニアです。"},
            {"role": "user", "content": f"このPythonエラーの原因と解決方法を教えてください:\n```\n{error_trace}\n```"}
        ],
        max_tokens=500)
        return response.choices[0].message.content
