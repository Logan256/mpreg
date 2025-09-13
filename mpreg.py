import argparse
import sys
import random
from typing import Generator

## Generators

# Incubators
def diversity() -> Generator[str, None, None]:
    variants = [
        '🫃🏻','🫃🏼','🫃🏽','🫃🏾','🫃🏿',
        '🫄🏻','🫄🏼','🫄🏽','🫄🏾','🫄🏿',
        '🤰🏽','🤰🏾','🤰🏿']
    while True:
        random.shuffle(variants)
        for variant in variants:
            yield variant

def vanilla() -> Generator[str, None, None]:
    while True:
        yield '🫃'

# Readers
def read_file(file_path: str) -> Generator[str, None, None]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for ch in file.read(4096):
                yield ch
    except FileNotFoundError:
        print("mpreg aborted [read error]: file not found", file=sys.stderr)
    except Exception as err:
        print("mpreg aborted [read error]: " + str(err), file=sys.stderr)

def read_std_in() -> Generator[str, None, None]:
    for ch in sys.stdin.read(4096):
        yield ch

## Writers
def write_file(file_path: str, input_gen: Generator[str, None, None]):
    try:
        with open(file_path, "wb") as file:
            for ch in input_gen:
                file.write(bytes(ch, encoding='utf-8'))
                file.flush()
    except Exception as err:
        print("mpreg aborted [write error]: " + str(err), file=sys.stderr)

def write_std_out(input_gen: Generator[str, None, None]):
    for ch in input_gen:
        sys.stdout.buffer.write(bytes(ch, encoding='utf-8'))
        sys.stdout.flush()


## Compositer
def mpregnate(input_gen: Generator[str, None, None], preg_gen: Generator[str, None, None]):
    for ch in input_gen:
        if ch != '—':
            yield ch
        else:
            yield next(preg_gen)

## Orchestration
def read_flags():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default="-")
    parser.add_argument("-o", "--output", default="-")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--diversity", action="store_true", help="use diverse emoji")
    group.add_argument("-v", "--vanilla", action="store_true", help="use single emoji")
    return parser.parse_args()

def main():
    args = read_flags()
    input_gen = read_std_in() if args.input == "-" else read_file(args.input)
    incubators = vanilla() if args.vanilla else diversity()
    if args.output != "-":
        write_file(args.output, mpregnate(input_gen, incubators))
    else:
        write_std_out(mpregnate(input_gen, incubators))


if __name__=="__main__":
    main()
