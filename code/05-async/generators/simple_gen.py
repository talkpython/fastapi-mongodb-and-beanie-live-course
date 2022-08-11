# TODO: Implement basic fib via lists
# TODO: Implement fib via generators
from typing import Iterator


# 1, 1, 2, 3, 5, 8, 13, 21, ...

def basic_fib(limit) -> list[int]:
    numbers = []
    current, nxt = 1, 1

    while len(numbers) < limit:
        numbers.append(current)
        current, nxt = nxt, nxt + current

    return numbers


def gen_fib() -> Iterator[int]:
    current, nxt = 1, 1

    while True:
        # numbers.append(current)
        yield current
        current, nxt = nxt, nxt + current


fibs = gen_fib()
# print(fibs)

for n in gen_fib():
    print(n, end=', ')

    if n > 10_000:
        break


