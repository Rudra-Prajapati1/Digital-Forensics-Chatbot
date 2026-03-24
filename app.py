import os
import re

from flask import Flask, render_template, request, jsonify
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

CORE BEHAVIOR:
1. Your main focus is Digital Forensics topics.
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
3. If the user sends a greeting, thanks, or brief small talk, reply warmly in 1-2 sentences and invite them to ask a digital forensics question.
4. If the user asks something clearly unrelated to digital forensics, do not answer that request. Politely explain that your focus is digital forensics, then guide them back by suggesting a relevant digital forensics topic they can ask about.
5. Requests for jokes, poems, stories, recipes, entertainment, general knowledge, coding help, or other unrelated tasks must be declined and redirected back to digital forensics.
6. Never make up answers. Never guess. Only use accurate, factual knowledge.
7. Always give clear, well-structured answers with real-world examples where possible.
8. Keep answers informative but easy to understand for a student audience."""

CASUAL_MESSAGES = {
    "hi",
    "hello",
    "hey",
    "hey there",
    "hello there",
    "hii",
    "hiii",
    "yo",
    "sup",
    "whats up",
    "what's up",
    "how are you",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
    "ok",
    "okay",
}

META_MESSAGES = {
    "help",
    "what can you do",
    "what do you do",
    "who are you",
    "what topics can you answer",
    "what topics do you cover",
}

FORENSICS_TERMS = {
    "forensics",
    "forensic",
    "autopsy",
    "wireshark",
    "volatility",
    "cellebrite",
    "encase",
    "kape",
    "regripper",
    "foremost",
    "exiftool",
    "bulk_extractor",
    "ghidra",
    "metadata",
    "steganography",
    "pcap",
    "dns",
    "mft",
    "prefetch",
    "shellbags",
    "registry",
    "malware",
    "ransomware",
    "rootkit",
    "osint",
}

FORENSICS_PHRASES = {
    "digital forensics",
    "digital evidence",
    "file carving",
    "hash value",
    "hash values",
    "slack space",
    "network forensics",
    "mobile forensics",
    "memory forensics",
    "windows forensics",
    "incident response",
    "chain of custody",
    "faraday bag",
    "event logs",
    "lnk files",
    "recycle bin",
    "forensic image",
    "firewall logs",
    "lateral movement",
    "data exfiltration",
    "fileless malware",
    "deepfake forensics",
    "blockchain forensics",
    "cloud forensics",
    "iot forensics",
    "mitre attack",
    "section 65b",
    "it act 2000",
    "cert in",
    "ftk imager",
}

OUT_OF_SCOPE_RESPONSE = (
    "I can't help with that because this assistant is limited to digital "
    "forensics topics. You can ask about evidence analysis, forensic tools, "
    "malware investigation, network forensics, or mobile forensics."
)


def normalize_message(text):
    cleaned = re.sub(r"[^\w\s']", " ", text.lower())
    return " ".join(cleaned.split())


def is_casual_message(text):
    return normalize_message(text) in CASUAL_MESSAGES


def is_meta_message(text):
    return normalize_message(text) in META_MESSAGES


def is_digital_forensics_related(text):
    normalized = normalize_message(text)
    tokens = set(normalized.split())

    if any(term in tokens for term in FORENSICS_TERMS):
        return True

    return any(phrase in normalized for phrase in FORENSICS_PHRASES)


def should_reject_as_out_of_scope(text):
    normalized = normalize_message(text)

    if (
        is_casual_message(normalized)
        or is_meta_message(normalized)
        or is_digital_forensics_related(normalized)
    ):
        return False

    return True


def is_redirect_response(text):
    lowered = text.lower()
    redirect_markers = [
        "my focus is digital forensics",
        "i focus on digital forensics",
        "i'm focused on digital forensics",
        "i am focused on digital forensics",
        "i specialize in digital forensics",
        "i am specialized in digital forensics",
        "please ask a digital forensics question",
        "ask a digital forensics question",
        "related to digital forensics",
    ]
    return any(marker in lowered for marker in redirect_markers)


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

        if is_casual_message(user_question) or is_meta_message(user_question):
            return jsonify({
                "answer": (
                    "Hello! I am here to help with digital forensics topics such as "
                    "evidence analysis, forensic tools, malware investigation, and "
                    "network or mobile forensics. What would you like to explore?"
                ),
                "out_of_scope": False
            })

        if should_reject_as_out_of_scope(user_question):
            return jsonify({
                "answer": OUT_OF_SCOPE_RESPONSE,
                "out_of_scope": True
            })

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
        is_out_of_scope = is_redirect_response(answer)

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
