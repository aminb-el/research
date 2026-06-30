import math
from functools import reduce
from operator import mul

def sieve_of_eratosthenes(limit):
    """Generate all primes up to limit."""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, limit + 1) if is_prime[i]]

def get_divisors(n):
    """Get all divisors of n."""
    divisors = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    return sorted(divisors)

def can_represent_all(divisors, target):
    """
    Check if all numbers from 1 to target can be represented
    as sums of distinct divisors.
    Returns (True/False, unreachable_numbers)
    """
    # DP: reachable[i] = True if i can be represented
    reachable = [False] * (target + 1)
    reachable[0] = True  # empty sum = 0
    
    for d in divisors:
        # Process in reverse to avoid using same divisor twice
        for i in range(target, d - 1, -1):
            if reachable[i - d]:
                reachable[i] = True
    
    unreachable = [i for i in range(1, target + 1) if not reachable[i]]
    return len(unreachable) == 0, unreachable

def is_practical(m):
    """Check if m is a practical number."""
    if m == 1:
        return True
    
    divisors = get_divisors(m)
    can_represent, _ = can_represent_all(divisors, m - 1)
    return can_represent

def compute_h(m, divisors):
    """
    Compute h(m): minimum number of divisors needed such that
    ANY choice of h(m) divisors can represent all 1..m-1.
    
    Actually, this is hard to compute directly. Instead, we compute:
    - The minimum number of divisors needed to represent each number
    - Return the maximum of these
    """
    # DP: min_divisors[i] = minimum number of divisors needed to make i
    min_divisors = [float('inf')] * m
    min_divisors[0] = 0
    
    for i in range(1, m):
        for d in divisors:
            if d <= i and min_divisors[i - d] != float('inf'):
                min_divisors[i] = min(min_divisors[i], min_divisors[i - d] + 1)
    
    # h(m) is the maximum number of divisors needed for any number < m
    h = max(min_divisors[1:])
    return h, min_divisors

def analyze_primorial(k, primes):
    """Analyze the k-th primorial (product of first k primes)."""
    if k == 0:
        return None
    
    primorial_primes = primes[:k]
    m = reduce(mul, primorial_primes, 1)
    
    print(f"\n{'='*70}")
    print(f"PRIMORIAL #{k}: P_{k} = {' × '.join(map(str, primorial_primes))} = {m}")
    print(f"{'='*70}")
    
    # Get divisors
    divisors = get_divisors(m)
    print(f"Number of divisors: d(P_{k}) = {len(divisors)}")
    print(f"Divisors: {divisors[:20]}{'...' if len(divisors) > 20 else ''}")
    
    # Check if practical
    is_prac = is_practical(m)
    print(f"\nIs P_{k} practical? {is_prac}")
    
    if not is_prac:
        _, unreachable = can_represent_all(divisors, m - 1)
        print(f"  Unreachable numbers: {unreachable[:10]}{'...' if len(unreachable) > 10 else ''}")
        return None
    
    # Compute h(m)
    h_value, min_div_needed = compute_h(m, divisors)
    
    print(f"\nRepresentation analysis:")
    print(f"  h(P_{k}) = {h_value}")
    print(f"  log(P_{k}) = {math.log(m):.4f}")
    print(f"  log(log(P_{k})) = {math.log(math.log(m)):.4f}")
    
    # Show which numbers need the most divisors
    max_needed = max(min_div_needed[1:])
    numbers_needing_max = [i for i in range(1, m) if min_div_needed[i] == max_needed]
    print(f"  Numbers needing {max_needed} divisors: {numbers_needing_max[:10]}")
    
    # Theoretical bounds
    log_m = math.log(m)
    log_log_m = math.log(log_m)
    
    print(f"\nGrowth rate analysis:")
    print(f"  h(P_{k}) / log(P_{k}) = {h_value / log_m:.6f}")
    print(f"  h(P_{k}) / log(log(P_{k})) = {h_value / log_log_m:.6f}")
    print(f"  h(P_{k}) / k = {h_value / k:.6f}")
    
    # Compare to theoretical prediction
    predicted_h = log_m / log_log_m
    print(f"\nPredicted h (log m / log log m) = {predicted_h:.4f}")
    print(f"Actual h = {h_value}")
    print(f"Ratio (actual/predicted) = {h_value / predicted_h:.4f}")
    
    return {
        'k': k,
        'm': m,
        'h': h_value,
        'num_divisors': len(divisors),
        'log_m': log_m,
        'log_log_m': log_log_m,
        'ratio_h_to_log': h_value / log_m,
        'ratio_h_to_k': h_value / k
    }

def main():
    print("PRIMORIAL PRACTICAL NUMBER ANALYSIS")
    print("="*70)
    
    # Generate enough primes
    primes = sieve_of_eratosthenes(100)
    print(f"Generated {len(primes)} primes: {primes[:20]}...")
    
    # Test primorials
    max_k = int(input("\nHow many primorials to test? (recommend ≤ 10 for speed): "))
    
    results = []
    for k in range(1, max_k + 1):
        result = analyze_primorial(k, primes)
        if result:
            results.append(result)
    
    # Summary table
    print(f"\n{'='*70}")
    print("SUMMARY TABLE")
    print(f"{'='*70}")
    print(f"{'k':<4} {'m':<15} {'d(m)':<8} {'h(m)':<8} {'h/log(m)':<12} {'h/k':<10}")
    print("-"*70)
    
    for r in results:
        print(f"{r['k']:<4} {r['m']:<15} {r['num_divisors']:<8} {r['h']:<8} "
              f"{r['ratio_h_to_log']:<12.6f} {r['ratio_h_to_k']:<10.4f}")
    
    # Theoretical analysis
    print(f"\n{'='*70}")
    print("THEORETICAL IMPLICATIONS")
    print(f"{'='*70}")
    
    if results:
        last = results[-1]
        print(f"\nFor P_{last['k']} = {last['m']}:")
        print(f"  h(P_{last['k']}) = {last['h']}")
        print(f"  k = {last['k']}")
        print(f"  h ≈ k? {abs(last['h'] - last['k']) <= 2}")
        print(f"\nIf h(primorial_k) ≈ k for all k:")
        print(f"  And primorial_k ≈ e^(k log k) by Prime Number Theorem")
        print(f"  Then log(primorial_k) ≈ k log k")
        print(f"  So k ≈ log(m) / log(log(m))")
        print(f"  Therefore h(m) = O(log(m) / log(log(m)))")
        print(f"\nThis is BETTER than (log m)^O(1) for large m!")
        print(f"Answer to the problem: YES (if primorials work)!")

if __name__ == "__main__":
    main()
