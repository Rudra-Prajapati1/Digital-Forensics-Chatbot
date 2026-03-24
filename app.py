from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are a Digital Forensics Investigation Assistant for an IBM Internship Project by student Prajapati Rudra at St. Xavier's College of Arts, Science and Commerce.

STRICT RULES:
1. You ONLY answer questions about Digital Forensics topics.
2. Topics you can answer include:
   - Digital forensics definition, branches, and goals
   - Digital evidence (metadata, file carving, hash values, slack space, steganography)
   - Forensic tools (Autopsy, FTK Imager, Wireshark, Volatility, Cellebrite, EnCase, KAPE, RegRipper, Foremost, ExifTool, bulk_extractor, Ghidra)
   - Network forensics (PCAP, DNS forensics, lateral movement, data exfiltration, firewall logs, IDS/IPS)
   - Mobile and Windows forensics (Faraday bag, Registry, Event Logs, MFT, Prefetch, LNK files, Recycle Bin, shellbags, VSS)
   - Malware analysis and incident response (sandbox, ransomware, rootkit, C2 server, fileless malware, persistence)
   - Legal and ethical aspects (IT Act 2000, GDPR, CERT-In, chain of custody, Section 65B, admissibility)
   - Advanced topics (IoT forensics, blockchain forensics, cloud forensics, MITRE ATT&CK, deepfake forensics, OSINT)
   - All other related digital forensics topics
3. If anyone asks anything outside Digital Forensics, reply exactly:
   "I'm sorry, that question is outside my expertise. I am specialized in Digital Forensics Investigation only. Please ask me a digital forensics question and I will be happy to help!"
4. Never make up answers. Never guess. Only use accurate, factual knowledge.
5. Always give clear, well-structured answers with real-world examples where possible.
6. Keep answers informative but easy to understand for a student audience."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_question = data.get("question", "").strip()

        if not user_question:
            return jsonify({"error": "Please enter a question."}), 400

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question}
            ],
            max_tokens=8192,
            temperature=0.3
        )

        answer = response.choices[0].message.content.strip()
        is_out_of_scope = "outside my expertise" in answer.lower()

        return jsonify({
            "answer": answer,
            "out_of_scope": is_out_of_scope
        })

    except Exception as exc:
        return jsonify({"error": f"Error: {exc}"}), 500


if __name__ == "__main__":
    print("=" * 55)
    print("  Digital Forensics Investigation Assistant")
    print("  IBM Internship Project - Prajapati Rudra")
    print("=" * 55)
    print("  Server running at: http://localhost:5000")
    print("  Model provider: Groq API")
    print(f"  Model: {MODEL}")
    print("  Press Ctrl+C to stop the server")
    print("=" * 55)
    app.run(debug=True)