"""
第三个脚本:把知识块转换成向量,存入ChromaDB
"""

import os
import time
from dotenv import load_dotenv
import dashscope
from langchain_text_splitters import MarkdownHeaderTextSplitter
import chromadb

# ========== 第一步:初始化配置 ==========
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

EMBEDDING_MODEL = "qwen3.7-text-embedding"
BATCH_SIZE = 10  # 每次批量向量化的文本数量

# ========== 第二步:加载并切分文档(复用之前的逻辑) ==========
headers_to_split_on = [
    ("#", "概念"),
    ("##", "小节"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

data_dir = "../data"
all_chunks = []

for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            chunks = markdown_splitter.split_text(content)
            for chunk in chunks:
                chunk.metadata["source_file"] = file
                all_chunks.append(chunk)

print(f"✅ 共切分出 {len(all_chunks)} 个知识块\n")

# ========== 第三步:批量向量化 ==========
print("开始向量化...")

all_embeddings = []
all_texts = [chunk.page_content for chunk in all_chunks]

for i in range(0, len(all_texts), BATCH_SIZE):
    batch = all_texts[i:i + BATCH_SIZE]

    resp = dashscope.TextEmbedding.call(
        model=EMBEDDING_MODEL,
        input=batch
    )

    if resp.status_code == 200:
        # 按顺序取出这一批的向量
        batch_embeddings = [item["embedding"] for item in resp.output["embeddings"]]
        all_embeddings.extend(batch_embeddings)
        print(f"  已处理 {min(i + BATCH_SIZE, len(all_texts))}/{len(all_texts)} 个知识块")
    else:
        print(f"  ❌ 第 {i} 批向量化失败: {resp.message}")
        break

    time.sleep(0.2)  # 稍微间隔一下,避免请求过快

print(f"\n✅ 向量化完成,共生成 {len(all_embeddings)} 个向量\n")

# ========== 第四步:存入ChromaDB ==========
print("开始存入 ChromaDB...")

# 在本地创建一个持久化的数据库,存放在 db 文件夹下
chroma_client = chromadb.PersistentClient(path="../db")

# 创建(或获取已存在的)集合,相当于一张表
collection = chroma_client.get_or_create_collection(name="weather_knowledge")

# 准备存入的数据
ids = [f"chunk_{i}" for i in range(len(all_chunks))]
documents = [chunk.page_content for chunk in all_chunks]
metadatas = [chunk.metadata for chunk in all_chunks]

collection.add(
    ids=ids,
    embeddings=all_embeddings,
    documents=documents,
    metadatas=metadatas
)

# ========= 第五步:验证存入结果 ==========
# 1. 查询数据库,验证数据库和向量接口
# 2. 手动计算 L2 和 cosine,验证和 Chroma 返回的距离是否一致，
# 3. 结果是，chroma默认确实是用 L2 距离计算的，千问3.7的向量是归一化的，
# 对于已经归一化的向量，它们的“排序结果的排序等价”，但数值本身并不相等。
# Qwen 向量接口并不知道 Chroma 用 L2。归一化是模型自身输出向量的设计。 
# Chroma 默认 L2 返回的数值，在测试中对应的是平方欧氏距离。
# 但因为 Qwen 给的全是单位向量，所以从排序的结果来看，欧氏距离，余弦距离和内积距离得到的排序结果是一样的。
# 由于 Qwen 输出的 embedding 已归一化为单位向量，Chroma 默认 L2 返回的平方欧氏距离与 cosine distance 满足
#       L2²=2Dcos
# 二者是严格的正比例关系，因此对同一个 query 的知识块进行排序时，排序结果完全一致。

import math

query_embedding = all_embeddings[0]

result = collection.query(
    query_embeddings=[query_embedding],
    n_results=2,
    include=["documents", "distances"]
)

print("\nChroma 查询结果：")
print(result["distances"])

# Chroma 返回的第二个结果
chroma_distance = result["distances"][0][1]

# 找到第二个结果对应的文本
target_text = result["documents"][0][1]

# 在 documents 里找到对应索引
index = documents.index(target_text)

target_embedding = all_embeddings[index]

# 手动计算 L2
l2_distance = math.sqrt(
    sum(
        (a - b) ** 2
        for a, b in zip(query_embedding, target_embedding)
    )
)

# 手动计算 cosine
dot = sum(
    a * b
    for a, b in zip(query_embedding, target_embedding)
)

norm_a = math.sqrt(sum(a * a for a in query_embedding))
norm_b = math.sqrt(sum(b * b for b in target_embedding))

cosine_similarity = dot / (norm_a * norm_b)

cosine_distance = 1 - cosine_similarity

print("\nChroma distance:", chroma_distance)
print("手动 L2 distance:", l2_distance)
print("手动 cosine similarity:", cosine_similarity)
print("手动 cosine distance:", cosine_distance)

print(f"✅ 已存入 ChromaDB,集合中共有 {collection.count()} 条记录")
print(f"集合元数据 {collection.metadata}")
print("数据库保存在 weather-assistant/db 文件夹下")