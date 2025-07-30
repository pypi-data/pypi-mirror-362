import pytest


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


class TestFibonacci:
    def test_fibonacci_base_cases(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
    
    def test_fibonacci_small_positive_numbers(self):
        assert fibonacci(2) == 1
        assert fibonacci(3) == 2
        assert fibonacci(4) == 3
        assert fibonacci(5) == 5
        assert fibonacci(6) == 8
        assert fibonacci(7) == 13
        assert fibonacci(8) == 21
        assert fibonacci(9) == 34
        assert fibonacci(10) == 55
    
    def test_fibonacci_negative_numbers(self):
        # Current implementation returns the number itself for n <= 1
        assert fibonacci(-1) == -1
        assert fibonacci(-5) == -5
    
    def test_fibonacci_sequence_property(self):
        # Test that fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)
        for n in range(2, 12):
            assert fibonacci(n) == fibonacci(n-1) + fibonacci(n-2)


class TestIsPrime:
    def test_is_prime_less_than_2(self):
        assert is_prime(-5) == False
        assert is_prime(-1) == False
        assert is_prime(0) == False
        assert is_prime(1) == False
    
    def test_is_prime_2(self):
        # 2 is the only even prime number
        assert is_prime(2) == True
    
    def test_is_prime_small_primes(self):
        small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        for prime in small_primes:
            assert is_prime(prime) == True
    
    def test_is_prime_small_composites(self):
        small_composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]
        for composite in small_composites:
            assert is_prime(composite) == False
    
    def test_is_prime_perfect_squares(self):
        # Perfect squares (except 1) are always composite
        perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
        for square in perfect_squares:
            assert is_prime(square) == False
    
    def test_is_prime_larger_primes(self):
        larger_primes = [53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        for prime in larger_primes:
            assert is_prime(prime) == True
    
    def test_is_prime_larger_composites(self):
        larger_composites = [51, 57, 63, 69, 75, 81, 87, 93, 99, 105, 111, 117, 123, 129, 135]
        for composite in larger_composites:
            assert is_prime(composite) == False
    
    def test_is_prime_edge_cases(self):
        # Test some edge cases around square roots
        assert is_prime(49) == False  # 7^2
        assert is_prime(121) == False  # 11^2
        assert is_prime(169) == False  # 13^2
        assert is_prime(289) == False  # 17^2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])