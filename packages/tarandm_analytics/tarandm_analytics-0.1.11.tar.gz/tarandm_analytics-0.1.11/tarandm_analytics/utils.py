from typing import Union


def get_number_formatting(number: Union[float, int]) -> str:
    import numpy as np

    if number == -np.inf:
        return "-inf"
    elif isinstance(number, int):
        return str(number)
    elif number * 100 > 1:
        return "{:.3f}".format(number)
    else:
        return "{:.2E}".format(number)
