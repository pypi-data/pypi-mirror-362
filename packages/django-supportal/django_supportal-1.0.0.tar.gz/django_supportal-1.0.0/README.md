# 🧠 Django Supportal – AI-Powered Business Support Chat APIs for django projects

**Django Supportal** is an intelligent, AI-powered customer support system built with **Django**, **Django Channels**, and **OpenAI API**.  
It provides APIs for businesses to upload their internal documents, and a smart assistant will handle customer inquiries via live chat – powered by a Retrieval-Augmented Generation (RAG) system.

---

## 🚀 Features

- ✅ Real-time chat via **Django Channels (WebSockets)**
- 📎 Businesses can upload **PDF, DOCX, or TXT documents**
- 🤖 Uses **OpenAI GPT models** to provide intelligent responses
- 📚 Implements **RAG (Retrieval-Augmented Generation)** to process custom business knowledge
- 🔒 Secured communication and Redis-based event layer

---

## 🧠 How it Works (RAG Architecture)

Supportal uses a **Retrieval-Augmented Generation (RAG)** approach to enable AI to answer business-specific questions:

1. **Document Upload:**  
   Businesses upload documents such as FAQs, product guides, manuals, or policies.

2. **Chunking & Embedding:**  
   Uploaded documents are:
   - Split into smaller text chunks
   - Converted into **vector embeddings** using OpenAI's `text-embedding` models

3. **Vector Storage:**  
   Embeddings are stored in a **vector database** (like FAISS) for fast similarity search.

4. **Chat Inference:**
   - When a customer sends a message, it's embedded and compared against stored chunks.
   - The most relevant chunks are selected as **context**.
   - The context is fed into OpenAI's **chat completion API** along with the user's question.
   - A tailored, relevant answer is generated based on actual business documents.

> This allows Supportal to **answer domain-specific questions accurately**, beyond what a generic AI model can do.

---

## 🛠️ Tech Stack

- **Backend:** Django + Django Channels
- **Realtime Layer:** Redis (via `channels_redis`)
- **AI Engine:** OpenAI API (GPT + Embeddings)
- **Vector DB:** FAISS (in-memory vector search)

---

## 📦 Getting Started

### 🔧 Prerequisites

- Django 4.2.2
- Channels
- Celery
- Redis
- OpenAI API key

### 🧪 Installation

```bash
Installation guide will be added after publish to pypi
```

## 📄 License
This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.