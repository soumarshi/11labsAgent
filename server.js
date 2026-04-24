const WebSocket = require('ws');
const dotenv = require('dotenv');
const http = require('http');

dotenv.config();

const PORT = parseInt(process.env.PORT || '3000');
const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;
const ELEVENLABS_AGENT_ID = process.env.ELEVENLABS_AGENT_ID || 'agent_4101kne33jyvef3rjxyfhd1kyyp0';

if (!ELEVENLABS_API_KEY) {
  throw new Error('ELEVENLABS_API_KEY must be set in .env file');
}

// Create HTTP server for WebSocket
const server = http.createServer();
const wss = new WebSocket.Server({ server });

// Log function
function log(message) {
  console.log(`[${new Date().toISOString()}] ${message}`);
}

async function connectTo11Labs() {
  return new Promise((resolve, reject) => {
    const uri = `wss://api.elevenlabs.io/convai?agent_id=${ELEVENLABS_AGENT_ID}`;
    
    log(`Connecting to 11Labs ConvAI: ${uri}`);
    
    const ws = new WebSocket(uri, ['convai'], {
      headers: {
        'Authorization': `Bearer ${ELEVENLABS_API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    ws.on('open', () => {
      log(`✓ Connected to 11Labs ConvAI with agent: ${ELEVENLABS_AGENT_ID}`);
      
      // Wait for initial message
      const messageHandler = (data) => {
        try {
          const event = JSON.parse(data);
          log(`✓ Received initial message from 11Labs: ${event.type}`);
          ws.removeListener('message', messageHandler);
          resolve({ ws, event });
        } catch (e) {
          log(`Warning: Could not parse initial message: ${e.message}`);
          ws.removeListener('message', messageHandler);
          resolve({ ws, event: { type: 'session.created', status: 'ready' } });
        }
      };
      
      ws.on('message', messageHandler);
      
      // Timeout after 5 seconds if no message
      setTimeout(() => {
        ws.removeListener('message', messageHandler);
        resolve({ ws, event: { type: 'session.created', status: 'ready' } });
      }, 5000);
    });

    ws.on('error', (error) => {
      log(`✗ Failed to connect to 11Labs ConvAI: ${error.message}`);
      reject(error);
    });

    ws.on('close', () => {
      log('11Labs WebSocket closed');
    });
  });
}

wss.on('connection', async (browserWs, req) => {
  const clientAddress = req.socket.remoteAddress;
  log(`Browser connected from ${clientAddress}`);

  let elevenLabsWs = null;
  const messageQueue = [];

  try {
    // Connect to 11Labs
    const { ws: labsWs, event: sessionCreated } = await connectTo11Labs();
    elevenLabsWs = labsWs;

    log('✓ Connected to 11Labs successfully!');

    // Send session created to browser
    browserWs.send(JSON.stringify(sessionCreated));
    log('✓ Forwarded session.created to browser');

    // Set up bidirectional relaying
    // Handle messages from browser to 11Labs
    const handleBrowserMessage = (data) => {
      try {
        if (typeof data === 'string') {
          const event = JSON.parse(data);
          log(`Relaying "${event.type}" to 11Labs`);
          elevenLabsWs.send(data);
        } else {
          // Binary audio data
          log(`Relaying binary audio to 11Labs (${data.length} bytes)`);
          elevenLabsWs.send(data);
        }
      } catch (error) {
        log(`Error processing browser message: ${error.message}`);
      }
    };

    // Handle messages from 11Labs to browser
    const handleElevenLabsMessage = (data) => {
      try {
        if (typeof data === 'string') {
          const event = JSON.parse(data);
          log(`Relaying "${event.type}" from 11Labs`);
          browserWs.send(JSON.stringify(event));
        } else {
          // Binary audio data from 11Labs
          log(`Relaying binary audio from 11Labs (${data.length} bytes)`);
          const audioMessage = {
            type: 'response.audio.delta',
            delta: data.toString('base64')
          };
          browserWs.send(JSON.stringify(audioMessage));
        }
      } catch (error) {
        log(`Error processing 11Labs message: ${error.message}`);
      }
    };

    browserWs.on('message', handleBrowserMessage);
    elevenLabsWs.on('message', handleElevenLabsMessage);

    // Handle browser disconnect
    browserWs.on('close', () => {
      log(`Browser connection closed from ${clientAddress}`);
      if (elevenLabsWs && elevenLabsWs.readyState === WebSocket.OPEN) {
        elevenLabsWs.close(1000, 'Browser disconnected');
      }
    });

    // Handle browser errors
    browserWs.on('error', (error) => {
      log(`Browser connection error: ${error.message}`);
      if (elevenLabsWs && elevenLabsWs.readyState === WebSocket.OPEN) {
        elevenLabsWs.close(1011, error.message);
      }
    });

    // Handle 11Labs disconnect
    elevenLabsWs.on('close', () => {
      log('11Labs connection closed');
      if (browserWs.readyState === WebSocket.OPEN) {
        browserWs.close(1000, '11Labs disconnected');
      }
    });

    // Handle 11Labs errors
    elevenLabsWs.on('error', (error) => {
      log(`11Labs connection error: ${error.message}`);
      if (browserWs.readyState === WebSocket.OPEN) {
        browserWs.close(1011, error.message);
      }
    });

  } catch (error) {
    log(`Error handling connection: ${error.message}`);
    if (browserWs.readyState === WebSocket.OPEN) {
      browserWs.close(1011, error.message);
    }
    if (elevenLabsWs && elevenLabsWs.readyState === WebSocket.OPEN) {
      elevenLabsWs.close(1000);
    }
  }
});

// Start server
server.listen(PORT, '0.0.0.0', () => {
  log(`✓ WebSocket relay server started on ws://0.0.0.0:${PORT}`);
  log(`✓ Using 11Labs agent: ${ELEVENLABS_AGENT_ID}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  log('Server shutdown requested');
  server.close(() => {
    log('Server shutdown complete');
    process.exit(0);
  });
});
