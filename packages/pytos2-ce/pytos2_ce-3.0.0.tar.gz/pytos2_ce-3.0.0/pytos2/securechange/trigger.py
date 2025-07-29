from functools import reduce, update_wrapper
from typing import Optional, Any
from os import environ
from sys import stdin
import sys  # Testability requires sys.exit() instead of just exit()

from traceback import format_exc
from xml.etree.ElementTree import fromstring, ParseError

from pytos2.utils import setup_logger
from pytos2.securechange import Scw
from .ticket import Ticket

LOGGER = setup_logger("trigger")

SCW_EVENT = "SCW_EVENT"
# XXX SCW_EVENT is test. so just use that instead of trying to read in stdin first. -_-


class Trigger:
    CURRENT_TRIGGER = None
    TRIGGERS: set = set()
    TICKET_INFO = None
    TICKET = None

    _bits = 0b1

    @staticmethod
    def from_scw_event(trigger):
        for t in Trigger.TRIGGERS:
            if t == trigger:
                return t

        return NONE

    @classmethod
    def _get_bits(cls):
        old_bits = cls._bits

        cls._bits *= 0b10

        return old_bits

    def __init__(self, representation, string, bits=None):
        if bits is None:
            bits = Trigger._get_bits()

        if type(representation) is str:
            representation = [representation]

        if type(string) is str:
            string = [string]

        self._bits = bits
        self._representation = representation
        self._string = string

    def __eq__(self, other):
        if type(other) is str:
            return repr(self) == other
        elif isinstance(other, Trigger):
            return self._bits == other._bits
        else:
            return False

    def __contains__(self, item):
        if not hasattr(item, "_bits"):
            return False

        return self._bits & item._bits == item._bits

    def __or__(self, other):
        if other in self:
            return self  # XXX do we want to return a copied version of that trigger?, or the actual trigger?

        if self in other:
            return other

        # FIXME: Is this check needed? other in self and self in other should take care of it?
        if self._bits == 0 or other._bits == 0:
            return NONE  # noqa

        # FIXME: I believe this check is covered by `other in self` and `self in other` implicitly
        if self._bits == other._bits:
            return self  # noqa

        # XXX make the reprs and strings a set, not a list, so we don't have to
        # do the above if checks
        return Trigger(
            self._representation + other._representation,
            self._string + other._string,
            self._bits | other._bits,
        )

    def __str__(self):
        if len(self._string) == 1:
            return self._string[0] + " Trigger"
        else:
            return " or ".join(self._string) + " Triggers"

    def __repr__(self):
        return "|".join(self._representation)

    def __hash__(self):
        return hash(repr(self))


TEST = Trigger("TEST", "Test")
CREATE = Trigger("CREATE", "Create")
CLOSE = Trigger("CLOSE", "Close")
CANCEL = Trigger("CANCEL", "Cancel")
REJECT = Trigger("REJECT", "Reject")
ADVANCE = Trigger("ADVANCE", "Advance")
REDO = Trigger("REDO", "Re-do")
RESUBMIT = Trigger("RESUBMIT", "Re-submit")
REOPEN = Trigger("REOPEN", "Re-open")
AUTOMATION_FAILED = Trigger("AUTOMATION_FAILED", "Automation Failed")
PRE_ASSIGNMENT_SCRIPT = Trigger("PRE_ASSIGNMENT_SCRIPT", "Pre-assignment script")
NONE = Trigger("NONE", "No", 0)
ALL = (
    CREATE
    | CLOSE
    | CANCEL
    | REJECT
    | ADVANCE
    | REDO
    | RESUBMIT
    | REOPEN
    | AUTOMATION_FAILED
    | PRE_ASSIGNMENT_SCRIPT
)

# the list of triggers received by SecureChange directly.
Trigger.TRIGGERS = {
    TEST,
    CREATE,
    CLOSE,
    CANCEL,
    REJECT,
    ADVANCE,
    REDO,
    RESUBMIT,
    REOPEN,
    AUTOMATION_FAILED,
}

STDIN = None


def _get_ticket_info_from_stdin():
    global STDIN
    # XXX get rid of the closure, and just use STDIN
    std_info = None

    def _save_ticket_info_from_stdin():
        nonlocal std_info
        global STDIN

        if std_info is not None:
            return std_info
        elif stdin.isatty():
            return None
        else:
            STDIN = stdin.read()
            # if we consumed stdin wrongly, then save it in STDIN for later consumers (like cron jobs)
            try:
                std_info = fromstring(STDIN)

                # then we're not a ticket_info XML
                if std_info.tag != "ticket_info":
                    return None

            except ParseError:
                # Then we're not XML
                return None

            return std_info

    return _save_ticket_info_from_stdin


get_ticket_info_from_stdin = _get_ticket_info_from_stdin()


def get_ticket_id_from_ticket_info(ticket_info):
    try:
        text_id = ticket_info.find("id").text
    except AttributeError:
        return None

    return int(text_id)


# FIXME: Do we need this function for pytos2?
def get_workflow_name(ticket):  # noqa
    return ticket["workflow"]["name"]


def workflow_is(workflow, ticket=None):
    def _workflow_is(ticket):
        if ticket is None:
            return False
        if ticket.workflow is None:
            return False

        return workflow == ticket.workflow.name

    return _workflow_is if ticket is None else _workflow_is(ticket)


# XXX alternatively, accept an integer step.
# step_is works on the current step. so "on advance, when the step we advanced to is X, then do this".
# use previous step to talk about the previous step.
def step_is(step, ticket=None):
    def _step_is(ticket):
        if ticket is None:
            return False

        # We use `.get` because completed tickets don't have current steps.
        # use get_current_step XXX
        # rename the "get step" and "get task" functions to match
        return step == ticket.current_step_name

    return _step_is if ticket is None else _step_is(ticket)


def rejected_on(step, ticket=None):
    def _rejected_on(ticket):
        if ticket is None:
            return False

        if len(ticket.comments) == 0:
            return False

        return step == ticket.comments[-1].task_name

    return _rejected_on if ticket is None else _rejected_on(ticket)


# XXX the name of this function might be deceiving? it only matches failures on
# the recent-most step


def failure_was(failure, ticket=None):
    def _failure_was(ticket):
        if ticket is None:
            return False

        return failure == ticket.get_last_automation_failure_on_current_step()

    return _failure_was if ticket is None else _failure_was(ticket)


def get_previous_stage(ticket):
    return ticket.get_step(-2).name


def get_current_stage(ticket_info):
    current_stage = ticket_info.find("current_stage")

    if current_stage is None:
        return None

    current_stage_name = current_stage.find("name")

    if current_stage_name is None:
        return None
    else:
        return current_stage_name.text


def triggers_are_racing(trigger, ticket_info, ticket):
    if trigger not in (CREATE, ADVANCE):
        # XXX I was told that tickets can only race on the CREATE and ADVANCE
        # triggers, so fast fail if that's not the case
        return False

    ticket_info_current_stage = get_current_stage(ticket_info)
    ticket_previous_stage = get_previous_stage(ticket)

    if ticket_info_current_stage != ticket_previous_stage:
        LOGGER.warning(
            f"Race detected. Ticket stage in trigger ({ticket_info_current_stage}) does not match previous stage in the retrieved ticket ({ticket_previous_stage})"
        )

    return ticket_info_current_stage != ticket_previous_stage


def prime_from_securechange_trigger():
    # if Trigger.TICKET:  # XXX turn Trigger.TICKET into the special ticket object
    #     return (Trigger.CURRENT_TRIGGER, Trigger.TICKET_INFO, Trigger.TICKET)

    ticket_info = get_ticket_info_from_stdin()
    # TODO CLEANUP
    #     if Trigger.ENTRYPOINT is None:
    #         LOGGER.error("No Scw instance initialized")
    #         return (None, None, None)
    if ticket_info is None:
        LOGGER.warning("Got empty ticket_info")
        return (None, None, None)

    trigger = Trigger.from_scw_event(environ["SCW_EVENT"])
    LOGGER.debug(f"Got {trigger} event")

    if trigger == TEST:
        LOGGER.debug("Got test trigger")
        return (trigger, ticket_info, None)

    ticket_id = get_ticket_id_from_ticket_info(ticket_info)
    LOGGER.debug("trigger found ticket_id: {}".format(ticket_id))

    if ticket_id is None:
        # XXX not sure why this would happen.
        return (None, None, None)

    ticket = Scw.default.get_ticket(ticket_id)

    if triggers_are_racing(trigger, ticket_info, ticket):
        LOGGER.debug("Detected race condition")
        sys.exit(0)

    return (trigger, ticket_info, ticket)


def _listify(xs):
    return xs if isinstance(xs, list) else [xs]


def when(*_predicates, **kwargs):
    if Trigger.CURRENT_TRIGGER is None:
        (
            Trigger.CURRENT_TRIGGER,
            Trigger.TICKET_INFO,
            Trigger.TICKET,
        ) = prime_from_securechange_trigger()
    # this seems unecessary
    # predicates = reduce(lambda ps, p: ps + _listify(p), _predicates, [])

    def _when(f):
        def _when2(*f_args, **f_kwargs):
            return f(*f_args, **f_kwargs)

        if Trigger.CURRENT_TRIGGER is None:
            pass
        elif not Trigger.TICKET:
            pass
        else:
            try:
                should_run = any(
                    ps(Ticket.kwargify(Trigger.TICKET.data)) for ps in _predicates
                )
            except Exception:
                LOGGER.error(format_exc())
                sys.exit(1)

            if should_run:
                try:
                    _when2(Trigger.TICKET, **kwargs)
                except Exception:
                    LOGGER.error(format_exc())
                    sys.exit(1)

        return update_wrapper(_when2, f)

    return _when


def on(*_trigger, when=lambda t: True, **kwargs):
    # duplicate with when because we need to prime
    # XXX refactor later
    (
        Trigger.CURRENT_TRIGGER,
        Trigger.TICKET_INFO,
        Trigger.TICKET,
    ) = prime_from_securechange_trigger()

    # on without a parameter runs always
    if len(_trigger) == 1 and callable(_trigger[0]):
        try:
            _trigger[0](Trigger.TICKET, **kwargs)
        except Exception:
            LOGGER.error(format_exc())
            sys.exit(1)

        return _trigger[0]

    trigger = None

    def _on(f):
        if (trigger is None) or (Trigger.CURRENT_TRIGGER in trigger):
            return globals()["when"](when, **kwargs)(f)
        else:
            return f

    for t in _trigger:
        if type(t) is list:
            if trigger is None:
                trigger = reduce(lambda ts, t: ts | t, t[1:], t[0])
            else:
                trigger = reduce(lambda ts, t: ts | t, t, trigger)
        else:
            if trigger is None:
                trigger = t
            else:
                trigger |= t

    return _on


def on_test(*args, when=lambda t: True, **kwargs):
    if args:
        return on(TEST, when=when, **kwargs)(args[0])
    else:
        return on(TEST, when=when, **kwargs)


def on_create(*args, when=lambda t: True, **kwargs):
    if args:
        return on(CREATE, when=when, **kwargs)(args[0])
    else:
        return on(CREATE, when=when, **kwargs)


def on_close(*args, when=lambda t: True, **kwargs):
    if args:
        return on(CLOSE, when=when, **kwargs)(args[0])
    else:
        return on(CLOSE, when=when, **kwargs)


def on_cancel(*args, when=lambda t: True, **kwargs):
    if args:
        return on(CANCEL, when=when, **kwargs)(args[0])
    else:
        return on(CANCEL, when=when, **kwargs)


def on_reject(*args, when=lambda t: True, **kwargs):
    if args:
        return on(REJECT, when=when, **kwargs)(args[0])
    else:
        return on(REJECT, when=when, **kwargs)


def on_advance(*args, when=lambda t: True, **kwargs):
    if args:
        return on(ADVANCE, when=when, **kwargs)(args[0])
    else:
        return on(ADVANCE, when=when, **kwargs)


def on_redo(*args, when=lambda t: True, **kwargs):
    if args:
        return on(REDO, when=when, **kwargs)(args[0])
    else:
        return on(REDO, when=when, **kwargs)


def on_resubmit(*args, when=lambda t: True, **kwargs):
    if args:
        return on(RESUBMIT, when=when, **kwargs)(args[0])
    else:
        return on(RESUBMIT, when=when, **kwargs)


def on_reopen(*args, when=lambda t: True, **kwargs):
    if args:
        return on(REOPEN, when=when, **kwargs)(args[0])
    else:
        return on(REOPEN, when=when, **kwargs)


def on_automation_failure(*args, when=lambda t: True, **kwargs):
    if args:
        return on(AUTOMATION_FAILED, when=when, **kwargs)(args[0])
    else:
        return on(AUTOMATION_FAILED, when=when, **kwargs)


def on_all(*args, when=lambda t: True, **kwargs):
    if args:
        return on(ALL, when=when, **kwargs)(args[0])
    else:
        return on(ALL, when=when, **kwargs)
