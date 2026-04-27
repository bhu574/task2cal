import streamlit as st
import json
import re
import os
from ics import Calendar, Event
import dateparser
from datetime import datetime

# ===== CONFIG =====
MODEL_GEMINI = "gemini-flash-lite-latest"


# ===== OLLAMA MODEL LIST =====
def get_ollama_models():
    import subprocess

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.strip().split("\n")

        models = []
        for line in lines[1:]:  # skip header
            parts = line.split()
            if parts:
                models.append(parts[0])

        return models if models else ["phi3"]

    except Exception as e:
        print("Ollama list error:", e)
        return ["phi3"]


# ===== LLM: OLLAMA =====
def call_ollama(text, model):
    import ollama

    prompt = f"""
Poimi kaikki tehtävät tekstistä.

Palauta JSON-lista:
[
  {{
    "title": "...",
    "deadline": "...",
    "description": "..."
  }}
]

Palauta VAIN JSON.

Teksti:
{text}
"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


# ===== LLM: GEMINI =====
def call_gemini(text):
    import google.generativeai as genai

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(MODEL_GEMINI)

    prompt = f"""
Poimi kaikki tehtävät tekstistä.

Palauta JSON-lista:
[
  {{
    "title": "...",
    "deadline": "...",
    "description": "..."
  }}
]

Palauta VAIN JSON.

Teksti:
{text}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"


# ===== JSON PARSINTA =====
def extract_json(text):
    text = re.sub(r"```json|```", "", text)

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        json_str = match.group(0)
    else:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            json_str = "[" + match.group(0) + "]"
        else:
            return []

    json_str = json_str.replace("\n", " ")
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    try:
        return json.loads(json_str)
    except:
        return []


# ===== FINNISH DATE PREPROCESS =====
def preprocess_finnish_date(text):
    if not text:
        return text

    text = text.lower()

    weekdays = [
        "maanantaina", "tiistaina", "keskiviikkona",
        "torstaina", "perjantaina", "lauantaina", "sunnuntaina"
    ]
    for d in weekdays:
        text = text.replace(d, "")

    months = {
        "tammikuuta": "01",
        "helmikuuta": "02",
        "maaliskuuta": "03",
        "huhtikuuta": "04",
        "toukokuuta": "05",
        "kesäkuuta": "06",
        "heinäkuuta": "07",
        "elokuuta": "08",
        "syyskuuta": "09",
        "lokakuuta": "10",
        "marraskuuta": "11",
        "joulukuuta": "12",
    }

    for name, num in months.items():
        text = text.replace(name, num)

    text = text.replace(",", " ")
    text = re.sub(r"\s+", " ", text)

    # 22.00 → 22:00
    text = re.sub(r"(\d{1,2})\.(\d{2})", r"\1:\2", text)

    return text.strip()


# ===== NORMALIZE DATETIME =====
def normalize_datetime(dt, original_text=""):
    if not dt:
        return None

    has_time = bool(re.search(r"\d{1,2}[:.]\d{2}", original_text))

    if not has_time:
        dt = dt.replace(hour=23, minute=59)

    return dt.strftime("%Y-%m-%d %H:%M")


# ===== DATE PARSING =====
def fill_missing_dates(tasks):
    for t in tasks:
        raw_deadline = t.get("deadline", "")
        description = t.get("description", "")

        parsed = None

        # 1. deadline
        if raw_deadline:
            cleaned = preprocess_finnish_date(raw_deadline)
            parsed = dateparser.parse(
                cleaned,
                languages=["fi", "en"],
                settings={"PREFER_DATES_FROM": "future"}
            )

        # 2. description
        if not parsed:
            cleaned = preprocess_finnish_date(description)
            parsed = dateparser.parse(
                cleaned,
                languages=["fi", "en"],
                settings={"PREFER_DATES_FROM": "future"}
            )

        # 3. combined fallback
        if not parsed:
            combined = raw_deadline + " " + description
            cleaned = preprocess_finnish_date(combined)
            parsed = dateparser.parse(
                cleaned,
                languages=["fi", "en"],
                settings={"PREFER_DATES_FROM": "future"}
            )

        if parsed:
            source = raw_deadline if raw_deadline else description
            t["deadline"] = normalize_datetime(parsed, source)
        else:
            print("⚠️ Ei tunnistettu:", raw_deadline)
            t["deadline"] = ""

    return tasks


# ===== REGEX FALLBACK =====
def regex_extract_tasks(text):
    tasks = []
    for line in text.split("\n"):
        if line.strip():
            tasks.append({
                "title": line[:60],
                "deadline": "",
                "description": line
            })
    return tasks


# ===== VALIDATION =====
def is_valid(tasks):
    return isinstance(tasks, list) and any(t.get("title") for t in tasks)


# ===== ICS =====
def create_ics(tasks):
    cal = Calendar()

    for t in tasks:
        if not t.get("deadline"):
            continue

        e = Event()
        e.name = t["title"]

        try:
            dt = datetime.strptime(t["deadline"], "%Y-%m-%d %H:%M")
            e.begin = dt
        except:
            print("Virheellinen päivämäärä:", t["deadline"])
            continue

        e.description = t["description"]
        cal.events.add(e)

    return str(cal)


# ===== UI =====
st.title("📚 Task → Calendar")

mode = st.radio("Valitse malli:", ["Paikallinen (Ollama)", "Pilvi (Gemini)"])

selected_model = None

if mode.startswith("Paikallinen"):
    models = get_ollama_models()
    selected_model = st.selectbox("Valitse paikallinen malli:", models)

text = st.text_area("Liitä tehtävänanto tähän:", height=200)

if st.button("Käsittele"):
    if not text.strip():
        st.warning("Syötä teksti")
        st.stop()

    with st.spinner("Analysoidaan..."):

        if mode.startswith("Paikallinen"):
            raw = call_ollama(text, selected_model)
        else:
            raw = call_gemini(text)

        st.subheader("🔍 RAW")
        st.code(raw)

        tasks = extract_json(raw)

        if not is_valid(tasks):
            st.warning("LLM epäonnistui → fallback")
            tasks = regex_extract_tasks(text)

        tasks = fill_missing_dates(tasks)

        st.subheader("📦 Tulkittu data")
        st.json(tasks)

        ics_data = create_ics(tasks)

        st.download_button(
            "📅 Lataa kalenteri (.ics)",
            data=ics_data,
            file_name="tehtavat.ics",
            mime="text/calendar"
        )