import click
from config import opts
from typing import List, Tuple

@click.command()
@click.option('--name', '-n', default='DeepFuse', help='Name of the algorithm.')
@click.option('--param', '-p', default=[], multiple=True, type=(str, str, str), help='Any parameter in the format --param key type value.')
def main(name: str, param: List[Tuple[str, str, str]]) -> None:
    """
    Main entry point for training an algorithm.

    This function checks if the specified algorithm exists in the provided field,
    updates its configuration options with any given parameters, and then 
    triggers the training process.

    Parameters:
    - name: str
        The name of the algorithm to be trained. Default is 'DeepFuse'.
    - param: List[Tuple[str, str, str]]
        A list of tuples where each tuple consists of a key, type, and value.
        These parameters will be used to update the algorithm's options before training.
    """
    algorithm = __import__(f'clib.model.collection.{name}', fromlist=['*'])

    opts[name] = {k: eval(t)(v) for k, v, t in param}

    algorithm.train(opts[name])

if __name__ == '__main__':
    main()
