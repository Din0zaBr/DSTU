from math import factorial


def main() -> None:
    N: int = int(input())
    S = 0
    for digit in range(1, N + 1):
        S += (-1) ^ digit * factorial(2 * digit + 1)
    print(S)


if __name__ == "__main__":
    main()
