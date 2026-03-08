# Vox-Live: Real-Time Data Intelligence Dashboard

Vox-Live is a high-performance monitoring interface designed to bridge the gap between raw system logs and actionable intelligence. By leveraging a FastAPI backend and a Streamlit frontend, the platform provides real-time anomaly detection and a multimodal AI interface for data querying.

## Core Capabilities

* **Real-Time Log Synchronization:** Utilizes Streamlit Fragments to achieve independent UI refreshes, ensuring the system event stream and risk index update without full-page reloads.
* **Multimodal Query Engine:** Integrated Groq-powered Whisper-large-v3 for speech-to-text and Llama 3.3 for large language model reasoning.
* **Heuristic Risk Scoring:** Automated parsing of log severity levels (Fatal, Critical, Error) into a visualized Activity Risk Index.
* **Audio Intelligence:** Automated gTTS integration providing verbal synthesis of AI-generated insights.

## Technical Architecture

* **Frontend:** Streamlit, Pandas, CSS Injection
* **Backend:** FastAPI, Uvicorn, Pydantic
* **AI/Inference:** Groq Cloud SDK
* **Communication:** RESTful API (JSON/Multipart)

## Setup and Deployment

### 1. Repository Initialization
```bash
git clone [https://github.com/abhishekbugata/vox-live.git](https://github.com/abhishekbugata/vox-live.git)
cd vox-live
```
### 2. Environment Configuration
It is recommended to use a virtual environment to manage dependencies:
```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```
3. Execution
The application requires both the FastAPI backend and the Streamlit frontend to be running simultaneously.

Step A: Start the Backend Server
Open a terminal and set your API key as an environment variable:
```bash
# Windows (PowerShell)
$env:GROQ_API_KEY="your_actual_groq_key_here"
python backend/main.py

# Mac/Linux or Git Bash
export GROQ_API_KEY="your_actual_groq_key_here"
python backend/main.py
```
Step B: Start the Streamlit Dashboard
Open a second terminal, activate the venv, and run:
```bash
streamlit run frontend/app.py
