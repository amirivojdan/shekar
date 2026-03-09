import argparse
import sys


def main():
    parser = argparse.ArgumentParser(prog="shekar")
    subparsers = parser.add_subparsers(dest="command")

    serve_parser = subparsers.add_parser("serve", help="Start the Shekar web UI server")
    serve_parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        metavar="PORT",
        help="Port to listen on (default: 8080)",
    )

    args = parser.parse_args()

    if args.command == "serve":
        from shekar.server import serve

        serve(port=args.port)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
