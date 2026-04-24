#!/usr/bin/env python3
import asyncio
import json
import logging
import os
import base64
from dotenv import load_dotenv
import websockets
from websockets.legacy.server import WebSocketServerProtocol, serve
from websockets.legacy.client import connect

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
PORT = int(os.getenv("PORT", 3000))
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID", "agent_4101kne33jyvef3rjxyfhd1kyyp0")

if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY must be set in .env file")


async def connect_to_elevenlabs():
    """Connect to 11Labs ConvAI WebSocket endpoint."""
    uri = f"wss://api.elevenlabs.io/convai?agent_id={ELEVENLABS_AGENT_ID}"

    try:
        ws = await connect(
            uri,
            extra_headers={
                "Authorization": f"Bearer {ELEVENLABS_API_KEY}",
                "Content-Type": "application/json",
            },
            subprotocols=["convai"],
        )
        logger.info(f"Successfully connected to 11Labs ConvAI with agent: {ELEVENLABS_AGENT_ID}")

        # 11Labs typically sends a welcome message
        try:
            response = await ws.recv()
            event = json.loads(response) if isinstance(response, str) else response
            logger.info(f"Received initial message from 11Labs: {event}")
            
            return ws, event
        except Exception as e:
            logger.warning(f"No initial response from 11Labs or error parsing: {e}")
            return ws, {"type": "session.created", "status": "ready"}

    except Exception as e:
        logger.error(f"Failed to connect to 11Labs ConvAI: {str(e)}")
        raise


class WebSocketRelay:
    def __init__(self):
        """Initialize the WebSocket relay server."""
        self.connections = {}
        self.message_queues = {}

    async def handle_browser_connection(
        self, websocket: WebSocketServerProtocol, path: str
    ):
        """Handle a connection from the browser."""
        base_path = path.split("?")[0]
        if base_path != "/":
            logger.error(f"Invalid path: {path}")
            await websocket.close(1008, "Invalid path")
            return

        logger.info(f"Browser connected from {websocket.remote_address}")
        self.message_queues[websocket] = []
        elevenlabs_ws = None

        try:
            # Connect to 11Labs ConvAI
            elevenlabs_ws, session_created = await connect_to_elevenlabs()
            self.connections[websocket] = elevenlabs_ws

            logger.info("Connected to 11Labs ConvAI successfully!")

            # Send session created to browser
            await websocket.send(json.dumps(session_created))
            logger.info("Forwarded session.created to browser")

            # Process any queued messages
            while self.message_queues[websocket]:
                message = self.message_queues[websocket].pop(0)
                try:
                    event = json.loads(message)
                    logger.info(f'Relaying "{event.get("type")}" to 11Labs')
                    await elevenlabs_ws.send(message)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from browser: {message}")

            async def handle_browser_messages():
                try:
                    while True:
                        message = await websocket.recv()
                        try:
                            if isinstance(message, str):
                                event = json.loads(message)
                                logger.info(f'Relaying "{event.get("type")}" to 11Labs')
                                await elevenlabs_ws.send(message)
                            else:
                                # Binary data - audio
                                logger.debug(f"Relaying binary audio to 11Labs ({len(message)} bytes)")
                                await elevenlabs_ws.send(message)
                        except json.JSONDecodeError:
                            logger.error(f"Invalid JSON from browser: {message}")
                except websockets.exceptions.ConnectionClosed as e:
                    logger.info(
                        f"Browser connection closed: code={e.code}, reason={e.reason}"
                    )
                    raise

            async def handle_elevenlabs_messages():
                try:
                    while True:
                        message = await elevenlabs_ws.recv()
                        try:
                            if isinstance(message, str):
                                event = json.loads(message)
                                logger.info(
                                    f'Relaying "{event.get("type")}" from 11Labs'
                                )
                                await websocket.send(json.dumps(event))
                            else:
                                # Binary audio data from 11Labs
                                logger.debug(f"Relaying binary audio from 11Labs ({len(message)} bytes)")
                                # Send as JSON with base64 encoded audio
                                audio_message = {
                                    "type": "response.audio.delta",
                                    "delta": base64.b64encode(message).decode('utf-8')
                                }
                                await websocket.send(json.dumps(audio_message))
                        except json.JSONDecodeError:
                            logger.error(f"Invalid JSON from 11Labs: {message}")
                except websockets.exceptions.ConnectionClosed as e:
                    logger.info(
                        f"11Labs connection closed: code={e.code}, reason={e.reason}"
                    )
                    raise

            try:
                await asyncio.gather(
                    handle_browser_messages(), handle_elevenlabs_messages()
                )
            except websockets.exceptions.ConnectionClosed:
                logger.info("One of the connections closed, cleaning up")

        except Exception as e:
            logger.error(f"Error handling connection: {str(e)}")
            if not websocket.closed:
                await websocket.close(1011, str(e))
        finally:
            if websocket in self.connections:
                if elevenlabs_ws and not elevenlabs_ws.closed:
                    await elevenlabs_ws.close(1000, "Normal closure")
                del self.connections[websocket]
            if websocket in self.message_queues:
                del self.message_queues[websocket]
            if not websocket.closed:
                await websocket.close(1000, "Normal closure")

    async def serve(self):
        """Start the WebSocket relay server."""
        async with serve(
            self.handle_browser_connection,
            "0.0.0.0",
            PORT,
            ping_interval=20,
            ping_timeout=20,
            subprotocols=["realtime", "convai"],
        ):
            logger.info(f"WebSocket relay server started on ws://0.0.0.0:{PORT}")
            logger.info(f"Using 11Labs agent: {ELEVENLABS_AGENT_ID}")
            await asyncio.Future()


def main():
    """Main entry point for the WebSocket relay server."""
    relay = WebSocketRelay()
    try:
        asyncio.run(relay.serve())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    finally:
        logger.info("Server shutdown complete")


if __name__ == "__main__":
    main()
