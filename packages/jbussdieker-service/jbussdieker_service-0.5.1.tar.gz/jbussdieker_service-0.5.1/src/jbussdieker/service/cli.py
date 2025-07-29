import time
import logging


def register(subparsers):
    parser = subparsers.add_parser("service", help="Service")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    subparsers.add_parser("install", help="Install the systemd service")
    parser.set_defaults(func=main)


def get_systemd_unit_path():
    """Get the systemd unit file path. Made configurable for testing."""
    return "/etc/systemd/system/jbussdieker.service"


def get_systemd_unit_content():
    """Get the systemd unit file content. Made configurable for testing."""
    return f"""\
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


def install_systemd_service():
    """Install the systemd service. Made configurable for testing."""
    unit_path = get_systemd_unit_path()
    unit_content = get_systemd_unit_content()

    with open(unit_path, "w") as f:
        f.write(unit_content)


def run_service():
    """Run the service loop. Made configurable for testing."""
    logging.info("Starting service")
    while True:
        logging.debug("running...")
        time.sleep(1)


def main(args, config):
    if args.command == "install":
        install_systemd_service()
    else:
        run_service()
