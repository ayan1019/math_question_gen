
# 📚 Automated Curriculum-Aligned Question Generation

This project implements an **AI-powered question generation system** that creates curriculum-aligned multiple-choice questions (MCQs) in the **exact format** specified in the provided assignment PDF.

---


## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clonehttps://github.com/ayan1019/ML_assignment.git
cd ML_assignment
```

### 2. Create & Activate Virtual Environment

```bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```
### 4. Set your OpenAI API key
#### Create a .env file:
```bash
OPENAI_API_KEY=sk-your-api-key

```



### 5. Run the generator

```
python3 src/generator_llm.py

```
---

## 🛠️ Tech Stack

- Python 3.10+

- OpenAI API (openai==0.28 for compatibility)

- matplotlib & Pillow for diagrams

- python-docx for Word export

- dotenv for environment variables

---

### 👨‍💻 Author
#### Ayan Yadav
#### Data Science & AI Enthusiast


