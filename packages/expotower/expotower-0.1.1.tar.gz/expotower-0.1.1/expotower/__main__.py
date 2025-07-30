import argparse
from . import expotower, log10_estimate

def main():
    parser = argparse.ArgumentParser(
        description="Compute an exponential tower like 10 ^ (20 ^ (30 ^ ...))"
    )
    parser.add_argument("numbers", metavar="N", type=float, nargs="+",
                        help="List of numbers to build the exponential tower")
    parser.add_argument("--log10", action="store_true",
                        help="Print log10 estimate instead of full result")
    args = parser.parse_args()

    if args.log10:
        print(log10_estimate(*args.numbers))
    else:
        print(expotower(*args.numbers))

if __name__ == "__main__":
    main()
