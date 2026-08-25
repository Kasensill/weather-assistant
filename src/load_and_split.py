"""
第二个测试脚本:读取data文件夹下所有md文件,按标题切分,查看切分效果
"""

import os
from langchain_text_splitters import MarkdownHeaderTextSplitter

# 第一步:定义按什么标题层级切分
# 我们的文档结构是 # 概念名 -> ## 定义/原理/特征等
headers_to_split_on = [
    ("#", "概念"),
    ("##", "小节"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

# 第二步:遍历data文件夹下所有md文件
data_dir = "../data"  # 相对于 src 文件夹的路径
all_chunks = []

for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 按标题切分
            chunks = markdown_splitter.split_text(content)

            # 给每个chunk加上来源文件信息,方便以后追溯
            for chunk in chunks:
                chunk.metadata["source_file"] = file
                all_chunks.append(chunk)

# 第三步:打印统计信息和示例
print(f"✅ 一共切分出 {len(all_chunks)} 个知识块\n")

print("=== 前3个知识块示例 ===\n")
for i, chunk in enumerate(all_chunks[:3]):
    print(f"--- 知识块 {i+1} ---")
    print(f"来源文件: {chunk.metadata.get('source_file')}")
    print(f"元数据: {chunk.metadata}")
    print(f"内容: {chunk.page_content[:100]}...")  # 只显示前100字符
    print()