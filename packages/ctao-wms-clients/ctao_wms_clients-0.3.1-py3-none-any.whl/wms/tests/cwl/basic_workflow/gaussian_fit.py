import argparse


def gaussian_fit(input_data: str):
    """Dummy gaussian fit."""
    with open(input_data) as f:
        data = f.readlines()
        mu = sum(map(float, data)) / len(data)
        sigma = sum([(float(x) - mu) ** 2 for x in data]) / len(data)
        print(f"Mean: {mu}, Std dev: {sigma}")
        return mu, sigma


def main(input_data_files: list[str], output_data: str):
    for input_data in input_data_files:
        mu, sigma = gaussian_fit(input_data)
        with open(output_data, "a") as f:
            f.write(f"{input_data}: Mean: {mu}, Std dev: {sigma}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gaussian fit script")
    parser.add_argument("input_data_files", nargs="+", help="Input data files")
    parser.add_argument("--output", "-o", default="fit.txt", help="Output file")
    args = parser.parse_args()
    main(args.input_data_files, args.output)
