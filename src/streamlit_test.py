# streamlit_test.py

import streamlit as st

from rag_chat import ask


# ========== 页面配置 ==========

st.set_page_config(
    page_title="大气科学RAG问答",
    page_icon="🌤️"
)

st.title("🌤️ 大气科学知识问答")
st.caption("输入问题，系统从知识库检索相关知识并生成回答")


# ========== 初始化对话历史 ==========

if "messages" not in st.session_state:
    st.session_state.messages = []


# ========== 显示历史消息 ==========

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        # 用户消息 / AI回答
        st.markdown(msg["content"])

        # 如果是 AI 消息，并且存在检索来源
        if msg["role"] == "assistant" and "sources" in msg:

            with st.expander("🔍 查看本次检索来源"):

                sources = msg["sources"]

                if not sources:
                    st.info("本次回答没有检索到来源。")

                else:

                    for i, source in enumerate(sources):

                        st.markdown(f"### 📚 检索结果 {i + 1}")

                        # 来源信息
                        st.markdown(
                            f"**📄 来源文件：** "
                            f"{source['source_file']}"
                        )

                        st.markdown(
                            f"**📌 知识位置：** "
                            f"{source['concept']} / {source['section']}"
                        )

                        st.markdown(
                            f"**📏 Distance：** "
                            f"`{source['distance']:.6f}`"
                        )

                        # Chunk 原文
                        with st.container(border=True):

                            st.markdown("**原始知识块：**")

                            st.markdown(source["document"])

                        # 分隔线
                        if i < len(sources) - 1:
                            st.divider()


# ========== 用户输入 ==========

if question := st.chat_input("请输入大气科学相关问题："):

    # ---------- 显示用户问题 ----------

    with st.chat_message("user"):
        st.markdown(question)

    # 保存用户消息
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # ---------- 生成 AI 回答 ----------

    with st.chat_message("assistant"):

        with st.spinner("🔍 正在检索知识库并生成回答..."):

            result = ask(question)

        # 取出最终回答
        answer = result["answer"]

        # 显示回答
        st.markdown(answer)


        # ---------- 构造检索来源 ----------

        sources = []

        ids = result["ids"]
        documents = result["documents"]
        metadatas = result["sources"]
        distances = result["distances"]


        for i in range(len(ids)):

            metadata = metadatas[i]

            sources.append(
                {
                    "id": ids[i],

                    "document": documents[i],

                    "source_file": metadata.get(
                        "source_file",
                        "未知文件"
                    ),

                    "concept": metadata.get(
                        "概念",
                        "未知概念"
                    ),

                    "section": metadata.get(
                        "小节",
                        "未知小节"
                    ),

                    "distance": distances[i]
                }
            )


        # ---------- 显示检索来源 ----------

        with st.expander("🔍 查看本次检索来源"):

            if not sources:

                st.info("本次回答没有检索到来源。")

            else:

                for i, source in enumerate(sources):

                    st.markdown(
                        f"### 📚 检索结果 {i + 1}"
                    )

                    st.markdown(
                        f"**📄 来源文件：** "
                        f"{source['source_file']}"
                    )

                    st.markdown(
                        f"**📌 知识位置：** "
                        f"{source['concept']} / "
                        f"{source['section']}"
                    )

                    st.markdown(
                        f"**📏 Distance：** "
                        f"`{source['distance']:.6f}`"
                    )

                    # 显示原始 Chunk
                    with st.container(border=True):

                        st.markdown("**原始知识块：**")

                        st.markdown(
                            source["document"]
                        )

                    if i < len(sources) - 1:
                        st.divider()


    # ========== 保存 AI 消息 ==========

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources
        }
    )

# 启动命令
# streamlit run streamlit_test.py