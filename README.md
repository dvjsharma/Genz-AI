# 🚀 InstaiQ

**InstaiQ** is a query-driven platform designed to simplify Instagram engagement analysis by providing data-driven insights. The platform fetches detailed Instagram data, including likes, comments, and engagement rates, using the Instaloader API. This data is securely stored in **DataStax Astra DB**, ensuring scalable and efficient data management.

Leveraging **Langflow** for advanced query processing, InstaiQ allows users to ask specific, natural-language questions such as:

- ❓ *“What is the average like count on my reels last month?”*
- ❓ *“Which type of post (static-image, reel, or carousel) gets the highest average likes?”*

The platform processes these queries using powerful AI models to deliver actionable insights instantly, empowering **content creators**, **marketers**, and **businesses** to optimize their content strategies effectively.

---
## 📸 UI Reference
![Home Page](https://github.com/user-attachments/assets/d3691805-3c67-4619-92b2-930d4ce3e5ab)

![Connect To Instagram](https://github.com/user-attachments/assets/2f6130df-c896-498a-89a1-d3e5ce06b4e2)

![Chat Page](https://github.com/user-attachments/assets/721eadef-f031-4182-8e83-83116d41794d)

## 🌐 Live Deployment
🔗 [InstaiQ Live Deployment](https://genz-ai.dvjshx.club/)

## 🎥 Demo Video
🔗 [InstaiQ Demo Video](https://youtu.be/aIZm0bwVQrA)

---

## 🧑‍💻 Technologies Used

- 🤖 **Hugging Face Embedding Models:** For data embedding and analysis.
- 📦 **DataStax Astra DB:** For efficient vector storage and data retrieval.
- 🧠 **Gemini & Langflow:** To build modular and scalable query pipelines.
- 🐍 **Flask:** For backend API management and data flow handling.
- ⚡ **Next.js:** For dynamic and responsive frontend development.
- 🎨 **Tailwind CSS:** Styled for a modern, mobile-friendly experience.

---

## 🌟 Features

- 📊 **Fetching Real-Time Data:** Fetch and store Instagram data in an organized manner using **Instaloader API**.
- 📈 **Engagement Analytics:** Compare post performances across reels, carousels, and static images.
- 🧩 **AI-Powered Insights:** Receive personalized recommendations based on engagement patterns.
- 📦 **Scalable Storage:** Uses **DataStax Astra DB** for low-latency storage and retrieval.

---

## 🛠️ Installation

### ⚡ Prerequisites
- ✅ Node.js, Flask installed.
- ✅ Access to **DataStax Astra DB**.

### 🖥️ Backend Setup (Flask)

```bash
git clone https://github.com/dvjsharma/Genz-AI.git
cd Genz-AI
python -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

### 🌐 Frontend Setup (Next.js)

```bash
cd src
npm install --legacy-peer-deps 
npm run dev
```

### 📦 Environment Variables
Create a `.env` file in the **root directory** with the following keys:

```plaintext
ASTRA_DB_API_ENDPOINT=<your-astra-db-api-endpoint>
ASTRA_DB_APPLICATION_TOKEN=<your-astra-db-application-token>
KEYSPACE=<your-keyspace-name>
ASTRA_DB_COLLECTION_NAME=<your-collection-name>
LANGFLOW_ID=<your-langflow-id>
ENDPOINT=<your-langflow-endpoint>
```

---

## ✅ How to Use

1. **Enter Instagram Handle:** Provide your Instagram handle to fetch your engagement data.
2. **Query Your Data:** Ask queries like *"What is the most liked post this month?"*
3. **Get Insights:** InstaiQ provides instant, data-driven insights to help you optimize your content strategy.

---

## 👨‍👩‍👧‍👦 Team

- [**Divij Sharma**](https://www.linkedin.com/in/dvjsharma)
- [**Gaurangi Bansal**](https://www.linkedin.com/in/gaurangi-bansal/)
- [**Samriddhi Sharma**](https://www.linkedin.com/in/samriddhi-sharma-b07b81254/)
- [**Akash Kumar Sah**](https://www.linkedin.com/in/akashsah2003)

---
