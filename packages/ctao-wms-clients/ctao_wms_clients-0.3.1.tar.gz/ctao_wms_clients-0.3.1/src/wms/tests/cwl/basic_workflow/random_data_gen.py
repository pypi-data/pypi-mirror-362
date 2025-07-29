import argparse
import random


def generate_random_data(file_path: str = "data.txt", num_lines: int = 100):
    with open(file_path, "w") as f:
        mu = random.randint(1, 10)
        sig = random.randint(1, 5)
        for _ in range(num_lines):
            rd = random.gauss(mu, sig)
            f.write(f"{rd}\n")
    print(f"data file: {file_path}, mean: {mu}, std dev: {sig}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random data")
    parser.add_argument("--file-path", default="data.txt", help="Output file path")
    parser.add_argument(
        "--num_lines", type=int, default=100, help="Number of lines to generate"
    )
    args = parser.parse_args()
    generate_random_data(args.file_path, args.num_lines)
