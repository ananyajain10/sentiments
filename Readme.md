
# Reddit Sentiment Analysis API

A FastAPI backend service that analyzes the sentiment of **raw text** or **Reddit posts/comments**.  
Supports **batch processing** and **logging** for debugging.

---

## Features
- Accepts **raw text** or a **Reddit post/comment URL**
- Uses **VADER Sentiment Analysis** (fast, social-media friendly)
- Returns **sentiment label** (`positive`, `negative`, `neutral`) and **confidence score**
- **Batch processing**: send multiple texts/URLs in one request
- **Logs** all requests and responses to `api.log`
- Environment‑based secret management (no hardcoded credentials)

---

## Requirements
- Python 3.9+
- Reddit API credentials (free to create)

---

## Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/reddit-sentiment-analysis.git
cd reddit-sentiment-analysis
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create a Reddit App
1. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
2. Click **Create another app**
3. Choose **script** type
4. Fill in:
   - **Name:** sentiment-analysis
   - **Redirect URI:** http://localhost:8080
5. Save and note your `client_id` and `client_secret`

---

### 5️⃣ Create a `.env` file
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=sentiment-analyser by u/yourusername
```

---

### 6️⃣ Run the API
```bash
uvicorn main:app --reload
```
Visit the interactive docs at:  
**http://127.0.0.1:8000/docs**

---

## Usage

### **POST** `/analyze`

#### Request Body (Batch Example)
```json
[
  {
    "text": "hate to love this world",
    "url": "https://www.reddit.com/r/Backend/comments/1nkhle5/which_backend_should_i_focus_on_for_the_future/"
  },
  {
    "text": "This is amazing!"
  },
  {
    "url": "https://www.reddit.com/r/Python/comments/abc123/some_post/"
  }
]
```

#### Example `curl` Command
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
-H "Content-Type: application/json" \
-d '[{"text":"I love this!"},{"url":"https://www.reddit.com/..."}]'
```

#### Example Response
```json
{
    "results": [
        {
            "source": "raw",
            "text": "hate to love this world",
            "label": "positive",
            "confidence": 0.128,
            "model": "VADER"
        },
        {
            "source": "reddit",
            "url": "https://www.reddit.com/r/Backend/comments/1nkhle5/which_backend_should_i_focus_on_for_the_future/",
            "text": "Which backend should I focus on for the future job market?\nHey everyone,  \nI’m a CS grad trying to specialize in backend development. There are so many options—Java Spring Boot, Node.js/Express, Django/FastAPI, Go, etc.—and I want to focus on something that’s in demand globally (especially in Europe and remote jobs).\n\nIf you’re working in the industry, could you share your experience on which backend frameworks/tech stacks companies are actually hiring for right now and what has good long-term career potential?\n\nWould appreciate recommendations from people actually in the field 🙏",
            "label": "positive",
            "confidence": 0.788,
            "model": "VADER"
        },
        {
            "source": "raw",
            "text": "This is amazing!",
            "label": "positive",
            "confidence": 0.624,
            "model": "VADER"
        },
        {
            "source": "reddit",
            "url": "https://www.reddit.com/r/Python/comments/abc123/some_post/",
            "text": "My roommates always come in my room to hang out while I’m trying to write so I post this on my door now\n[removed]",
            "label": "neutral",
            "confidence": 0.0,
            "model": "VADER"
        }
    ]
}
```

---

## Logging
- All requests and responses are logged to `api.log` in the project root.
- Each log entry includes a timestamp and request ID.

---