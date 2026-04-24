# Real-Time AI Voice Agent - Recall.ai Integration

A modern web application featuring real-time voice conversations using OpenAI's Real-time API, integrated with Recall.ai for meeting participation.

## Architecture

- **Backend**: Python WebSocket server that relays messages between the browser and OpenAI's Real-time API
- **Frontend**: HTML/JavaScript client that handles audio I/O and WebSocket communication
- **Integration**: Works with Recall.ai's Output Media feature for meeting participation

## Prerequisites

- Python 3.8+
- OpenAI API Key (with credits)
- Ngrok (for exposing local server to internet)
- Recall.ai API Key

## Local Setup

### 1. Clone and Install

```bash
cd /home/soumarshinagbiswas/11labsAgent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Start Server Locally

```bash
python server.py
```

Server will run on `ws://localhost:3000`

### 4. Test Locally

Open `index.html` in your browser. The client will try to connect to `ws://localhost:3000`.

## Deploy to Internet with Ngrok

### 1. Install Ngrok

[Download from ngrok.com](https://ngrok.com/download)

### 2. Expose Server

In a separate terminal:

```bash
ngrok http 3000
```

This will give you a URL like: `wss://xxxx-xx-xxxx-xxx.ngrok-free.app`

## Deploy Frontend to GitHub Pages

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Add real-time AI agent with backend server"
git push origin main
```

### 2. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Select **main** branch and **/(root)** folder
3. Click Save

## Use with Recall.ai

### 1. Create a Bot in Recall.ai

Replace placeholders and run:

```bash
curl --request POST \
  --url https://us-west-2.recall.ai/api/v1/bot/ \
  --header 'Authorization: Token YOUR_RECALL_TOKEN' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{
    "meeting_url": "https://meet.google.com/YOUR_MEETING_URL",
    "bot_name": "AI Agent",
    "output_media": {
      "camera": {
        "kind": "webpage",
        "config": {
          "url": "https://soumarshi.github.io/11labsAgent?wss=wss://YOUR_NGROK_URL"
        }
      }
    },
    "variant": {
      "zoom": "web_4_core",
      "google_meet": "web_4_core",
      "microsoft_teams": "web_4_core"
    }
  }'
```

**Important**: 
- Replace `YOUR_RECALL_TOKEN` with your Recall.ai API token
- Replace `YOUR_MEETING_URL` with the actual meeting URL
- Replace `YOUR_NGROK_URL` with your ngrok URL (from step 2 above)
- Replace `soumarshi` with your GitHub username in the URL

## How It Works

1. **Browser connects** to the backend via WebSocket
2. **Audio input**: Browser captures microphone and sends to backend
3. **Backend relays** to OpenAI's Real-time API
4. **OpenAI responds** with audio and text
5. **Backend relays** back to browser
6. **Browser plays** audio response

## Environment Variables

```
OPENAI_API_KEY=sk-...          # Your OpenAI API key
PORT=3000                       # WebSocket server port (default: 3000)
```

## Troubleshooting

### Bot doesn't speak in meeting
- Ensure OpenAI account has credits
- Check that server is running (`python server.py`)
- Verify ngrok URL is correct in Recall.ai bot config
- Check browser console for connection errors (F12 → Console)

### Connection refused
- Start the backend server: `python server.py`
- Expose with ngrok: `ngrok http 3000`
- Pass correct `wss` parameter to frontend

### No audio from browser
- Check microphone permissions
- Ensure audio context is not suspended
- Check browser console for audio errors

## File Structure

```
11labsAgent/
├── index.html          # Frontend client
├── styles.css          # UI styling
├── server.py           # WebSocket relay server
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .env                # Local environment (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Flow

```
Browser ←→ WebSocket Server ←→ OpenAI Real-time API
  ↓            ↓
Audio I/O   Relay              ↓
            Messages         GPT-4 Realtime
```

## Security Notes

- Never commit `.env` file with API keys
- Use environment variables for secrets
- Ngrok URLs are temporary - regenerate when needed
- Restrict Recall.ai bot to specific meetings

## References

- [OpenAI Real-time API Docs](https://platform.openai.com/docs/guides/realtime)
- [Recall.ai Documentation](https://docs.recall.ai/)
- [WebSocket Protocol](https://tools.ietf.org/html/rfc6455)

## License

MIT License - See LICENSE file for details

---

**Created**: April 2026 | **Updated**: April 2026

