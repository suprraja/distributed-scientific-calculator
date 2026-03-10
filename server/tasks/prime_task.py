def compute_primes(limit):
    """
    Returns a list of all prime numbers up to 'limit' using Sieve of Eratosthenes.
    Also returns summary stats for nicer response.
    """
    if limit < 2:
        return {
            "status": "success",
            "primes": [],
            "count": 0,
            "largest": None,
            "message": "No primes below 2"
        }

    # Sieve implementation
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False

    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False

    primes = [i for i in range(2, limit + 1) if sieve[i]]

    return {
        "status": "success",
        "count": len(primes),
        "largest": primes[-1] if primes else None,
        "primes_sample": primes[:10] + ["..."] + primes[-5:] if len(primes) > 15 else primes,
        "full_list_returned": len(primes) <= 1000   # we won't send huge lists over network
    }


def handle_prime_request(data):
    """
    Wrapper to parse input and call compute_primes
    """
    try:
        limit = int(data.get("limit", 100))
        if limit > 1000000:
            return {
                "status": "error",
                "message": "Limit too large (max 1,000,000 for safety)"
            }
        result = compute_primes(limit)
        return result
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid limit (must be integer)"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
