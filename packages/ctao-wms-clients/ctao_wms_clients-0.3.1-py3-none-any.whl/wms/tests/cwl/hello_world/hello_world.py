from pathlib import Path


def hello_world(file="output.txt"):
    Path(file).write_text("Hello!")


if __name__ == "__main__":
    hello_world("./output.txt")
