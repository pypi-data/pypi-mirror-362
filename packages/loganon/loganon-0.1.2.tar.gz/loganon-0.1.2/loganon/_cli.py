from pathlib import Path
import click
import logging as py_logging

from loganon import rulesets, Anonymizer
from loganon._config import config
import loganon._logging as logging

logger = logging.getLogger(__name__)

@click.group()
@click.option("--debug", "-d", is_flag=True, default=False, help="Enable debug logging")
def cli(debug: bool):
    if debug:
        logging.console_handler.setLevel(py_logging.DEBUG)
    pass

@cli.command("run")
@click.argument("rules", nargs=-1)
@click.option("--input", "-i", type=click.File("r"), help="Input file")
@click.option("--output", "-o", type=click.File("w"), help="Output file")
def anonymize(rules: list[str], input, output):
    data = input.read()

    active_rulesets = []
    for rule in rules:
        try:
            active_rulesets.extend(rulesets[rule])
        except KeyError:
            logger.critical(f"Unknown ruleset: {rule}")
            return
        
    anonymizer = Anonymizer(active_rulesets)

    anonymized_data = anonymizer.anonymize(data)

    output.write(anonymized_data)

@cli.command("config", no_args_is_help=True)
@click.option("--ruleset", "-r", type=(str, click.Path(exists=True, path_type=Path)), multiple=True, help="Add a custom ruleset")
@click.option("--remove-ruleset", "-R", type=str, multiple=True, help="Remove a custom ruleset")
@click.option("--log-file", "-l", type=click.Path(exists=False, path_type=Path), help="Set the log file")
def set_config(ruleset: list[tuple[str, Path]], remove_ruleset: list[str], log_file: Path):
    if rulesets or remove_ruleset:
        current_rulesets = config.custom_rulesets
        for name, path in ruleset:
            current_rulesets[name] = path
            logger.debug(f"Added custom ruleset: {name} -> {path}")
        
        # Remove the rulesets
        for name in remove_ruleset:
            current_rulesets.pop(name, None)
            logger.debug(f"Removed custom ruleset: {name}")

        config.custom_rulesets = current_rulesets
    
    if log_file:
        config.log_file = log_file
        logger.debug(f"Set log file: {log_file}")
    
    logger.info("Config updated.")

if __name__ == "__main__":
    cli()