import click
import cslib
import config
from typing import List, Tuple

@click.command()
@click.option('--name', '-n', default='LeNet', help='Name of the algorithm.')
@click.option('--field', '-f', default='classical', help='Field of the algorithm.')
@click.option('--param', '-p', default=[], multiple=True, type=(str, str, str), help='Any parameter in the format --param key type value.')
def main(name: str, field: str, param: List[Tuple[str, str, str]]) -> None:
    """
    Main entry point for training an algorithm.

    This function checks if the specified algorithm exists in the provided field,
    updates its configuration options with any given parameters, and then 
    triggers the training process.

    Parameters:
    - name: str
        The name of the algorithm to be trained. Default is 'LeNet'.
    - field: str
        The field in which the algorithm is categorized. Default is 'classical'.
    - param: List[Tuple[str, str, str]]
        A list of tuples where each tuple consists of a key, type, and value.
        These parameters will be used to update the algorithm's options before training.

    Returns:
    - None
    """
    # Validate the field exists in clib.model
    assert hasattr(clib.projects, field), f"Field '{field}' not found in clib.model"
    all_algorithms = getattr(clib.projects, field)
    
    # Validate the algorithm name exists in the field
    assert hasattr(all_algorithms, name), f"Algorithm '{name}' not found in field '{field}'"
    
    # Validate the algorithm name exists in config.opts
    # assert name in config.opts, f"Algorithm '{name}' not found in config.opts"
    algorithm = getattr(all_algorithms, name)

    # Update options with the provided parameters
    config.opts[name] = {k: bool(int(v)) if t=='bool' else eval(t)(v) for k, v, t in param}
    opts = config.opts[name] 

    # Trigger the training process
    algorithm.inference(opts)

if __name__ == '__main__':
    main()
