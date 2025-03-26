# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Modern customers expect highly personalized experiences that cater to their unique preferences. This is a Generative Al-driven solution that enhances hyper-personalization by analyzing customer profiles, social media activity, purchase history, sentiment data, and demographic details. According to the challenge we have to design a system that generates personalized recommendations for products, services, or content while also providing actionable insights for businesses to optimize customer engagement.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)
![image](https://github.com/user-attachments/assets/b7b7cf9e-5f69-4763-897f-bfa4306fcc4f)


## 💡 Inspiration
In the era of hyper-personalization, users expect financial services tailored to their specific behaviors, needs, and lifestyles. This project was inspired by the growing demand for AI-driven financial advisory tools that not only recommend products but also optimize user engagement and service delivery. We wanted to build a solution that understands each customer like a human advisor would—learning from their actions and adapting in real time.

## ⚙️ What It Does
This system delivers:

🎯 Personalized financial product recommendations (cards, loans, investments)

🤖 AI-rephrased, user-friendly suggestions using Hugging Face LLMs

📈 AI-driven insights for user engagement, product discovery, and service optimization

🔄 Dynamic recommendation updates based on user feedback

💬 Real-time feedback loop to fine-tune the personalization

## 🛠️ How We Built It
We combined machine learning (for customer clustering) with rule-based recommendations and LLM-powered rephrasing. Flask powers the backend APIs, while a React frontend gives users an intuitive interface to receive and refine their financial advice. We also integrated Hugging Face Inference API to generate human-like recommendation text.

## 🚧 Challenges We Faced
Setting up proper CORS handling between Flask and React

Getting consistent, relevant outputs from LLMs (like flan-t5-large)

Dynamically updating recommendations based on vague user feedback

Managing data quality and simulating realistic financial personas

## 🏃 How to Run
1. Clone the repository  
   git clone https://github.com/ewfx/gaidp-data-rapids.git
   cd gaidp-data-rapids/code
2. Set up the backend 
   pip install -r requirements.txt
   python app.py
3. Setup the frontend  
   cd frontend
   npm install
   npm start

## 🏗️ Tech Stack
🔹 Frontend: React

🔹 Backend: Flask

🔹 Modeling: scikit-learn, pandas

🔹 AI/NLP: Hugging Face Transformers (flan-t5-large)

🔹 Others: Axios, Flask-CORS, Joblib

## 👥 Team
- Akash Singh
- Vaishnavi Srivastav
- Mehak M
- Poorna Hegde
