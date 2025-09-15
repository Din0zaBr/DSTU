def main() -> None:
    digit_in_eighth: list = input().split()

    for digit in digit_in_eighth:
        print(int(digit, 8))


if __name__ == "__main__":
    main()
