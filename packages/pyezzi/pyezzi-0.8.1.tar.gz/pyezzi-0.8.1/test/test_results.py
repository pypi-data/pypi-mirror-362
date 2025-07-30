import numpy as np

from pyezzi.thickness import ThicknessSolver, compute_thickness_cardiac


def test_L0(example_reference: dict, example_solver: ThicknessSolver):
    assert np.allclose(example_reference["L0"], example_solver.L0)


def test_L1(example_reference: dict, example_solver: ThicknessSolver):
    assert np.allclose(example_reference["L1"], example_solver.L1)


def test_thickness(example_reference: dict, example_solver: ThicknessSolver):
    assert np.allclose(example_reference["thickness"], example_solver.result)


def test_laplace(example_reference: dict, example_solver: ThicknessSolver):
    assert np.allclose(example_reference["laplace"], example_solver.laplace_grid)


def test_real_data(realistic_endo, realistic_epi, realistic_thickness):
    thickness = compute_thickness_cardiac(
        realistic_endo,
        realistic_epi,
        (2, 1.5, 0.5),
        None,
        0,
        5000,
        0,
        5000,
    )
    assert np.allclose(thickness, realistic_thickness, equal_nan=True)


def test_weights(example_wall, example_epi, example_weights, thickness_weights):
    thickness = compute_thickness_cardiac(
        example_wall ^ example_epi,
        example_epi,
        (3, 3, 3),
        example_weights,
        0,
        5000,
        0,
        5000,
    )

    assert np.allclose(thickness_weights, thickness)
