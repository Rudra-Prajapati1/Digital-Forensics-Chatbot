# 🔍 Digital Forensics Investigation Assistant

A professional Flask-based web application that answers digital forensics questions using the Groq API with an OpenAI-compatible client. The chatbot is designed for educational use and remains strictly limited to digital forensics topics, declining unrelated queries.

## Overview

The Digital Forensics Investigation Assistant helps students and learners explore important digital forensics concepts such as digital evidence, forensic tools, malware analysis, network forensics, mobile forensics, and legal or ethical considerations. It is built as a simple, student-friendly web app for interactive learning.

## Features

- Answers questions related only to digital forensics
- Rejects unrelated questions with a clear out-of-scope response
- Built with Flask for a lightweight and easy-to-run backend
- Uses the Groq API with the `llama-3.3-70b-versatile` model
- Loads environment variables securely with `python-dotenv`
- Provides a clean web interface using HTML, CSS, and JavaScript
- Suitable for learning, demonstration, and internship project submission

## Tech Stack

- Python
- Flask
- Groq API
- OpenAI Python SDK
- HTML
- CSS
- JavaScript
- `python-dotenv`

## Folder Structure

```text
Digital-Forensics-Chatbot/
|-- static/
|   |-- Script.js
|   `-- Style.css
|-- templates/
|   `-- index.html
|-- app.py
|-- .env
|-- .env.example
|-- requirements.txt
`-- README.md
```

## Installation And Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Digital-Forensics-Chatbot
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root, or copy `.env.example` and update it with your Groq API key.

Example `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

If you want to copy the example file directly:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

## How To Run The App

Start the Flask application with:

```bash
python app.py
```

Then open your browser and visit:

```text
http://localhost:5000
```

## Disclaimer

This project was developed as part of the IBM SkillsBuild Internship 2025-26 by Prajapati Rudra from St. Xavier's College of Arts, Science and Commerce (SXCA), Ahmedabad. It is intended for educational and demonstration purposes.
