import argparse
import os

from dotenv import load_dotenv

load_dotenv()


def to_run_mcp_in_server_mode_or_std_io() -> bool:
    print(f"is_the_mcp_to_run_in_server_mode_or_std_dio: {get_script_args().run_in_server_mode}")
    return get_script_args().run_in_server_mode


def get_script_args():
    parser = argparse.ArgumentParser(
        description="MCP server for WhatsApp functionality via Titanmind."
    )

    parser.add_argument(
        "--run-in-server-mode",
        action="store_true",
        # even of the presence of --run-in-server-mode will make set the bool as true. no need to provide True/False to this flag
        help="bool to run in server mode or stdio mode"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="The port number to run the server on (default: 3000)."
    )

    return parser.parse_args()
