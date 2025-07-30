"""
Generates a latin hypercube ``ModelValues`` container given
the ``ModelSpecification``. Uses :mod:``pyDOE``.
"""

from pyDOE import lhs

from swiftemulator.backend.model_specification import ModelSpecification
from swiftemulator.backend.model_parameters import ModelParameters
from swiftemulator.design.transform import transform_to_model_spec

from typing import Optional, Dict, Any, Optional
from contextlib import redirect_stdout
from os import devnull

import numpy as np


def create_hypercube(
    model_specification: ModelSpecification,
    number_of_samples: int,
    correlation_retries: Optional[int] = 32,
    prefix_unique_id: Optional[str] = None,
) -> ModelParameters:
    """
    Creates a Latin Hypercube model design.

    Parameters
    ----------

    model_specification: ModelSpecification
        Model specification for which to create a latin hypercube
        from.

    number_of_samples: int
        The number of samples to draw; this will be the number
        of input simulations that you wish to create.

    correlation_retries: int, optional
        Number of times to re-try creating a random hypercube, to
        minimize the correlation coefficient even further.
        Default: 32.

    prefix_unique_id: str, optional
        An optional prefix for the newly generated unique IDs.
        Defaults to no prefix.


    Returns
    -------

    model_parameters: ModelParameters
        A model values container with the prepared latin hypercube.
        Contains methods to visualise the output hypercube.


    Notes
    -----

    Uses :mod:``pyDOE``'s :func:`lhs` function, with the ``maximin``
    method.
    """

    samples = None
    corr = 1.0

    for _ in range(correlation_retries):
        # Reduce correlation as much as practical
        with redirect_stdout(open(devnull, "w")):
            new_samples = lhs(
                n=model_specification.number_of_parameters,
                samples=number_of_samples,
                criterion="maximin",
            )

        R = np.corrcoef(new_samples)
        min_corr = np.max(np.abs(R - np.eye(R.shape[0])))

        if min_corr <= corr:
            samples = new_samples
            corr = min_corr

    return transform_to_model_spec(
        input_array=samples,
        model_specification=model_specification,
        prefix_unique_id=prefix_unique_id,
    )
