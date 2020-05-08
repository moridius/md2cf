#!/usr/bin/env python3

import argparse
import re
import sys


def convert(markdown):
    output = []
    for line in markdown:
        if line.startswith("# "):
            output.append("h1. " + line[2:].rstrip())
            continue

        if line.startswith("## "):
            output.append("h2. " + line[3:].rstrip())
            continue

        if line.startswith("### "):
            output.append("h3. " + line[4:].rstrip())
            continue

        if line.startswith("#### "):
            output.append("h4. " + line[4:].rstrip())
            continue

        if line.startswith("##### "):
            output.append("h5. " + line[4:].rstrip())
            continue

        m = re.fullmatch(r"==+\n", line)
        if m:
            output = output[:-1] + ["h1. " + output[-1]]
            continue

        m = re.fullmatch(r"--+\n", line)
        if m:
            output = output[:-1] + ["h2. " + output[-1]]
            continue

        m = re.fullmatch(r"( *)[-*] (.*)\n", line)
        if m:
            spaces = len(m.group(1))
            level = int(spaces / 4) + 1
            output.append("*" * level + " " + m.group(2))
            continue

        m = re.fullmatch(r"( *)[0-9]+[\.\)] (.*)\n", line)
        if m:
            spaces = len(m.group(1))
            level = int(spaces / 4) + 1
            output.append("#" * level + " " + m.group(2))
            continue

        line = re.sub(r"[_*]{2}(.+?)[_*]{2}", r"{b}\1{b}", line)
        line = re.sub(r"[_*]{1}(.+?)[_*]{1}", r"{i}\1{i}", line)
        line = re.sub(r"\{b\}(.+?)\{b\}", r"*\1*", line)
        line = re.sub(r"\{i\}(.+?)\{i\}", r"_\1_", line)
        line = re.sub(r"\[(.+)\]\((.+)\)", r"[\1|\2]", line)

        output.append(line.rstrip())
    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("input_file", nargs="?", help="")
    args = parser.parse_args()

    if args.input_file:
        with open(args.input_file, "r") as f:
            print(convert(f))
    else:
        print(convert(sys.stdin))
