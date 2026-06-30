"""
Phi Function Visualizations
============================

Beautiful, publication-quality visualizations of the Φ function.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.gridspec as gridspec
from phi_function import PhiFunction
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['lines.linewidth'] = 2


def plot_main_function():
    """
    Plot Φ(c) and H(x) to show they are inverses.
    """
    phi = PhiFunction()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left plot: Φ(c) and its bounds
    c_vals = np.linspace(1.01, 20, 500)
    phi_vals = phi(c_vals)
    lower, upper = phi.bounds(c_vals)
    
    ax1.plot(c_vals, phi_vals, 'b-', linewidth=2.5, label=r'$\Phi(c)$')
    ax1.plot(c_vals, lower, 'r--', linewidth=1.5, alpha=0.7, 
             label=r'Lower bound: $c - (\log c)^2$')
    ax1.plot(c_vals, upper, 'g--', linewidth=1.5, alpha=0.7, 
             label=r'Upper bound: $c$')
    ax1.fill_between(c_vals, lower, upper, alpha=0.1, color='gray')
    
    ax1.set_xlabel(r'$c$', fontsize=12)
    ax1.set_ylabel(r'$x$', fontsize=12)
    ax1.set_title(r'The function $\Phi(c)$: solution to $x + (\log x)^2 = c$', 
                  fontsize=13)
    ax1.legend(loc='upper left', framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim([1, 20])
    
    # Right plot: H(x) and the line y = c
    x_vals = np.linspace(1.01, 15, 500)
    H_vals = phi._H(x_vals)
    
    ax2.plot(x_vals, H_vals, 'b-', linewidth=2.5, label=r'$H(x) = x + (\log x)^2$')
    
    # Show several horizontal lines y = c
    c_examples = [2, 5, 10, 15]
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(c_examples)))
    
    for c_ex, color in zip(c_examples, colors):
        ax2.axhline(y=c_ex, color=color, linestyle='--', alpha=0.6, linewidth=1.5)
        phi_c = phi(c_ex)
        ax2.plot(phi_c, c_ex, 'o', color=color, markersize=8, 
                label=rf'$c={c_ex}$: $\Phi({c_ex})={phi_c:.2f}$')
    
    ax2.set_xlabel(r'$x$', fontsize=12)
    ax2.set_ylabel(r'$y$', fontsize=12)
    ax2.set_title(r'$H(x) = x + (\log x)^2$ and horizontal lines $y = c$', 
                  fontsize=13)
    ax2.legend(loc='upper left', framealpha=0.95, fontsize=8)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_xlim([1, 15])
    ax2.set_ylim([0, 20])
    
    plt.tight_layout()
    plt.savefig('/home/claude/phi_function_monograph/visualizations/main_function.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: main_function.png")
    plt.close()


def plot_derivatives():
    """
    Plot Φ'(c) and Φ''(c) to show monotonicity and convexity.
    """
    phi = PhiFunction()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    c_vals = np.linspace(1.01, 30, 500)
    phi_vals = phi(c_vals)
    phi_prime = phi.derivative(c_vals)
    phi_double_prime = phi.second_derivative(c_vals)
    
    # First derivative
    ax1.plot(c_vals, phi_prime, 'b-', linewidth=2.5)
    ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.5, label=r"$\Phi'(c) = 1$ asymptote")
    ax1.set_xlabel(r'$c$', fontsize=12)
    ax1.set_ylabel(r"$\Phi'(c)$", fontsize=12)
    ax1.set_title(r"First derivative: $\Phi'(c) = \frac{1}{1 + 2\log(\Phi(c))/\Phi(c)}$", 
                  fontsize=12)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(framealpha=0.95)
    ax1.set_ylim([0, 1.1])
    
    # Second derivative (showing inflection point)
    ax2.plot(c_vals, phi_double_prime, 'r-', linewidth=2.5)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
    
    # Mark inflection point (occurs when Φ(c) = e)
    e = np.e
    c_inflection = e + (np.log(e))**2  # c value where Φ(c) = e
    ax2.axvline(x=c_inflection, color='green', linestyle='--', alpha=0.7, 
                label=f'Inflection point: $c \\approx {c_inflection:.2f}$')
    
    ax2.set_xlabel(r'$c$', fontsize=12)
    ax2.set_ylabel(r"$\Phi''(c)$", fontsize=12)
    ax2.set_title(r"Second derivative: changes sign at $\Phi(c) = e$", fontsize=12)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(framealpha=0.95)
    
    plt.tight_layout()
    plt.savefig('/home/claude/phi_function_monograph/visualizations/derivatives.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: derivatives.png")
    plt.close()


def plot_asymptotic_behavior():
    """
    Show how asymptotic approximations converge to Φ(c) for large c.
    """
    phi = PhiFunction()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Large c behavior
    c_vals = np.logspace(0.5, 3, 500)  # 10^0.5 to 10^3
    phi_vals = phi(c_vals)
    
    approx_1 = phi.asymptotic_approximation(c_vals, order=1)
    approx_2 = phi.asymptotic_approximation(c_vals, order=2)
    approx_3 = phi.asymptotic_approximation(c_vals, order=3)
    
    ax1.semilogx(c_vals, phi_vals, 'k-', linewidth=3, label=r'$\Phi(c)$ (exact)', zorder=5)
    ax1.semilogx(c_vals, approx_1, 'b--', linewidth=2, alpha=0.7, 
                 label=r'$c - (\log c)^2$')
    ax1.semilogx(c_vals, approx_2, 'g--', linewidth=2, alpha=0.7, 
                 label=r'$c - (\log c)^2 + 2(\log c)^3/c$')
    ax1.semilogx(c_vals, approx_3, 'r--', linewidth=2, alpha=0.7, 
                 label=r'$c - (\log c)^2 + 2(\log c)^3/c - 3(\log c)^4/c^2$')
    
    ax1.set_xlabel(r'$c$ (log scale)', fontsize=12)
    ax1.set_ylabel(r'$\Phi(c)$', fontsize=12)
    ax1.set_title('Asymptotic approximations for large $c$', fontsize=13)
    ax1.legend(framealpha=0.95, loc='upper left')
    ax1.grid(True, alpha=0.3, linestyle='--', which='both')
    
    # Relative error
    rel_error_1 = np.abs((approx_1 - phi_vals) / phi_vals)
    rel_error_2 = np.abs((approx_2 - phi_vals) / phi_vals)
    rel_error_3 = np.abs((approx_3 - phi_vals) / phi_vals)
    
    ax2.loglog(c_vals, rel_error_1, 'b-', linewidth=2, label='Order 1')
    ax2.loglog(c_vals, rel_error_2, 'g-', linewidth=2, label='Order 2')
    ax2.loglog(c_vals, rel_error_3, 'r-', linewidth=2, label='Order 3')
    
    ax2.set_xlabel(r'$c$ (log scale)', fontsize=12)
    ax2.set_ylabel('Relative Error', fontsize=12)
    ax2.set_title('Convergence of asymptotic approximations', fontsize=13)
    ax2.legend(framealpha=0.95)
    ax2.grid(True, alpha=0.3, linestyle='--', which='both')
    
    plt.tight_layout()
    plt.savefig('/home/claude/phi_function_monograph/visualizations/asymptotic.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: asymptotic.png")
    plt.close()


def plot_near_endpoint():
    """
    Behavior of Φ(c) near c = 1.
    """
    phi = PhiFunction()
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    
    # Very close to c = 1
    c_vals = np.linspace(1.001, 1.5, 500)
    phi_vals = phi(c_vals)
    
    # Series approximation
    series_approx = phi._compute_series(c_vals)
    
    ax.plot(c_vals, phi_vals, 'b-', linewidth=3, label=r'$\Phi(c)$ (exact)')
    ax.plot(c_vals, series_approx, 'r--', linewidth=2, alpha=0.7, 
            label=r'Series: $1 + (c-1) - (c-1)^2 + \frac{4}{3}(c-1)^3 + ...$')
    
    # Show linear approximation
    ax.plot(c_vals, 1 + (c_vals - 1), 'g:', linewidth=2, alpha=0.6, 
            label=r'Linear: $1 + (c-1)$')
    
    ax.axhline(y=1, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.3)
    
    ax.set_xlabel(r'$c$', fontsize=12)
    ax.set_ylabel(r'$\Phi(c)$', fontsize=12)
    ax.set_title(r'Behavior near $c = 1$: $\lim_{c \to 1^+} \Phi(c) = 1$', fontsize=13)
    ax.legend(framealpha=0.95)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim([1, 1.5])
    ax.set_ylim([1, 1.35])
    
    plt.tight_layout()
    plt.savefig('/home/claude/phi_function_monograph/visualizations/near_endpoint.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: near_endpoint.png")
    plt.close()


def plot_convergence_analysis():
    """
    Show Newton vs Halley convergence rates.
    """
    phi = PhiFunction()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    c = 100.0
    true_value = phi(c, method='halley')  # High-precision value
    
    # Manual Newton iterations
    x = phi._initial_guess(np.array([c]))[0]
    newton_errors = []
    newton_iterations = []
    
    for i in range(15):
        newton_iterations.append(i)
        error = np.abs(x - true_value)
        newton_errors.append(error)
        
        if error < 1e-15:
            break
        
        # Newton step
        f = x + np.log(x)**2 - c
        fp = 1 + 2*np.log(x)/x
        x = x - f/fp
    
    # Manual Halley iterations
    x = phi._initial_guess(np.array([c]))[0]
    halley_errors = []
    halley_iterations = []
    
    for i in range(15):
        halley_iterations.append(i)
        error = np.abs(x - true_value)
        halley_errors.append(error)
        
        if error < 1e-15:
            break
        
        # Halley step
        log_x = np.log(x)
        f = x + log_x**2 - c
        fp = 1 + 2*log_x/x
        fpp = 2*(1 - log_x)/x**2
        denominator = fp - 0.5 * f * fpp / fp
        x = x - f/denominator
    
    # Plot convergence
    ax1.semilogy(newton_iterations, newton_errors, 'bo-', linewidth=2, 
                 markersize=8, label='Newton (quadratic)')
    ax1.semilogy(halley_iterations, halley_errors, 'rs-', linewidth=2, 
                 markersize=8, label='Halley (cubic)')
    
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Absolute Error', fontsize=12)
    ax1.set_title(f'Convergence comparison for $c = {c}$', fontsize=13)
    ax1.legend(framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--', which='both')
    
    # Convergence rate visualization
    if len(newton_errors) > 2:
        newton_ratios = [newton_errors[i+1] / newton_errors[i]**2 
                        for i in range(len(newton_errors)-1) 
                        if newton_errors[i] > 1e-14]
        ax2.plot(newton_ratios, 'bo-', linewidth=2, markersize=8, 
                label='Newton: $e_{n+1}/e_n^2$ (quadratic)')
    
    if len(halley_errors) > 2:
        halley_ratios = [halley_errors[i+1] / halley_errors[i]**3 
                        for i in range(len(halley_errors)-1) 
                        if halley_errors[i] > 1e-14]
        ax2.plot(halley_ratios, 'rs-', linewidth=2, markersize=8, 
                label='Halley: $e_{n+1}/e_n^3$ (cubic)')
    
    ax2.set_xlabel('Iteration', fontsize=12)
    ax2.set_ylabel('Convergence Ratio', fontsize=12)
    ax2.set_title('Convergence rate analysis', fontsize=13)
    ax2.legend(framealpha=0.95)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('/home/claude/phi_function_monograph/visualizations/convergence.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: convergence.png")
    plt.close()


def plot_comprehensive_panel():
    """
    Create a comprehensive 6-panel figure showing all key properties.
    """
    phi = PhiFunction()
    
    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(3, 2, hspace=0.3, wspace=0.25)
    
    # Panel 1: Main function
    ax1 = fig.add_subplot(gs[0, 0])
    c_vals = np.linspace(1.01, 30, 500)
    phi_vals = phi(c_vals)
    ax1.plot(c_vals, phi_vals, 'b-', linewidth=2.5)
    ax1.plot(c_vals, c_vals, 'k--', alpha=0.3, label=r'$y = c$')
    ax1.set_xlabel(r'$c$', fontsize=11)
    ax1.set_ylabel(r'$\Phi(c)$', fontsize=11)
    ax1.set_title(r'(a) The function $\Phi(c)$', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Inverse relationship
    ax2 = fig.add_subplot(gs[0, 1])
    x_vals = np.linspace(1.01, 20, 300)
    H_vals = phi._H(x_vals)
    ax2.plot(x_vals, H_vals, 'b-', linewidth=2.5, label=r'$H(x) = x + (\log x)^2$')
    ax2.plot(H_vals, x_vals, 'r-', linewidth=2.5, alpha=0.7, label=r'$\Phi(c)$ (inverse)')
    ax2.plot([0, 25], [0, 25], 'k--', alpha=0.3, label=r'$y = x$')
    ax2.set_xlabel(r'$x$', fontsize=11)
    ax2.set_ylabel(r'$y$', fontsize=11)
    ax2.set_title(r'(b) $H$ and $\Phi$ are inverses', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, 25])
    ax2.set_ylim([0, 25])
    
    # Panel 3: First derivative
    ax3 = fig.add_subplot(gs[1, 0])
    phi_prime = phi.derivative(c_vals)
    ax3.plot(c_vals, phi_prime, 'g-', linewidth=2.5)
    ax3.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    ax3.set_xlabel(r'$c$', fontsize=11)
    ax3.set_ylabel(r"$\Phi'(c)$", fontsize=11)
    ax3.set_title(r"(c) Monotonicity: $\Phi'(c) > 0$", fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim([0, 1.1])
    
    # Panel 4: Second derivative (convexity)
    ax4 = fig.add_subplot(gs[1, 1])
    phi_double_prime = phi.second_derivative(c_vals)
    ax4.plot(c_vals, phi_double_prime, 'r-', linewidth=2.5)
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    e = np.e
    c_inflection = e + 1  # Approximate
    ax4.axvline(x=c_inflection, color='purple', linestyle='--', alpha=0.7)
    ax4.set_xlabel(r'$c$', fontsize=11)
    ax4.set_ylabel(r"$\Phi''(c)$", fontsize=11)
    ax4.set_title(r"(d) Inflection point at $\Phi(c) = e$", fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Panel 5: Asymptotic behavior
    ax5 = fig.add_subplot(gs[2, 0])
    c_large = np.logspace(0.5, 3, 300)
    phi_large = phi(c_large)
    approx = phi.asymptotic_approximation(c_large, order=2)
    ax5.semilogx(c_large, phi_large, 'b-', linewidth=2.5, label=r'$\Phi(c)$')
    ax5.semilogx(c_large, approx, 'r--', linewidth=2, label=r'$c - (\log c)^2 + 2(\log c)^3/c$')
    ax5.set_xlabel(r'$c$ (log scale)', fontsize=11)
    ax5.set_ylabel(r'$\Phi(c)$', fontsize=11)
    ax5.set_title(r'(e) Asymptotic expansion', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3, which='both')
    
    # Panel 6: Near endpoint
    ax6 = fig.add_subplot(gs[2, 1])
    c_small = np.linspace(1.001, 2, 300)
    phi_small = phi(c_small)
    ax6.plot(c_small, phi_small, 'b-', linewidth=2.5, label=r'$\Phi(c)$')
    ax6.plot(c_small, 1 + (c_small - 1), 'r--', linewidth=2, label=r'$1 + (c-1)$')
    ax6.axhline(y=1, color='gray', linestyle='--', alpha=0.3)
    ax6.axvline(x=1, color='gray', linestyle='--', alpha=0.3)
    ax6.set_xlabel(r'$c$', fontsize=11)
    ax6.set_ylabel(r'$\Phi(c)$', fontsize=11)
    ax6.set_title(r'(f) Behavior near $c = 1$', fontsize=12, fontweight='bold')
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)
    
    plt.suptitle(r'Comprehensive Analysis of $\Phi(c)$: The Inverse of $H(x) = x + (\log x)^2$', 
                 fontsize=15, fontweight='bold', y=0.995)
    
    plt.savefig('/home/claude/phi_function_monograph/visualizations/comprehensive_panel.png', 
                dpi=300, bbox_inches='tight')
    print("✓ Saved: comprehensive_panel.png")
    plt.close()


def create_all_visualizations():
    """Generate all visualization figures."""
    print("\nGenerating Visualizations")
    print("=" * 50)
    
    plot_main_function()
    plot_derivatives()
    plot_asymptotic_behavior()
    plot_near_endpoint()
    plot_convergence_analysis()
    plot_comprehensive_panel()
    
    print("\n" + "=" * 50)
    print("All visualizations completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    create_all_visualizations()
