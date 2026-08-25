"""
第四个脚本:完整的RAG问答系统
用户提问 -> 检索相关知识 -> 调用DeepSeek生成回答
"""

import os
from dotenv import load_dotenv
import dashscope
import chromadb
from openai import OpenAI

# ========== 第一步:初始化配置 ==========
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

EMBEDDING_MODEL = "qwen3.7-text-embedding"
TOP_K = 3  # 每次检索最相关的3个知识块

# 连接到之前存好的ChromaDB
chroma_client = chromadb.PersistentClient(path="../db")
collection = chroma_client.get_collection(name="weather_knowledge")

# DeepSeek客户端
deepseek_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# ========== 第二步:定义检索函数 ==========
def retrieve_relevant_chunks(question, top_k=TOP_K):
    """把问题向量化,然后在ChromaDB里检索最相关的知识块"""
    """
    关于top‑k
    k = number，返回相似度最高的前 k 条结果
    top_k=3:检索库里面，挑出最相关的前 3 个 chunk
    """

    resp = dashscope.TextEmbedding.call(
        model=EMBEDDING_MODEL,
        input=question
    )

    question_embedding = resp.output["embeddings"][0]["embedding"]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
        # where={"source":"doc.md"}
    )
    """
        where 是元数据过滤，和相似度无关，它是前置筛选条件。
        原理:先根据 where 条件，从库里面过滤一部分文档，然后再在剩下的数据里面做向量相似度检索。
        ⚠️where不能用来改相似度、不能用来排序，它只是做范围过滤。
    """
    """
        n_results输出的结果默认按相似度从高到低排
        Chroma 使用余弦距离:distance 值越小 = 越相似
        注意:这个排序，是向量相似度排序，不是语义精准度排序。
    """
    """
        👉 输入:问题向量
        👉 输出:top‑3 条 chunk 原文 + 距离分数
        这里拿到的仍然是文本，不是向量！！向量只用做搜索，后面大模型、重排模型全部接收字符串文本。
    """
    """
        关于重排rerank
        把:用户问题 + 刚刚捞出来的 3 段 chunk 原文，发给重排 API
        重排模型完全不使用向量，它直接拿纯文字做深度语义打分，重新排优先级。
        经过重排之后挑选靠前的片段，拼接成一段上下文，交给 DeepSeek 大模型
        传给 DeepSeek 大模型，100% 是纯文本字符串，绝对不是向量
        😀向量只干一件事:在 Chroma 里面做相似度搜索
        一旦检索结束，向量就不再使用。

        行业标准做法是混合检索(Hybrid Search) + 重排序(Rerank)
            1.并行召回:同一个问题同时走向量检索(语义)和关键词检索(精确匹配)
            2.分数融合:用RRF或加权求和把两组分数合并
            重排序:对Top-20用Cross-Encoder模型(如BGE-Reranker)做精细评分，再取Top-5送给大模型

            真正的生产级RAG检索链路是三层漏斗
                【第一阶段:召回(Recall)】  
                目的:从海量文档中快速筛出候选集  
                方式:多路并行(向量 + BM25关键词 + 可能还有时间/标签过滤)  
                输出:Top-50 ~ Top-200(宽进)

                【第二阶段:重排(Rerank)】  
                目的:用更精细的模型对候选集打分，重新排序  
                方式:Cross-Encoder模型(如BGE-Reranker、Cohere Rerank)逐对计算问题-文档的相关性  
                输出:Top-5 ~ Top-10(严出)

                【第三阶段:上下文压缩/精炼(Context Compression)】  
                目的:把Top-5文档压缩成不超上下文窗口的"精华摘要"  
                方式:LLM总结、提取关键句、或者用LongLLMLingua做信息压缩  
                输出:最终喂给大模型的prompt

                第四步可以是自我反思（Self-Correction）：
                大模型生成答案后，再问自己一遍"这个答案真的基于我给的文档吗？"
                如果有幻觉，重新生成。但第四步属于高级玩法，先把前三步跑通。
        
        语义感知切分（Semantic-Aware Chunking）:
            让每个chunk的语义边界和文档结构对齐,是生产环境里最重要的优化手段之一。
            核心思想：不是机械地按字符数切，而是按文档的语义边界（标题、段落、代码块）切，保证每个chunk内部逻辑自洽。  

        倒排索引（Inverted Index）:传统搜索引擎的核心技术,通过关键词快速定位文档,但无法理解语义。
            这是搜索引擎最核心的数据结构，打个比方：
            正向索引：文档1 → 包含“大气”“压力”“温度”；文档2 → 包含“湿度”“降水”...
            倒排索引：“大气” → 出现在文档1、文档3、文档7；“压力” → 出现在文档1、文档4、文档9...

            它倒过来了：从“词”指向“文档列表”。这样用户搜“大气压力”时，系统直接查倒排索引找到同时包含这两个词的文档，秒级返回。
            搜索引擎（Elasticsearch、Solr）的核心就是倒排索引。  

        BM25全文检索：
            BM25是一个独立的、标准的、经典的全文检索算法, 全称：Best Matching 25.
            它是倒排索引的经典算法，基于词频(TF)和逆文档频率(IDF)计算文档相关性。

            25的由来：
                25是BM系列算法的第25个版本, 是 Stephen Robertson 和 Karen Spärck Jones 在 1990 年代
                于伦敦城市大学（City University London）的 Okapi 信息检索项目中提出的.
                它是对BM1、BM2等早期版本的改进，综合考虑了词频、逆文档频率和文档长度归一化等因素。  

            它做了什么：
                给定一个查询词（比如“湿绝热递减率”），对每个文档计算一个相关性分数。分数取决于三个因素：

                词频（TF）：这个词在文档里出现了几次？
                逆文档频率（IDF）：这个词在所有文档里多常见？“的”这个词到处都是，得分低；“湿绝热”很罕见，得分高。
                文档长度归一化：同样包含“大气”一词，短文档比长文档更相关。

            BM25公式: 
            
                score(D,Q) = ∑ (IDF(qi) * (f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * |D|/avgdl)))
                其中:
                    D:文档
                    Q:查询
                    qi:查询中的词
                    f(qi,D):词qi在文档D中出现的次数
                    |D|:文档D的长度(词数)
                    avgdl:语料库中文档的平均长度
                    k1,b:调节参数,通常k1=1.2,b=0.75
      
        切块策略确实值得独立研究——它是RAG的“地基”
        唯一建议：把选型参数写进配置文件，不要hardcode在代码里。

        Streamlit：前端工程师的“RAG展示神器”
            Streamlit是一个纯Python的Web应用框架，专门给机器学习工程师做原型展示用的。
            你不需要写任何HTML/CSS/JS，只需要写Python，它自动生成交互式界面。

    """
    return results


# ========== 第三步:定义生成回答函数 ==========
def generate_answer(question, retrieved_results):
    """把检索到的知识组织成Prompt,交给DeepSeek生成回答"""

    context_pieces = []
    for i, doc in enumerate(retrieved_results["documents"][0]):
        metadata = retrieved_results["metadatas"][0][i]
        source = f"[{metadata.get('概念', '未知')} - {metadata.get('小节', '未知')}]"
        context_pieces.append(f"{source}\n{doc}")

    context = "\n\n---\n\n".join(context_pieces)

    system_prompt = """你是一个专业的大气科学科普助手。请严格根据下面提供的"参考资料"来回答用户的问题。
要求:
1. 回答要准确、通俗易懂
2. 只使用参考资料中的信息,不要编造资料中没有的内容
3. 如果参考资料不足以回答问题,请明确说明"根据现有资料,无法完整回答这个问题"
4. 回答末尾注明参考了哪些概念"""

    user_prompt = f"""参考资料:
{context}

用户问题:{question}"""

    """
        关于f""""""
        和 JS ${变量} 是同一个思想，Python 里面叫 f‑string(格式化字符串)
        开头没有 f的"""""" 是 Python 多行字符串，原样文字，不能插入变量
            三重引号字符串 """""" 里面的换行、缩进空格，全部属于字符串内容本身，
            Python 语法层面不会报错,但是会造成你不想要的多余空格、缩进。
        开头有 f的f"""""" 是 Python 多行格式化字符串，可以插入变量
            大括号 {context}、{question}，会自动替换成变量里面真实的文本
    """

    response = deepseek_client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=False
    )

    return response.choices[0].message.content


# ========== 第四步:整合成完整问答流程 ==========
def ask(question):
    print(f"\n❓ 问题: {question}\n")

    print("🔍 正在检索相关知识...")
    results = retrieve_relevant_chunks(question)

    # 测试结果distance的阈值，是否合格，如果一个都没有，就不再请求大模型了
    # results里distances[0][0]是这批数据最小的也是最可靠的，如果这个都比设定阈值大，这批数据可以宣告失败
    # if results["distances"][0][0] >= ?:
    #     print("检索到的知识块质量不高，不再请求大模型。")
    #     return


    print("\n💬", "结果:", results, "\n")


    print("检索到的知识块来源:")
    for metadata in results["metadatas"][0]:
        print(f"  - {metadata.get('概念')} / {metadata.get('小节')}")

    print("\n💬 正在生成回答...\n")
    answer = generate_answer(question, results)

    print("=== 回答 ===")
    print(answer)

    # ========== 新增这1行 ==========
    # 把答案返回给调用者（Streamlit）时使用，本文件运行时不适用
    # return answer  # 返回答案和来源元数据

    # return {'answer':answer, 'sources':results["metadatas"][0], 'distances':results["distances"][0]}  # 返回答案和来源元数据
    
    # 返回最终答案及其检索来源，供 Streamlit 展示
    return {
        "answer": answer,
        "ids": results["ids"][0],
        "documents": results["documents"][0],
        "sources": results["metadatas"][0],
        "distances": results["distances"][0]
    }


# ========== 测试 ==========
if __name__ == "__main__":
    # ask("为什么台风都是旋转的?")
    # 假答案测试
    # ask("为什么台风的风是从中心往外吹的?")
    ask("为什么地球是圆的?")