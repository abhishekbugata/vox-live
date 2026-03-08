\# Vox-Live: Real-Time Data Intelligence Dashboard



Vox-Live is a high-performance monitoring interface designed to bridge the gap between raw system logs and actionable intelligence. By leveraging a FastAPI backend and a Streamlit frontend, the platform provides real-time anomaly detection and a multimodal AI interface for data querying.



\## Core Capabilities

\* \*\*Real-Time Log Synchronization:\*\* Utilizes Streamlit Fragments to achieve independent UI refreshes, ensuring the system event stream and risk index update without full-page reloads.

\* \*\*Multimodal Query Engine:\*\* Integrated Groq-powered Whisper-large-v3 for speech-to-text and Llama 3.3 for large language model reasoning.

\* \*\*Heuristic Risk Scoring:\*\* Automated parsing of log severity levels (Fatal, Critical, Error) into a visualized Activity Risk Index.

\* \*\*Audio Intelligence:\*\* Automated gTTS integration providing verbal synthesis of AI-generated insights.



\## Technical Architecture

\* \*\*Frontend:\*\* Streamlit, Pandas, CSS Injection

\* \*\*Backend:\*\* FastAPI, Uvicorn, Pydantic

\* \*\*AI/Inference:\*\* Groq Cloud SDK

\* \*\*Communication:\*\* RESTful API (JSON/Multipart)



\## Setup and Deployment

1\. \*\*Repository Initialization\*\*

&nbsp;  ```bash

&nbsp;  git clone \[https://github.com/abhishekbugata/vox-live.git](https://github.com/abhishekbugata/vox-live.git)

&nbsp;  cd vox-live

