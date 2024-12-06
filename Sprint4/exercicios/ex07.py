def pares_ate(n: int):
    for num in range(2, n + 1, 2):
        yield num
