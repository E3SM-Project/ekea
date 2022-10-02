"""main entry for ekea command-line interface"""


def main():
    from ekea import EKEA
    ret, _ = EKEA().run_command()
    return ret


if __name__ == "__main__":
    main()
