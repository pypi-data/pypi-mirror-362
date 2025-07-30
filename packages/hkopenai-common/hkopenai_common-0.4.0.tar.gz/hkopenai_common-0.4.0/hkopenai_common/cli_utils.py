import argparse
import os
import sys


def cli_main(server_main_func, description, args_list=None):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)",
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to bind the server to"
    )

    # Parse command-line arguments
    if args_list is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args_list)

    # Initialize final values with command-line arguments (or their defaults)
    sse_final = args.sse
    host_final = args.host
    port_final = args.port

    # Apply environment variables if command-line arguments were not provided (i.e., still default)
    if not sse_final and os.environ.get("TRANSPORT_MODE") == "sse":
        sse_final = True

    if host_final == parser.get_default("host"):
        env_host = os.environ.get("HOST")
        if env_host is not None:
            host_final = env_host

    if port_final == parser.get_default("port"):
        env_port = os.environ.get("PORT")
        if env_port is not None:
            try:
                port_final = int(env_port)
            except ValueError:
                pass  # Keep the default or command-line value if env var is invalid

    server = server_main_func()
    if sse_final:
        server.run(transport="streamable-http", host=host_final, port=port_final)
    else:
        server.run()
