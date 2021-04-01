"""main entry for ekea command-line interface"""


def main():
    from ekea import E3smKea
    ret, _ = E3smKea().run_command()
    return ret


if __name__ == "__main__":
    main()
