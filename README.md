# task2cal
Convert text-based assignments into calendar events automatically.  This app extracts tasks and deadlines from natural language (including Finnish) and generates a downloadable .ics calendar file.


Seminaarityönä Ohjelmistokehityksen teknologioita -kurssille tehty sovellus, joka muuntaa luonnollisella kielellä kirjoitetut tehtävänannot automaattisesti kalenterimerkinnöiksi (.ics-muotoon).

Alla oleva osuus README:sta generoitu tekoälyllä:


# 📚 Task → Calendar

Convert text-based assignments into calendar events automatically.

This app extracts tasks and deadlines from natural language (including Finnish) and generates a downloadable `.ics` calendar file.

---

## 🚀 Features

* Extracts tasks from plain text
* Supports Finnish natural language dates
  (e.g. *"maanantaina 27. huhtikuuta 2026, 22.00"*)
* Generates `.ics` calendar files
* Supports:

  * Local LLMs via Ollama
  * Cloud LLM via Google Gemini
* Fallback logic for unreliable AI output

---

## 🧠 Tech Stack

* Python
* Streamlit
* dateparser
* ICS (calendar generation)
* Ollama (local models)
* Google Gemini API

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/bhu574/task2cal.git
cd task2cal
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements file, install manually:

```bash
pip install streamlit dateparser ics google-generativeai ollama
```

---

### 3. Install Ollama (optional, for local models)

Install Ollama from: https://ollama.com

Pull at least one model:

```bash
ollama pull phi3
```

Optional (better quality):

```bash
ollama pull gemma2:2b  (<- recommended)
ollama pull mistral
ollama pull llama3
```

---

### 4. Setup Gemini API (optional, for cloud model)

Get API key from Google AI Studio and set environment variable:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

(macOS / Linux)

---

## ▶️ Running the app

```bash
streamlit run app.py
```

---

## 🧪 Example input

```
Palautettava viimeistään: maanantaina 27. huhtikuuta 2026, 22.00
Historian essee 10.5
```

---

## 📅 Output

* Extracted tasks
* Structured JSON data
* Downloadable `.ics` calendar file

---

## 💡 Notes

* Local models are faster and private
* Gemini provides better accuracy in some cases
* Date parsing includes preprocessing for Finnish formats

---

## 📌 Future improvements

* OCR (image → tasks)
* smarter deadline detection

---
