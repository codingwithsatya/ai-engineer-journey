# Aria — AI Chatbot

A full-stack AI chatbot with streaming responses, multi-turn conversation memory, and a clean Next.js UI. Built with the Claude API and deployed on Vercel + Railway.

**🔗 Live demo:** https://project-pv9qy.vercel.app

![Claude API](https://img.shields.io/badge/Built%20with-Claude%20API-blue) ![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green) ![Next.js](https://img.shields.io/badge/Frontend-Next.js-black)

---

## Features

- **Streaming responses** — text appears word by word, not all at once
- **Multi-turn memory** — full conversation history maintained across turns
- **Context window guard** — automatically trims history to prevent token overflow
- **Markdown rendering** — bold, bullets, headers, and code blocks rendered correctly
- **Real-time UI** — React state updates as each token streams in

---

## Tech Stack

| Layer      | Technology                                          |
| ---------- | --------------------------------------------------- |
| Frontend   | Next.js 16, TypeScript, Tailwind CSS, ReactMarkdown |
| Backend    | Python, FastAPI, Uvicorn                            |
| AI         | Claude API (claude-sonnet-4-6)                      |
| Deployment | Vercel (frontend) + Railway (backend)               |

---

## How It Works

1. User types a message in the Next.js UI
2. Frontend appends the message to conversation history and POSTs full history to FastAPI
3. FastAPI opens a streaming connection to the Claude API
4. Claude streams tokens back through FastAPI via `StreamingResponse`
5. Frontend reads the stream chunk by chunk using `ReadableStream` and updates the UI in real time
6. Assistant reply is appended to history for the next turn

**Key engineering decisions:**

- Full conversation history sent on every request (Claude API is stateless)
- `MAX_HISTORY = 20` sliding window prevents unbounded token growth
- `StreamingResponse` with `media_type="text/plain"` pipes Claude output directly to browser
- `CORSMiddleware` allows the Vercel frontend to call the Railway backend

---

## Project Structure

```
ai-engineer-journey/
├── main.py              # FastAPI backend — POST /chat streaming endpoint
├── chatbot.py           # Terminal chatbot with memory + streaming (dev tool)
├── requirements.txt     # anthropic, fastapi, uvicorn, python-dotenv
├── nixpacks.toml        # Railway deployment config
├── .env                 # ANTHROPIC_API_KEY (not committed)
└── aria-chat/
    ├── app/
    │   └── page.tsx     # Next.js chat UI with streaming fetch
    └── vercel.json      # Vercel deployment config
```

---

## Running Locally

**Backend**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API key to .env
echo "ANTHROPIC_API_KEY=your_key_here" > .env

uvicorn main:app --reload
# Runs on http://localhost:8000
```

**Frontend**

```bash
cd aria-chat
npm install
npm run dev
# Runs on http://localhost:3000
```

---

## API Endpoints

### `POST /chat`

Stream a response given a conversation history.

**Request**

```json
{
  "messages": [
    { "role": "user", "content": "What is the capital of France?" },
    { "role": "assistant", "content": "The capital of France is Paris." },
    { "role": "user", "content": "What's the population?" }
  ]
}
```

**Response**
Plain text stream — chunks arrive as the model generates them.

---

### `GET /health`

```json
{ "status": "ok" }
```

---

## Key Code Patterns

**Streaming endpoint**

```python
@app.post("/chat")
def chat(request: ChatRequest):
    def stream_response():
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[m.dict() for m in request.messages]
        ) as stream:
            for text in stream.text_stream:
                yield text
    return StreamingResponse(stream_response(), media_type="text/plain")
```

**Streaming fetch in Next.js**

```typescript
const reader = response.body.getReader();
const decoder = new TextDecoder();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  assistantText += decoder.decode(value);
  setMessages([...history, { role: "assistant", content: assistantText }]);
}
```

**Context window guard**

```python
MAX_HISTORY = 20
def trim_history(history):
    if len(history) > MAX_HISTORY:
        return history[-MAX_HISTORY:]
    return history
```

---

## Deployment

**Backend → Railway**

- Push to GitHub — Railway auto-deploys
- Set `ANTHROPIC_API_KEY` in Railway environment variables
- `nixpacks.toml` handles the Python venv start command

**Frontend → Vercel**

- Set Root Directory to `aria-chat` in Vercel project settings
- Auto-deploys on every push to main

---

## Built as part of a 6-month AI Engineering curriculum

This project is Week 2 of a structured learning path from full-stack developer to AI engineer.
Follow the journey: [@codingwithsatya](https://github.com/codingwithsatya)
