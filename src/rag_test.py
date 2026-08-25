# test_rag.py
# 测试脚本
from rag_chat import ask  # 导入你的核心函数

test_cases = [
    # in: 知识库明确覆盖的问题（分散测试不同文档，别只测台风）
    {"question": "什么是湿绝热递减率？", "expected_in_answer": "湿绝热", "type": "in"},
    {"question": "寒潮是怎么形成的？", "expected_in_answer": "寒潮", "type": "in"},
    {"question": "厄尔尼诺现象是什么？", "expected_in_answer": "厄尔尼诺", "type": "in"},
    {"question": "台风为什么会旋转？", "expected_in_answer": "科里奥利", "type": "in"},

    # out: 完全无关的问题
    {"question": "明天北京会下雨吗？", "expected_in_answer": "不知道", "type": "out"},
    {"question": "为什么地球是圆的？", "expected_in_answer": "无法", "type": "out"},
    {"question": "Python和JavaScript有什么区别？", "expected_in_answer": "无法", "type": "out"},

    # 边界case：看似和气象相关，但库里没有对应内容（实时数据/具体预报类）
    {"question": "今天台风预警发布了吗？", "expected_in_answer": "无法", "type": "out"},
    {"question": "上海明天的湿度是多少？", "expected_in_answer": "无法", "type": "out"},

    # conflict: 带错误前提的问题，测试模型能否纠正而不是顺着错误前提回答
    {"question": "台风是静止不动的吗？", "expected_in_answer": "移动", "type": "conflict"},
    {"question": "台风眼是台风里最危险的地方对吧？", "expected_in_answer": "平静", "type": "conflict"},
]

for case in test_cases:
    result = ask(case["question"])  # 现在ask返回的是dict了，记得改变量名
    print(f"问题: {case['question']}")
    print(f"distances: {result['distances']}")
    print("---")

"""
为什么重要：
    你做了一次改动（比如换了分块策略），怎么知道效果是变好了还是变差了？
    没有测试集，你只能“凭感觉”。
    有了测试集，你能说：“我把分块从固定500改成按标题切分后，3个测试用例的通过率从66%提升到100%。”
    ——这是面试官最想听到的表达。
"""