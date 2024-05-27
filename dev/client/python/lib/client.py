import websocket
import logging
import time
from lib.parser import Parser
from lib.model import Model

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Client:
    def __init__(self, host: str, port: int, parser: Parser, model: Model, reconnect_delay: int = 5, enable_trace: bool = False):
        """
        Initialize the WebSocket client.
        
        :param host: WebSocket server host
        :param port: WebSocket server port
        :param parser: Parser instance for message handling
        :param model: Model instance for processing messages
        :param reconnect_delay: Delay before attempting to reconnect in seconds
        :param enable_trace: Enable WebSocket tracing if True
        """
        self.host = host
        self.port = port
        self.parser = parser
        self.model = model
        self.reconnect_delay = reconnect_delay
        self.enable_trace = enable_trace
        self.ws = None
        self.should_reconnect = True

    def on_message(self, ws, message):
        try:
            logging.info(f"Received: {message}")
            parsed_message = self.parser.message_to_json(message)
            response = self.model.process_message(parsed_message)
            composed_message = self.parser.message_to_json(response)
            ws.send(composed_message)
            logging.info(f"Processed response: {response}")
        except Exception as e:
            logging.error(f"Error processing message: {e}", exc_info=True)

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}", exc_info=True)

    def on_close(self, ws, close_status_code, close_msg):
        logging.info(f"Connection closed with code: {close_status_code}, message: {close_msg}")
        if self.should_reconnect:
            time.sleep(self.reconnect_delay)
            self.connect()

    def on_open(self, ws):
        try:
            message = "Hello, server!"
            logging.info(f"Sending: {message}")
            ws.send(message)
        except Exception as e:
            logging.error(f"Error during on_open: {e}", exc_info=True)

    def connect(self):
        """
        Create a new WebSocket connection and assign callbacks.
        """
        try:
            websocket.enableTrace(self.enable_trace)
            ws_url = f"ws://{self.host}:{self.port}"
            self.ws = websocket.WebSocketApp(ws_url,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws.run_forever()
        except Exception as e:
            logging.critical(f"Critical error in WebSocket connection: {e}", exc_info=True)
            time.sleep(self.reconnect_delay)
            self.connect()

    def run(self):
        self.should_reconnect = True
        self.connect()

    def stop(self):
        """
        Stop the WebSocket client and prevent reconnection attempts.
        """
        self.should_reconnect = False
        if self.ws:
            self.ws.close()