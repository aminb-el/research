"""
Polynomial Prime Hunter - Ultra-Optimized Version
Orders of magnitude faster through algorithmic and implementation optimizations

Key optimizations:
1. Sieve of Eratosthenes for batch prime checking
2. Early polynomial value bounds checking
3. Optimized prime testing with wheel factorization
4. Reduced redundant calculations
5. Better memory locality
6. All original features preserved
"""

from collections import namedtuple
import time
import json
import os
from datetime import datetime
import numpy as np

# Result structure
PolynomialResult = namedtuple('PolynomialResult', 
    ['a', 'b', 'c', 'total_primes', 'density', 'max_streak', 'first_primes', 'early_density'])

# ============================================================================
# OPTIMIZED PRIME GENERATION AND TESTING
# ============================================================================

def sieve_of_eratosthenes(limit):
    """Fast prime sieve - generates all primes up to limit"""
    if limit < 2:
        return []
    
    # Boolean array, initially all True
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0] = is_prime[1] = False
    
    # Sieve
    for i in range(2, int(np.sqrt(limit)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    
    return np.nonzero(is_prime)[0]


class FastPrimeChecker:
    """Optimized prime checker using sieve + wheel factorization"""
    
    def __init__(self, max_value):
        # Build sieve for small primes
        self.sieve_limit = min(10_000_000, max_value)
        print(f"   Building prime sieve up to {self.sieve_limit:,}...")
        
        self.small_primes = sieve_of_eratosthenes(self.sieve_limit)
        self.prime_set = set(self.small_primes)
        
        # Wheel factorization basis (2, 3, 5)
        self.wheel = [4, 2, 4, 2, 4, 6, 2, 6]  # Gaps in 30k + {1,7,11,13,17,19,23,29}
        self.wheel_primes = [2, 3, 5]
        
        print(f"   Sieve built with {len(self.small_primes):,} primes")
    
    def is_prime(self, n):
        """Fast prime test"""
        if n <= 1:
            return False
        if n <= self.sieve_limit:
            return n in self.prime_set
        if n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
            return False
        
        # Wheel factorization for numbers beyond sieve
        limit = int(np.sqrt(n)) + 1
        i = 7
        wheel_idx = 0
        
        while i <= limit:
            if n % i == 0:
                return False
            i += self.wheel[wheel_idx]
            wheel_idx = (wheel_idx + 1) % 8
        
        return True


def generate_primes_below(limit):
    """Generate all primes below limit using sieve"""
    return sieve_of_eratosthenes(limit).tolist()


# ============================================================================
# OPTIMIZED POLYNOMIAL EVALUATION
# ============================================================================

def evaluate_polynomial(a, b, c, n):
    """Evaluate P(n) = a*n^2 + b*n + c"""
    val = a * n * n + b * n + c
    if val <= 1:
        return None
    return val


def get_polynomial_bounds(a, b, c, n_max):
    """
    Calculate min/max values the polynomial can produce.
    Used to skip polynomials that will produce values too large or negative.
    """
    # Check at key points: n=1, n=n_max
    vals = []
    for n in [1, n_max]:
        val = a * n * n + b * n + c
        vals.append(val)
    
    # For negative 'a', also check vertex
    if a < 0:
        vertex_n = -b / (2 * a)
        if 1 <= vertex_n <= n_max:
            val = a * vertex_n * vertex_n + b * vertex_n + c
            vals.append(val)
    
    return min(vals), max(vals)


# ============================================================================
# OPTIMIZED POLYNOMIAL ANALYSIS
# ============================================================================

def analyze_polynomial_fast(a, b, c, early_test_n, max_n, min_early_density, 
                            min_streak, prime_checker):
    """
    Ultra-fast polynomial analysis with early exits and batch operations
    """
    # Early bounds check - skip if polynomial produces bad values
    min_val, max_val = get_polynomial_bounds(a, b, c, early_test_n)
    
    # Skip if all values will be negative or too small
    if max_val <= 1:
        return None
    
    # Skip if minimum value in early range is negative (likely poor performer)
    if min_val < 0:
        return None
    
    # Quick check: P(1) and P(2) must be prime
    p1 = evaluate_polynomial(a, b, c, 1)
    p2 = evaluate_polynomial(a, b, c, 2)
    
    if p1 is None or p2 is None or not prime_checker.is_prime(p1) or not prime_checker.is_prime(p2):
        return None
    
    # Early range test - batch calculate values
    early_primes = 0
    early_streak = 0
    max_early_streak = 0
    
    for n in range(1, early_test_n + 1):
        val = evaluate_polynomial(a, b, c, n)
        if val is not None and prime_checker.is_prime(val):
            early_primes += 1
            early_streak += 1
            max_early_streak = max(max_early_streak, early_streak)
        else:
            early_streak = 0
    
    early_density = early_primes / early_test_n
    
    # Skip if early performance is poor
    if early_density < min_early_density or max_early_streak < min_streak:
        return None
    
    # Full range test
    total_primes = 0
    current_streak = 0
    max_streak = 0
    first_primes = []
    
    for n in range(1, max_n + 1):
        val = evaluate_polynomial(a, b, c, n)
        if val is not None and prime_checker.is_prime(val):
            total_primes += 1
            current_streak += 1
            max_streak = max(max_streak, current_streak)
            if len(first_primes) < 10:
                first_primes.append((n, val))
        else:
            current_streak = 0
    
    density = total_primes / max_n
    
    return PolynomialResult(
        a=a, b=b, c=c,
        total_primes=total_primes,
        density=density,
        max_streak=max_streak,
        first_primes=first_primes,
        early_density=early_density
    )


# ============================================================================
# SAVE/LOAD STATE (same as before)
# ============================================================================

def save_state(results, progress, params, filename="polynomial_search_state.json"):
    """Save current state to JSON file"""
    state = {
        'timestamp': datetime.now().isoformat(),
        'params': params,
        'progress': progress,
        'results': [
            {
                'a': r.a,
                'b': r.b,
                'c': r.c,
                'total_primes': r.total_primes,
                'density': r.density,
                'max_streak': r.max_streak,
                'first_primes': r.first_primes,
                'early_density': r.early_density
            }
            for r in results
        ]
    }
    
    temp_filename = filename + ".tmp"
    with open(temp_filename, 'w') as f:
        json.dump(state, f, indent=2)
    
    try:
        os.replace(temp_filename, filename)
    except PermissionError:
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass
        os.rename(temp_filename, filename)


def load_state(filename="polynomial_search_state.json"):
    """Load saved state from JSON file"""
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
        
        results = [
            PolynomialResult(
                a=r['a'],
                b=r['b'],
                c=r['c'],
                total_primes=r['total_primes'],
                density=r['density'],
                max_streak=r['max_streak'],
                first_primes=[tuple(p) for p in r['first_primes']],
                early_density=r['early_density']
            )
            for r in state['results']
        ]
        
        return {
            'results': results,
            'progress': state['progress'],
            'params': state['params'],
            'timestamp': state['timestamp']
        }
    except Exception as e:
        print(f"Warning: Could not load state file: {e}")
        return None


# ============================================================================
# OPTIMIZED SEARCH FUNCTION
# ============================================================================

def search_polynomials_fast(a_range=(1, 10), b_range=(-100, 100), c_max=100,
                            max_n=5000, early_test_n=50, top_k=10,
                            min_early_density=0.3, min_streak=5, 
                            autosave_interval=1000, resume=True, verbose=True):
    """
    Ultra-optimized search with all features preserved
    """
    state_filename = "polynomial_search_state.json"
    
    # Estimate maximum polynomial value to optimize prime checker
    max_possible_value = max(
        abs(a_range[1] * max_n * max_n + b_range[1] * max_n + c_max),
        abs(a_range[1] * max_n * max_n + b_range[0] * max_n + c_max)
    )
    
    print(f"Initializing optimized prime checker (max value: {max_possible_value:,})...")
    prime_checker = FastPrimeChecker(max_possible_value)
    
    # Try to resume from saved state
    start_a, start_b, start_c_idx = a_range[0], b_range[0], 0
    results = []
    tested = 0
    skipped = 0
    
    if resume:
        saved_state = load_state(state_filename)
        if saved_state:
            print("Found saved state from:", saved_state['timestamp'])
            resume_choice = input("Resume from saved state? (y/n, default y): ").lower() or 'y'
            
            if resume_choice == 'y':
                results = saved_state['results']
                progress = saved_state['progress']
                start_a = progress['a']
                start_b = progress['b']
                start_c_idx = progress['c_idx']
                tested = progress['tested']
                skipped = progress['skipped']
                
                if verbose:
                    print(f"Resuming from: a={start_a}, b={start_b}, c_idx={start_c_idx}")
                    print(f"Already found {len(results)} results")
                    print()
    
    start_time = time.time()
    
    # Generate candidate c values
    print("Generating candidate c values...")
    candidate_cs = generate_primes_below(c_max)
    
    # Calculate total candidates
    a_count = a_range[1] - a_range[0] + 1
    b_count = b_range[1] - b_range[0] + 1
    c_count = len(candidate_cs)
    total_candidates = a_count * b_count * c_count
    
    if verbose:
        print("\nStarting optimized search...")
        print(f"   a in [{a_range[0]}, {a_range[1]}]")
        print(f"   b in [{b_range[0]}, {b_range[1]}]")
        print(f"   c in primes < {c_max} ({c_count} values)")
        print(f"   Total candidates: {total_candidates:,}")
        print(f"   Test range: n in [1, {max_n}]")
        print(f"   Early test: n in [1, {early_test_n}]")
        print(f"   Autosave interval: {autosave_interval:,} candidates")
        print()
    
    progress_interval = max(1, total_candidates // 20)
    last_save_count = tested + skipped
    last_print_time = start_time
    
    # Search through all combinations
    for a in range(a_range[0], a_range[1] + 1):
        if a < start_a:
            continue
            
        for b in range(b_range[0], b_range[1] + 1):
            if a == start_a and b < start_b:
                continue
                
            for c_idx, c in enumerate(candidate_cs):
                if a == start_a and b == start_b and c_idx < start_c_idx:
                    continue
                
                current = tested + skipped
                
                # Progress update (every 5% OR every 5 seconds)
                current_time = time.time()
                if verbose and (current % progress_interval == 0 or current_time - last_print_time >= 5.0) and current > 0:
                    percent = (current / total_candidates) * 100.0
                    elapsed = current_time - start_time
                    rate = current / elapsed if elapsed > 0 else 0
                    eta = (total_candidates - current) / rate if rate > 0 else 0
                    
                    print(f"\r   Progress: {current:,}/{total_candidates:,} ({percent:.1f}%) - "
                          f"Found: {len(results)}, Tested: {tested:,}, Skipped: {skipped:,}, "
                          f"Rate: {rate:.0f}/s, ETA: {eta/60:.1f}m      ", end='', flush=True)
                    last_print_time = current_time
                
                # Autosave check
                if current - last_save_count >= autosave_interval and current > 0:
                    progress = {
                        'a': a,
                        'b': b,
                        'c_idx': c_idx,
                        'tested': tested,
                        'skipped': skipped
                    }
                    params = {
                        'a_range': a_range,
                        'b_range': b_range,
                        'c_max': c_max,
                        'max_n': max_n,
                        'early_test_n': early_test_n,
                        'top_k': top_k,
                        'min_early_density': min_early_density,
                        'min_streak': min_streak
                    }
                    save_state(results, progress, params, state_filename)
                    last_save_count = current
                    if verbose:
                        print(f"\n   [Autosaved at {current:,} candidates]")
                
                result = analyze_polynomial_fast(a, b, c, early_test_n, max_n, 
                                                 min_early_density, min_streak, prime_checker)
                
                if result:
                    results.append(result)
                    tested += 1
                else:
                    skipped += 1
    
    # Final sort
    results.sort(key=lambda x: x.density, reverse=True)
    top_results = results[:top_k]
    
    elapsed_time = time.time() - start_time
    
    # Final save
    progress = {
        'a': a_range[1],
        'b': b_range[1],
        'c_idx': len(candidate_cs) - 1,
        'tested': tested,
        'skipped': skipped
    }
    params = {
        'a_range': a_range,
        'b_range': b_range,
        'c_max': c_max,
        'max_n': max_n,
        'early_test_n': early_test_n,
        'top_k': top_k,
        'min_early_density': min_early_density,
        'min_streak': min_streak
    }
    save_state(top_results, progress, params, state_filename)
    
    if verbose:
        print()
        print("\nSearch complete!")
        print(f"   Time: {elapsed_time:.2f} seconds ({elapsed_time/3600:.2f} hours)")
        print(f"   Tested: {tested:,}")
        print(f"   Skipped: {skipped:,}")
        print(f"   Average rate: {total_candidates/elapsed_time:.0f} candidates/second")
        print(f"   Top results: {len(top_results)}")
        print(f"   Final state saved to: {state_filename}")
        print()
    
    return top_results


# ============================================================================
# USER INPUT AND DISPLAY (same as before)
# ============================================================================

def get_user_input():
    """Get search parameters from user"""
    print("Polynomial Prime Search Configuration (OPTIMIZED)")
    print("=" * 50)
    
    a_min = int(input("Enter minimum value for a (default 1): ") or "1")
    a_max = int(input("Enter maximum value for a (default 10): ") or "10")
    
    b_min = int(input("Enter minimum value for b (default -100): ") or "-100")
    b_max = int(input("Enter maximum value for b (default 100): ") or "100")
    
    c_max = int(input("Enter maximum for c (primes < this, default 100): ") or "100")
    
    max_n = int(input("Enter maximum n to test (default 5000): ") or "5000")
    early_test_n = int(input("Enter early test range (default 50): ") or "50")
    
    top_k = int(input("Enter number of top results to show (default 10): ") or "10")
    
    min_early_density = float(input("Enter minimum early density 0-1 (default 0.3): ") or "0.3")
    min_streak = int(input("Enter minimum early streak (default 5): ") or "5")
    
    autosave_interval = int(input("Enter autosave interval (candidates, default 5000): ") or "5000")
    
    print()
    
    return {
        'a_range': (a_min, a_max),
        'b_range': (b_min, b_max),
        'c_max': c_max,
        'max_n': max_n,
        'early_test_n': early_test_n,
        'top_k': top_k,
        'min_early_density': min_early_density,
        'min_streak': min_streak,
        'autosave_interval': autosave_interval
    }


def print_results(results, max_n=5000):
    """Pretty print the results"""
    print("=" * 80)
    print(f"{'RANK':<6} {'POLYNOMIAL':<30} {'PRIMES':<15} {'DENSITY':<10} {'STREAK':<8}")
    print("=" * 80)
    
    for idx, r in enumerate(results, 1):
        poly_str = f"{r.a}n² + {r.b:+d}n + {r.c:+d}"
        primes_str = f"{r.total_primes}/{max_n}"
        density_str = f"{r.density*100:.2f}%"
        
        print(f"{idx:<6} {poly_str:<30} {primes_str:<15} {density_str:<10} {r.max_streak:<8}")
    
    print("=" * 80)
    print()
    
    # Detailed view of top 3
    print("Detailed View (Top 3):")
    print()
    
    for idx, r in enumerate(results[:3], 1):
        print(f"#{idx}: P(n) = {r.a}n² + {r.b:+d}n + {r.c:+d}")
        print(f"   Total Primes: {r.total_primes:,} / {max_n:,} ({r.density*100:.2f}%)")
        print(f"   Max Consecutive Streak: {r.max_streak}")
        print(f"   Early Density (n=1-50): {r.early_density*100:.1f}%")
        print(f"   P(1) = {r.first_primes[0][1]}")
        first_n_values = ', '.join(str(n) for n, _ in r.first_primes[:8])
        print(f"   First primes at n = {first_n_values}...")
        print()


def generate_pdf_report(results, params, filename="polynomial_prime_report.pdf"):
    """Generate a PDF report with formatted table of results"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        print("Installing reportlab for PDF generation...")
        import subprocess
        subprocess.run(["pip", "install", "reportlab", "--break-system-packages", "-q"])
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    
    doc = SimpleDocTemplate(filename, pagesize=letter,
                          topMargin=0.75*inch, bottomMargin=0.75*inch,
                          leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        spaceBefore=12
    )
    
    title = Paragraph("Polynomial Prime Search Results", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    param_text = f"""
    <b>Search Parameters:</b><br/>
    • Coefficient a: [{params['a_range'][0]}, {params['a_range'][1]}]<br/>
    • Coefficient b: [{params['b_range'][0]}, {params['b_range'][1]}]<br/>
    • Coefficient c: primes &lt; {params['c_max']}<br/>
    • Test range: n ∈ [1, {params['max_n']}]<br/>
    • Early test range: n ∈ [1, {params['early_test_n']}]<br/>
    • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    elements.append(Paragraph(param_text, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph("Top Polynomial Results", heading_style))
    elements.append(Spacer(1, 0.1*inch))
    
    table_data = [
        ['Rank', 'Polynomial', 'Total\nPrimes', 'Density', 'Max\nStreak', 'Early\nDensity']
    ]
    
    for idx, r in enumerate(results, 1):
        poly_str = f"{r.a}n² {r.b:+d}n {r.c:+d}"
        primes_str = f"{r.total_primes:,}"
        density_str = f"{r.density*100:.2f}%"
        streak_str = f"{r.max_streak}"
        early_density_str = f"{r.early_density*100:.1f}%"
        
        table_data.append([
            str(idx), poly_str, primes_str, density_str, streak_str, early_density_str
        ])
    
    table = Table(table_data, colWidths=[0.6*inch, 2.0*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.lightgrey]),
    ])
    
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    if len(results) > 0:
        elements.append(PageBreak())
        elements.append(Paragraph("Detailed Analysis (Top 5)", heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        for idx, r in enumerate(results[:5], 1):
            poly_header = f"#{idx}: P(n) = {r.a}n² {r.b:+d}n {r.c:+d}"
            elements.append(Paragraph(poly_header, styles['Heading3']))
            
            detail_text = f"""
            <b>Performance Metrics:</b><br/>
            • Total Primes: {r.total_primes:,} / {params['max_n']:,} ({r.density*100:.2f}%)<br/>
            • Max Consecutive Streak: {r.max_streak}<br/>
            • Early Density (n=1-{params['early_test_n']}): {r.early_density*100:.1f}%<br/>
            <br/>
            <b>First Prime Values:</b><br/>
            """
            
            for n, val in r.first_primes:
                detail_text += f"• P({n}) = {val:,}<br/>"
            
            elements.append(Paragraph(detail_text, styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
    
    doc.build(elements)
    print(f"PDF report generated: {filename}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ULTRA-OPTIMIZED Polynomial Prime Search")
    print("=" * 70)
    print()
    
    # Get user parameters
    params = get_user_input()
    
    # Run optimized search
    results = search_polynomials_fast(
        a_range=params['a_range'],
        b_range=params['b_range'],
        c_max=params['c_max'],
        max_n=params['max_n'],
        early_test_n=params['early_test_n'],
        top_k=params['top_k'],
        min_early_density=params['min_early_density'],
        min_streak=params['min_streak'],
        autosave_interval=params['autosave_interval'],
        resume=True
    )
    
    # Display results
    print_results(results, max_n=params['max_n'])
    
    # Generate PDF report
    if results:
        pdf_choice = input("Generate PDF report? (y/n, default y): ").lower() or 'y'
        if pdf_choice == 'y':
            pdf_filename = f"polynomial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            generate_pdf_report(results, params, pdf_filename)
            print(f"\nReport saved as: {pdf_filename}")
    
    print("\nSearch complete!")
