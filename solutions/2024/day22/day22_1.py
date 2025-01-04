from handy_dandy_library.file_processing import read_lines


def evolve_secret(secret: int) -> int:
    secret = prune_secret(mix_secret(secret, secret * 64))
    secret = prune_secret(mix_secret(secret, secret // 32))
    secret = prune_secret(mix_secret(secret, secret * 2048))
    return secret


def mix_secret(secret: int, mix: int) -> int:
    return secret ^ mix


def prune_secret(secret: int) -> int:
    return secret & 16777215


def evolve_secret_repeat(secret: int, number_of_iterations: int) -> int:
    x = secret
    for _ in range(number_of_iterations):
        x = evolve_secret(x)
    return x


def evolved_secrets_sum(lines: list[str], number_of_iterations: int) -> int:
    total = 0
    for line in lines:
        total += evolve_secret_repeat(int(line), number_of_iterations)
    return total


def tests():
    assert prune_secret(100000000) == 16113920
    assert mix_secret(42, 15) == 37

    assert evolved_secrets_sum(read_lines("puzzle22_1_test_input1.txt"), 2000) == 37327623


def main():
    tests()

    t1 = evolved_secrets_sum(read_lines("puzzle22_1.txt"), 2000)
    assert t1 == 13764677935


if __name__ == "__main__":
    main()
