import time
import logging


def register(subparsers):
    parser = subparsers.add_parser("service", help="Service")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    parser_create = subparsers.add_parser("create", help="Create a new service")
    parser_create.add_argument("name", metavar="NAME", help="Name of the new project")
    parser.set_defaults(func=main)


def main(args):
    if args.command == "create":
        print(
            f"""\
[Unit]
Description={args.name}
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/jbussdieker/Desktop
ExecStart=/home/jbussdieker/.local/bin/{args.name}
Restart=on-failure
RestartSec=5s
Environment=PYTHONUNBUFFERED=1

User=jbussdieker
Group=jbussdieker
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        )
    else:
        logging.info("Starting service")
        while True:
            logging.debug("running...")
            time.sleep(1)
