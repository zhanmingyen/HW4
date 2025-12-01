# HW4 - Streamlit RAG 系統

本專案為一個基於 Streamlit 的 RAG（Retrieval-Augmented Generation）問答系統，支援知識文件上傳、分段、向量檢索、OpenAI API 串接。

## 功能
- 上傳 txt 知識文件
- 自動分段與 embedding
- FAISS 向量檢索
- 問答互動介面
- 串接 OpenAI GPT 產生回答

## 執行方式
1. 安裝 Python 3.8+ 並建立虛擬環境
2. 安裝必要套件：
   ```bash
   pip install streamlit sentence-transformers faiss-cpu numpy openai
   ```
3. 啟動網頁：
   ```bash
   streamlit run app.py
   ```

## Prompt 範例
系統自動組合如下 prompt 給 OpenAI：

```
你是一個知識問答助手，根據以下知識片段回答問題：

（知識片段1）
（知識片段2）
...

問題：{使用者輸入的問題}
回答：
```

## 目錄結構
- app.py
- README.md
- Demo06b_RAG02_打造_RAG_系統.ipynb

## 參考
- [原始 notebook 範例](https://github.com/yenlung/AI-Demo/blob/master/%E3%80%90Demo06b%E3%80%91RAG02_%E6%89%93%E9%80%A0_RAG_%E7%B3%BB%E7%B5%B1.ipynb)

---
如需推送到 GitHub，請依下列指令操作：

```bash
git init
git remote add origin https://github.com/zhanmingyen/HW4.git
git add .
git commit -m "Initial commit: Streamlit RAG system"
git push -u origin master
```
