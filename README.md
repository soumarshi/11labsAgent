# Real-Time 11Labs Voice Agent - Recall.ai Integration

A modern web application featuring real-time voice conversations using 11Labs' ConvAI Agent, integrated with Recall.ai for meeting participation.

## Architecture

- **Backend**: Python WebSocket server that relays messages between the browser and 11Labs ConvAI API
- **Frontend**: HTML/JavaScript client that handles audio I/O and WebSocket communication
- **Integration**: Works with Recall.ai's Output Media feature for meeting participation
- **Voice Agent**: 11Labs ConvAI AI voice agent with natural conversations

## Prerequisites

- Node.js 14+ and npm
- 11Labs API Key (with ConvAI agent created)
- Ngrok (for exposing local server to internet)
- Recall.ai API Key

## Local Setup

### 1. Clone and Install

```bash
cd /home/soumarshinagbiswas/11labsAgent
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your 11Labs API key:

```bash
cp .env.example .env
# Edit .env and add your ELEVENLABS_API_KEY
```

Get your 11Labs API key from: https://elevenlabs.io/app/settings/api-keys

### 3. Start Server Locally

```bash
npm start
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
git commit -m "Add 11Labs ConvAI agent with Recall.ai integration"
git push origin main
```

### 2. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Select **main** branch and **/(root)** folder
3. Click Save

## Use with Recall.ai

### 1. Create 11Labs Agent

1. Go to https://elevenlabs.io/app/conversational-ai/agents
2. Create a new agent or use existing one
3. Note the agent ID (e.g., `agent_4101kne33jyvef3rjxyfhd1kyyp0`)

### 2. Create a Bot in Recall.ai

Replace placeholders and run:

```bash
curl --request POST \
  --url https://us-west-2.recall.ai/api/v1/bot/ \
  --header 'Authorization: Token YOUR_RECALL_TOKEN' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{
    "meeting_url": "https://meet.google.com/YOUR_MEETING_URL",
    "bot_name": "11Labs AI Agent",
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
3. **Backend relays** to 11Labs ConvAI API
4. **11Labs responds** with audio from the AI voice agent
5. **Backend relays** back to browser
6. **Browser plays** audio response

## Environment Variables

```
ELEVENLABS_API_KEY=xi_...         # Your 11Labs API key
ELEVENLABS_AGENT_ID=agent_...    # Your ConvAI agent ID (optional, defaults to included agent)
PORT=3000                          # WebSocket server port (default: 3000)
```

## Troubleshooting

### Bot doesn't speak in meeting
- Ensure 11Labs agent is active and configured properly
- Check that server is running (`python server.py`)
- Verify ngrok URL is correct in Recall.ai bot config
- Check browser console for connection errors (F12 → Console)

### Connection refused
- Start the backend server: `npm start`
- Expose with ngrok: `ngrok http 3000`
- Pass correct `wss` parameter to frontend

### No audio from browser
- Check microphone permissions
- Ensure audio context is not suspended
- Check browser console for audio errors
- Verify 11Labs agent is online

## File Structure

```
11labsAgent/
├── index.html          # Frontend client
├── styles.css          # UI styling
├── server.js           # WebSocket relay server (Node.js)
├── package.json        # Node.js dependencies
├── .env.example        # Environment template
├── .env                # Local environment (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Flow

```
Browser ←→ WebSocket Server ←→ 11Labs ConvAI API
  ↓            ↓
Audio I/O   Relay              ↓
            Messages         AI Voice Agent
```

## Security Notes

- Never commit `.env` file with API keys
- Use environment variables for secrets
- Ngrok URLs are temporary - regenerate when needed
- Restrict Recall.ai bot to specific meetings

## References

- [11Labs API Documentation](https://elevenlabs.io/docs)
- [11Labs ConvAI Agents](https://elevenlabs.io/app/conversational-ai/agents)
- [Recall.ai Documentation](https://docs.recall.ai/)
- [WebSocket Protocol](https://tools.ietf.org/html/rfc6455)

## License

MIT License - See LICENSE file for details

---

**Created**: April 2026 | **Updated**: April 2026 | **Powered by 11Labs ConvAI**
