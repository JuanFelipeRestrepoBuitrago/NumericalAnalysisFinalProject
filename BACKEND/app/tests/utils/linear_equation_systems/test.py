from app.utils.linear_equation_systems import regressive_substitution
from app.utils.utils import construct_augmented_matrix
from app.routes.routes import logger
from fastapi.exceptions import HTTPException
import numpy as np

def test_regressive_substitution():
    # Test for a system of equations with 3 variables
    A = np.array([[1, -2, 3], [0, 1, -2], [0, 0, 9]])
    b = np.array([7, -3, 9])
    x = np.array([2, -1, 1])
    result = regressive_substitution(construct_augmented_matrix(A, b), 3, logger=logger)
    assert np.allclose(result, x), "Test failed for a system of equations with 3 variables"

    # Test for a system of equations with 4 variables
        # Test for a system of equations with 4 variables
    A = np.array([
        [2, -1, 0, 3],
        [0, 3, -1, 2],
        [0, 0, 4, -2],
        [0, 0, 0, 5]
    ])
    b = np.array([8, 9, 12, 10])
    x = np.array([2.5, 3, 4, 2])
    result = regressive_substitution(construct_augmented_matrix(A, b), 4, logger=logger)
    assert np.allclose(result, x), "Test failed for a system of equations with 4 variables"

    # Test for a system of equations with 5 variables
    A = np.array([
        [1, -2, 3, 0, 1],
        [0, 4, -1, 2, -3],
        [0, 0, 5, -2, 1],
        [0, 0, 0, 6, -1],
        [0, 0, 0, 0, 7]
    ])
    b = np.array([5, 12, 17, 18, 21])
    x = np.array([-3/2, 91/20, 21/5, 7/2, 3])

    assert np.allclose(regressive_substitution(construct_augmented_matrix(A, b), 5, logger=logger), x), "Test failed for a system of equations with 5 variables"
