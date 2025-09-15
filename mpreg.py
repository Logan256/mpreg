"""
mpreg: Em-dash Pregnancy Replacement Utility

A high-performance streaming text processor for replacing em dashes (—) 
with pregnancy-related emoji variants. Designed for memory-efficient 
processing of arbitrarily large inputs.
"""

from argparse import Namespace, ArgumentParser
from random import shuffle
from typing import Generator
import sys
import os

FLUSH_RESET_MASK = 0xFF

## Generators

# Incubators
def diversity() -> Generator[str, None, None]:
    variants = [
        "🫃🏻","🫃🏼","🫃🏽","🫃🏾","🫃🏿",
        "🫄🏻","🫄🏼","🫄🏽","🫄🏾","🫄🏿",
        "🤰🏽","🤰🏾","🤰🏿"]
    while True:
        shuffle(variants)
        for variant in variants:
            yield variant

def vanilla() -> Generator[str, None, None]:
    while True:
        yield "🫃"

# Readers
def read_file(file_path: str, chunk_size: int) -> Generator[str, None, None]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            while chunk := file.read(chunk_size):
                for char in chunk:
                    yield char
    except FileNotFoundError:
        print("mpreg aborted [read error]: file not found", file=sys.stderr)
        sys.exit(2)
    except (PermissionError, OSError) as err:
        print(f"mpreg aborted [access denied]: {err}", file=sys.stderr)
        sys.exit(3)
    except UnicodeDecodeError as err:
        print(f"mpreg aborted [encoding error]: {err}", file=sys.stderr) 
        sys.exit(4)
    except Exception as err:
        print(f"mpreg aborted [read error]: {err}", file=sys.stderr)
        sys.exit(1)

def read_std_in(chunk_size: int) -> Generator[str, None, None]:
    while chunk := sys.stdin.read(chunk_size):
        for char in chunk:
            yield char

## Writers
def write_file(file_path: str, input_gen: Generator[bytearray, None, None]) -> None:
    try:
        with open(file_path, "wb") as file:
            for i, bz in enumerate(input_gen):
                file.write(bz)
                if i & FLUSH_RESET_MASK == 0:
                    file.flush()
            file.flush()
    except Exception as err:
        print(f"mpreg aborted [write error]: {err}", file=sys.stderr)
        sys.exit(1)

def write_std_out(input_gen: Generator[bytearray, None, None]) -> None:
    try:
        for i, bz in enumerate(input_gen):
            sys.stdout.buffer.write(bz)
            if i & FLUSH_RESET_MASK == 0:
                sys.stdout.buffer.flush()
        sys.stdout.buffer.flush()
    except Exception as err:
        print(f"mpreg aborted [write error]: {err}", file=sys.stderr)
        sys.exit(1)


## Compositor
def mpregnate(input_gen: Generator[str, None, None], preg_gen: Generator[str, None, None]) -> Generator[str, None, None]:
    for ch in input_gen:
        if ch == "\u2014":
            yield next(preg_gen)
        elif ch == "\u2E3A":
            yield next(preg_gen)
        elif ch == "\u2E3B":
            yield next(preg_gen)
        else:
            yield ch

## Orchestration
def read_flags() -> Namespace:
    parser = ArgumentParser(
        prog="mpreg",
        description="Replace em dashes with pregnancy emoji in large text streams"
    )
    parser.add_argument("-i", "--input", default="-", 
                       metavar="FILE", help="input file (default: stdin)")
    parser.add_argument("-o", "--output", default="-",
                       metavar="FILE", help="output file (default: stdout)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--diversity", action="store_true", 
                      help="use diverse emoji variants")
    group.add_argument("-v", "--vanilla", action="store_true", 
                      help="use single emoji variant")
    return parser.parse_args()

def buffer(char_gen: Generator[str, None, None], chunk_size: int) -> Generator[bytearray, None, None]:
    buf = bytearray()
    for char in char_gen:
        buf.extend(char.encode("utf-8"))
        if len(buf) >= chunk_size:
            yield buf
            buf = bytearray()
    if buf:
        yield buf

def get_optimal_chunk_size() -> int:
    try:
        page_size = os.sysconf('SC_PAGE_SIZE')
        return max(page_size * 4, 4096)
    except (AttributeError, OSError):
        return 4096

def main() -> None:
    chunk_size = get_optimal_chunk_size()
    args = read_flags()
    input_gen = read_std_in(chunk_size) if args.input == "-" else read_file(args.input, chunk_size)
    incubators = vanilla() if args.vanilla else diversity()
    if args.output != "-":
        write_file(args.output, buffer(mpregnate(input_gen, incubators), chunk_size))
    else:
        write_std_out(buffer(mpregnate(input_gen, incubators), chunk_size))

if __name__=="__main__":
    main()
