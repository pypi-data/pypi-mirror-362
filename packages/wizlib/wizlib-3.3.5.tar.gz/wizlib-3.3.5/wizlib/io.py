# Primitive i/o functions referenced elsewhere, useful for test patching (a
# sort of dependency injection

import sys

import readchar

from wizlib.parser import WizArgumentError
from wizlib.ui.shell import ESC


ISATTY = all(s.isatty() for s in (sys.stdin, sys.stdout, sys.stderr))


def isatty():
    return ISATTY


def stream():
    return '' if ISATTY else sys.stdin.read()


def ttyin():  # pragma: nocover
    if ISATTY:
        key = readchar.readkey()
        # Handle specialized escape sequences
        if key == ESC + '[1;':
            key = key + readchar.readkey() + readchar.readkey()
        return key
    else:
        raise WizArgumentError(
            'Command designed for interactive use')
