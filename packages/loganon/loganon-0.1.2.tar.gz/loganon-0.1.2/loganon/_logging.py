import logging

from loganon._config import config

import click

class ClickEchoHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        # Print critical, unrecoverable errors in red
        if record.levelno >= logging.CRITICAL:
            click.echo(click.style("ERROR: ", fg="red") + record.getMessage(), err=True)
        # Print warnings for the user to advise better usage
        elif record.levelno == logging.WARNING:
            click.echo(click.style("WARNING: ", fg="yellow") + record.getMessage(), err=True)
        elif record.levelno <= logging.INFO:
            # Print all other messages in white
            # This should be just informational messages but if the "--debug" flag is passed, will
            #   include those messages as well
            click.echo(record.getMessage())


"""Setup logging for the app."""
console_handler = ClickEchoHandler()
console_handler.setFormatter(logging.Formatter("%(message)s"))
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(config.log_file)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] (%(name)s) %(funcName)s(): %(message)s"))
file_handler.setLevel(logging.INFO)

debug_file_handler = logging.FileHandler(config.log_file.parent / (config.log_file.stem + "_debug.log"))
debug_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] (%(name)s) %(funcName)s(): %(message)s"))
debug_file_handler.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler, debug_file_handler])

"""Export the logger function"""
getLogger = logging.getLogger