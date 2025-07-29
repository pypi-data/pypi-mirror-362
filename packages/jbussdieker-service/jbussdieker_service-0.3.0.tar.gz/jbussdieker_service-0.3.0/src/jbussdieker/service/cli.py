import time
import logging


def register(subparsers):
    parser = subparsers.add_parser("service", help="Service")
    parser.set_defaults(func=main)


def main(args):
    logging.info("Starting service")
    while True:
        logging.debug("running...")
        time.sleep(1)
