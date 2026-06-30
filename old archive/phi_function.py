"""
Phi Function: Complete Implementation
======================================

This module provides efficient, robust numerical computation of the function Φ(c),
defined as the inverse of H(x) = x + (log x)^2 for x > 1.

Author: Mathematical Research
Date: February 2026
"""

import numpy as np
from scipy.optimize import newton, brentq
from typing import Union, Tuple, Optional
import warnings


class PhiFunction:
    """
    Complete implementation of Φ(c), the inverse of H(x) = x + (log x)^2.
    
    This class provides multiple numerical methods with automatic method selection,
    error estimation, and rigorous bounds.
    """
    
    def __init__(self, tolerance: float = 1e-12, max_iterations: int = 100):
        """
        Initialize the Φ function computer.
        
        Parameters
        ----------
        tolerance : float
            Convergence tolerance for iterative methods
        max_iterations : int
            Maximum iterations for Newton's method
        """
        self.tol = tolerance
        self.max_iter = max_iterations
        
    def __call__(self, c: Union[float, np.ndarray], 
                 method: str = 'auto') -> Union[float, np.ndarray]:
        """
        Compute Φ(c) for given c value(s).
        
        Parameters
        ----------
        c : float or array_like
            Input value(s), must be > 1
        method : str
            Method to use: 'auto', 'newton', 'halley', 'brent', or 'series'
            
        Returns
        -------
        float or ndarray
            Φ(c) value(s)
        """
        scalar_input = np.isscalar(c)
        c = np.atleast_1d(c)
        
        # Validate input
        if np.any(c <= 1):
            raise ValueError("All c values must be > 1")
        
        # Select method
        if method == 'auto':
            result = self._compute_auto(c)
        elif method == 'newton':
            result = self._compute_newton(c)
        elif method == 'halley':
            result = self._compute_halley(c)
        elif method == 'brent':
            result = self._compute_brent(c)
        elif method == 'series':
            result = self._compute_series(c)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return result[0] if scalar_input else result
    
    def _H(self, x: np.ndarray) -> np.ndarray:
        """Compute H(x) = x + (log x)^2"""
        return x + np.log(x)**2
    
    def _H_prime(self, x: np.ndarray) -> np.ndarray:
        """Compute H'(x) = 1 + 2*log(x)/x"""
        return 1 + 2*np.log(x)/x
    
    def _H_double_prime(self, x: np.ndarray) -> np.ndarray:
        """Compute H''(x) = 2/x^2 - 2*log(x)/x^2"""
        return 2*(1 - np.log(x))/x**2
    
    def _initial_guess(self, c: np.ndarray) -> np.ndarray:
        """
        Compute intelligent initial guess for Φ(c).
        
        Uses asymptotic expansion for large c and series for small c.
        """
        # For c near 1, use series expansion
        small_c = c < 2
        large_c = ~small_c
        
        x0 = np.zeros_like(c)
        
        # Series expansion around c = 1: Φ(c) ≈ 1 + (c-1) - (c-1)^2 + ...
        if np.any(small_c):
            delta = c[small_c] - 1
            x0[small_c] = 1 + delta - delta**2 + delta**3
        
        # Asymptotic expansion: Φ(c) ≈ c - (log c)^2 + 2(log c)^3/c
        if np.any(large_c):
            log_c = np.log(c[large_c])
            x0[large_c] = c[large_c] - log_c**2 + 2*log_c**3/c[large_c]
        
        return x0
    
    def _compute_newton(self, c: np.ndarray) -> np.ndarray:
        """
        Compute Φ(c) using Newton's method.
        
        Newton iteration: x_{n+1} = x_n - f(x_n)/f'(x_n)
        where f(x) = x + (log x)^2 - c
        """
        x = self._initial_guess(c)
        
        for iteration in range(self.max_iter):
            f = self._H(x) - c
            fp = self._H_prime(x)
            
            # Newton step
            delta = f / fp
            x_new = x - delta
            
            # Ensure x stays positive
            x_new = np.maximum(x_new, 0.5)
            
            # Check convergence
            if np.all(np.abs(delta) < self.tol):
                return x_new
            
            x = x_new
        
        warnings.warn(f"Newton's method did not converge in {self.max_iter} iterations")
        return x
    
    def _compute_halley(self, c: np.ndarray) -> np.ndarray:
        """
        Compute Φ(c) using Halley's method (cubic convergence).
        
        Halley iteration: x_{n+1} = x_n - f/(f' - f*f''/(2*f'))
        """
        x = self._initial_guess(c)
        
        for iteration in range(self.max_iter):
            f = self._H(x) - c
            fp = self._H_prime(x)
            fpp = self._H_double_prime(x)
            
            # Halley step
            denominator = fp - 0.5 * f * fpp / fp
            delta = f / denominator
            x_new = x - delta
            
            # Ensure x stays positive
            x_new = np.maximum(x_new, 0.5)
            
            # Check convergence
            if np.all(np.abs(delta) < self.tol):
                return x_new
            
            x = x_new
        
        warnings.warn(f"Halley's method did not converge in {self.max_iter} iterations")
        return x
    
    def _compute_brent(self, c: np.ndarray) -> np.ndarray:
        """
        Compute Φ(c) using Brent's method (guaranteed convergence).
        
        More robust but slower than Newton's method.
        """
        result = np.zeros_like(c)
        
        for i, c_val in enumerate(c):
            def f(x):
                return self._H(np.array([x]))[0] - c_val
            
            # Bracket the root
            a, b = 1.0, float(c_val)
            
            # Ensure bracket is valid
            if f(a) * f(b) > 0:
                b = c_val + 10  # Expand upper bound
            
            try:
                result[i] = brentq(f, a, b, xtol=self.tol)
            except ValueError:
                # Fallback to Newton if bracket fails
                warnings.warn(f"Brent method failed for c={c_val}, using Newton")
                result[i] = self._compute_newton(np.array([c_val]))[0]
        
        return result
    
    def _compute_series(self, c: np.ndarray) -> np.ndarray:
        """
        Compute Φ(c) using series expansion (only accurate near c = 1).
        
        Valid for |c - 1| < 0.5
        """
        if np.any(np.abs(c - 1) > 0.5):
            warnings.warn("Series expansion only accurate for c near 1")
        
        delta = c - 1
        
        # Compute series coefficients (derived from Lagrange inversion)
        # Φ(c) = 1 + a₁(c-1) + a₂(c-1)² + a₃(c-1)³ + ...
        result = (1 + delta - delta**2 + (4/3)*delta**3 - (13/6)*delta**4 + 
                  (32/15)*delta**5)
        
        return result
    
    def _compute_auto(self, c: np.ndarray) -> np.ndarray:
        """
        Automatically select best method based on c values.
        """
        # Use series for c very close to 1
        very_close = np.abs(c - 1) < 0.1
        # Use Halley for moderate c (best convergence)
        moderate = (c >= 1.1) & (c < 1000)
        # Use Newton with good initial guess for large c
        large = c >= 1000
        
        result = np.zeros_like(c)
        
        if np.any(very_close):
            result[very_close] = self._compute_series(c[very_close])
        if np.any(moderate):
            result[moderate] = self._compute_halley(c[moderate])
        if np.any(large):
            result[large] = self._compute_newton(c[large])
        
        return result
    
    def derivative(self, c: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Compute Φ'(c) = 1 / (1 + 2*log(Φ(c))/Φ(c))
        
        Parameters
        ----------
        c : float or array_like
            Input value(s)
            
        Returns
        -------
        float or ndarray
            Φ'(c) value(s)
        """
        phi_c = self(c)
        return 1 / self._H_prime(phi_c)
    
    def second_derivative(self, c: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Compute Φ''(c) using implicit differentiation.
        
        Parameters
        ----------
        c : float or array_like
            Input value(s)
            
        Returns
        -------
        float or ndarray
            Φ''(c) value(s)
        """
        phi_c = self(c)
        phi_prime = self.derivative(c)
        
        # Φ''(c) = -H''(Φ(c)) * (Φ'(c))^3
        return -self._H_double_prime(phi_c) * phi_prime**3
    
    def bounds(self, c: Union[float, np.ndarray]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute rigorous bounds: c - (log c)^2 < Φ(c) < c
        
        Parameters
        ----------
        c : float or array_like
            Input value(s)
            
        Returns
        -------
        lower, upper : tuple of arrays
            Lower and upper bounds
        """
        c = np.atleast_1d(c)
        log_c = np.log(c)
        lower = c - log_c**2
        upper = c
        return lower, upper
    
    def asymptotic_approximation(self, c: Union[float, np.ndarray], 
                                 order: int = 3) -> Union[float, np.ndarray]:
        """
        Compute asymptotic approximation for large c.
        
        Φ(c) ≈ c - (log c)^2 + 2(log c)^3/c - O((log c)^4/c^2)
        
        Parameters
        ----------
        c : float or array_like
            Input value(s)
        order : int
            Order of approximation (1, 2, or 3)
            
        Returns
        -------
        float or ndarray
            Asymptotic approximation
        """
        c = np.atleast_1d(c)
        log_c = np.log(c)
        
        if order == 1:
            return c - log_c**2
        elif order == 2:
            return c - log_c**2 + 2*log_c**3/c
        elif order == 3:
            return c - log_c**2 + 2*log_c**3/c - 3*log_c**4/c**2
        else:
            raise ValueError("Order must be 1, 2, or 3")
    
    def error_estimate(self, c: Union[float, np.ndarray], 
                      computed_value: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Estimate numerical error in computed Φ(c).
        
        Parameters
        ----------
        c : float or array_like
            Input value(s)
        computed_value : array_like, optional
            Previously computed Φ(c); if None, compute it
            
        Returns
        -------
        ndarray
            Estimated absolute error
        """
        if computed_value is None:
            computed_value = self(c)
        
        # Residual: |H(Φ(c)) - c|
        residual = np.abs(self._H(computed_value) - c)
        
        # Error estimate: residual / |H'(Φ(c))|
        error = residual / np.abs(self._H_prime(computed_value))
        
        return error


def benchmark_methods():
    """
    Benchmark different numerical methods for computing Φ(c).
    """
    import time
    
    phi = PhiFunction(tolerance=1e-12)
    
    # Test values
    c_values = np.array([1.1, 2.0, 10.0, 100.0, 1000.0, 10000.0])
    methods = ['newton', 'halley', 'brent']
    
    print("Benchmark Results")
    print("=" * 70)
    print(f"{'c':<12} {'Method':<10} {'Result':<18} {'Time (ms)':<12} {'Error'}")
    print("-" * 70)
    
    for c in c_values:
        for method in methods:
            start = time.time()
            result = phi(c, method=method)
            elapsed = (time.time() - start) * 1000
            
            # Verify result
            error = phi.error_estimate(c, result)
            
            print(f"{c:<12.1f} {method:<10} {result:<18.12f} {elapsed:<12.4f} {error:.2e}")
    
    print("=" * 70)


if __name__ == "__main__":
    # Demonstration
    phi = PhiFunction()
    
    print("Φ Function Implementation Demo")
    print("=" * 50)
    
    # Single value
    c = 10.0
    result = phi(c)
    print(f"\nΦ({c}) = {result:.12f}")
    print(f"Verification: H(Φ({c})) = {phi._H(np.array([result]))[0]:.12f}")
    print(f"Error estimate: {phi.error_estimate(c, result):.2e}")
    
    # Derivative
    print(f"\nΦ'({c}) = {phi.derivative(c):.12f}")
    print(f"Φ''({c}) = {phi.second_derivative(c):.12f}")
    
    # Bounds
    lower, upper = phi.bounds(c)
    print(f"\nBounds: {lower[0]:.6f} < Φ({c}) < {upper[0]:.6f}")
    
    # Asymptotic
    asymp_val = phi.asymptotic_approximation(c, 3)
    print(f"\nAsymptotic approximation (order 3): {asymp_val[0] if isinstance(asymp_val, np.ndarray) else asymp_val:.12f}")
    
    # Array computation
    print("\n" + "=" * 50)
    print("Array Computation")
    c_array = np.array([1.5, 2, 5, 10, 50, 100])
    results = phi(c_array)
    
    print(f"\n{'c':<10} {'Φ(c)':<18} {'Error'}")
    print("-" * 40)
    for c_val, res in zip(c_array, results):
        err = phi.error_estimate(c_val, res)
        print(f"{c_val:<10.1f} {res:<18.12f} {err:.2e}")
    
    print("\n" + "=" * 50)
    print("\nRunning benchmark...")
    benchmark_methods()
