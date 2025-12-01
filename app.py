
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import openai
import textwrap

# Streamlit 介面
st.title("RAG 完整系統 Demo")

# 1. 上傳文件
uploaded_file = st.file_uploader("上傳知識文件 (txt)", type=["txt"])

if uploaded_file:
	file_text = uploaded_file.read().decode("utf-8")
	st.write("文件內容預覽：")
	st.code(textwrap.shorten(file_text, width=500))
else:
	file_text = """RAG 是 Retrieval-Augmented Generation 的縮寫。\nRAG 系統結合了檢索與生成模型。\nStreamlit 可以快速建立互動式網頁。\nFAISS 是高效的向量檢索工具。"""

# 2. 分段
def split_text(text, chunk_size=100):
	paragraphs = text.split('\n')
	chunks = []
	for p in paragraphs:
		if len(p) <= chunk_size:
			chunks.append(p)
		else:
			for i in range(0, len(p), chunk_size):
				chunks.append(p[i:i+chunk_size])
	return [c for c in chunks if c.strip()]

documents = split_text(file_text)
st.write(f"分段數量：{len(documents)}")

# 3. 建立 embedding 與 FAISS 索引
MODEL_NAME = 'paraphrase-MiniLM-L6-v2'
@st.cache_resource
def get_model():
	return SentenceTransformer(MODEL_NAME)
model = get_model()

embeddings = model.encode(documents)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# 4. 問答互動
user_query = st.text_input("請輸入你的問題：")
k = st.slider("檢索片段數量", 1, min(5, len(documents)), 2)

if user_query:
	query_vec = model.encode([user_query])
	D, I = index.search(np.array(query_vec), k=k)
	retrieved_docs = [documents[i] for i in I[0]]
	st.write("檢索到的知識片段：")
	for doc in retrieved_docs:
		st.info(doc)

	# 5. 串接 OpenAI 產生回答
	openai_api_key = st.text_input("OpenAI API Key (選填)", type="password")
	if openai_api_key:
		openai.api_key = openai_api_key
		prompt = f"你是一個知識問答助手，根據以下知識片段回答問題：\n\n" + "\n".join(retrieved_docs) + f"\n\n問題：{user_query}\n回答："
		with st.spinner("OpenAI 產生回答中..."):
			try:
				response = openai.ChatCompletion.create(
					model="gpt-3.5-turbo",
					messages=[{"role": "user", "content": prompt}],
					max_tokens=256
				)
				answer = response['choices'][0]['message']['content']
				st.success("RAG 回答：")
				st.write(answer)
			except Exception as e:
				st.error(f"OpenAI API 錯誤：{e}")
	else:
		st.warning("如需 GPT 產生完整回答，請輸入 OpenAI API Key")
