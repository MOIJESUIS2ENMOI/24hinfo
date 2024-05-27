import argparse
import logging
from lib.client import Client
from lib.parser import Parser
from lib.model import Model

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="WebSocket Client")
    parser.add_argument('--host', type=str, required=True, help='WebSocket server host')
    parser.add_argument('--port', type=int, required=True, help='WebSocket server port')
    parser.add_argument('--reconnect-delay', type=int, default=5, help='Delay before attempting to reconnect in seconds')
    parser.add_argument('--enable-trace', action='store_true', help='Enable WebSocket trace')
    return parser.parse_args()

def main():
    """
    Main function to run the WebSocket client.
    """
    args = parse_args()

    try:
        model = Model()
        parser = Parser()
        client = Client(host=args.host, port=args.port, parser=parser, model=model, reconnect_delay=args.reconnect_delay, enable_trace=args.enable_trace)
        client.run()
    except Exception as e:
        logging.critical(f"Critical error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
