from dotenv import dotenv_values
from types import List
from pytos2.securechange import Scw as SecureChange
from pytos2.securechange.trigger import on_advance, step_is
from pytos2.securechange.ticket import Ticket, Comment

config = dotenv_values(".env")

HOST = "" or config["AURORA_HOST"]
USER = "" or config["USER"]
PASS = "" or config["PASS"]

# Instantiate Class
secure_change = SecureChange(HOST, USER, PASS)

STEP_NAME = "Trigger Test"


@on_advance(when=step_is(STEP_NAME))
def trigger_test(ticket: Ticket):
    ticket.add_comment(f"Tufin Ticket #{ticket.id}")
    ticket.advance()


def main():
    # Dummy function for console script to use
    pass
