"""
第一个测试脚本:验证 DeepSeek API 是否能正常调用
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 第一步:加载 .env 文件里的环境变量(比如 API Key)
load_dotenv()

# 第二步:读取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    print("❌ 没有读取到 API Key,请检查 .env 文件")
else:
    print(f"✅ 成功读取到 API Key,开头是: {api_key[:10]}...")

# 第三步:调用 DeepSeek API(用 OpenAI 兼容格式)
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "你是一个大气科学科普助手。"},
        {"role": "user", "content": "用一句话解释一下什么是锋面。"}
    ],
    stream=False
)

print("\n=== DeepSeek 的回复 ===")
print(response.choices[0].message.content)