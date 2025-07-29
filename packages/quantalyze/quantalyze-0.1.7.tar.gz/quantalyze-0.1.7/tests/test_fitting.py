import pytest
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from quantalyze.core.fitting import fit, Fit


def test_fit_linear_function():
    # Define a linear function
    def linear_func(x, a, b):
        return a * x + b

    # Create a DataFrame with linear data
    df = pd.DataFrame({
        'x': np.linspace(0, 10, 100),
        'y': 3 * np.linspace(0, 10, 100) + 2
    })

    # Fit the linear function to the data
    fit_result = fit(linear_func, df, 'x', 'y')

    # Assert that the optimal parameters are close to the expected values
    np.testing.assert_allclose(fit_result.parameters, [3, 2], rtol=1e-2)


def test_fit_with_x_range():
    # Define a quadratic function
    def quadratic_func(x, a, b, c):
        return a * x**2 + b * x + c

    # Create a DataFrame with quadratic data
    df = pd.DataFrame({
        'x': np.linspace(0, 10, 100),
        'y': 2 * np.linspace(0, 10, 100)**2 + 3 * np.linspace(0, 10, 100) + 1
    })

    # Fit the quadratic function to the data within a specific x range
    fit_result = fit(quadratic_func, df, 'x', 'y', x_min=2, x_max=8)

    # Assert that the optimal parameters are close to the expected values
    np.testing.assert_allclose(fit_result.parameters, [2, 3, 1], rtol=1e-2)


def test_fit_with_no_data_in_range():
    # Define a linear function
    def linear_func(x, a, b):
        return a * x + b

    # Create a DataFrame with linear data
    df = pd.DataFrame({
        'x': np.linspace(0, 10, 100),
        'y': 3 * np.linspace(0, 10, 100) + 2
    })

    # Fit the linear function to the data with an x range that has no data
    with pytest.raises(RuntimeError):
        fit(linear_func, df, 'x', 'y', x_min=20, x_max=30)


def test_get_item():
    # Create a DataFrame
    df = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [4, 5, 6]
    })

    def model(x, lorem, ipsum):
        return lorem * x + ipsum
    
    result = fit(model, df, 'x', 'y', p0=[1, 1])

    assert result['lorem'] == result.parameters[0]
    assert result['ipsum'] == result.parameters[1]

    assert result['lorem'] == result[0]
    assert result['ipsum'] == result[1]
    
    with pytest.raises(KeyError):
        result['dolor']

    with pytest.raises(IndexError):
        result[2]


def test_lambda_get_item():
    # Create a DataFrame
    df = pd.DataFrame({
        'x': [1, 2, 3],
        'y': [4, 5, 6]
    })

    model = lambda x, a, b: a * x + b
    
    result = fit(model, df, 'x', 'y', p0=[1, 1])
    
    assert result.parameters[0] == result['a']
    assert result.parameters[1] == result['b']
    
    with pytest.raises(KeyError):
        result['c']

    