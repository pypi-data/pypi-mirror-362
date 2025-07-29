import time
import logging


def register(subparsers):
    parser = subparsers.add_parser("service", help="Service")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    subparsers.add_parser("install", help="Install the systemd service")
    parser.set_defaults(func=main)


def main(args):
    if args.command == "install":
        with open("/etc/systemd/system/jbussdieker.service", "w") as f:
            f.write(
                f"""\
[Unit]
Description=jbussdieker service
After=network.target

[Service]
Type=simple
WorkingDirectory=/tmp
ExecStart=/home/jbussdieker/.local/bin/jbussdieker service
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
