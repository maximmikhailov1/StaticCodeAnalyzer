import os
import re
import argparse


def check_001(s):
    return len(s) > 79


def check_002(s):
    return (len(s) - len(s.lstrip(" "))) % 4


def check_003(s):
    parts_s = s.split('#')
    return parts_s[0].rstrip("\n").rstrip(" ").endswith(";")


def check_004(s):
    return re.match(r"[^#]*[^ ]( ?#)", s)


def check_005(s):
    # return re.match(r'.*#.*[Tt][oO][dD][oO].*', s)
    return re.search(r'(?i)# *todo', s)


def check_006(s):
    global empty_lines
    if s.rstrip('\n') == "":
        empty_lines += 1
    if s.rstrip('\n') != "" and empty_lines > 2:
        empty_lines = 0
        return True


def check_line(path, line, line_number):
    for error_num in error_checkers:
        if error_checkers[error_num](line):
            print(f'{path} Line {line_number}: {error_num} {code[error_num]}')


code = {'S001': "Too long",
        'S002': "Indentation is not a multiple of four",
        'S003': "Unnecessary semicolon",
        'S004': "At least two spaces required before inline comments",
        'S005': "TODO found",
        'S006': "More than two blank lines preceding a code line"}


error_checkers = {'S001': check_001, 'S002': check_002,
                  'S003': check_003, 'S004': check_004,
                  'S005': check_005, 'S006': check_006}

empty_lines = 0

parser = argparse.ArgumentParser()
parser.add_argument('path')

args = parser.parse_args()
try:
    if os.path.isdir(args.path):
        for path in sorted(os.listdir(args.path)):
            with open(path, 'r', encoding='utf-8') as file:
                code_line = file.readline()
                i = 1
                while code_line:
                    check_line(args.path, code_line, i)
                    code_line = file.readline()
                    i += 1
    else:
        with open(args.path, 'r', encoding='utf-8') as file:
            code_line = file.readline()
            i = 1
            while code_line:
                check_line(args.path, code_line, i)
                code_line = file.readline()
                i += 1

except FileNotFoundError:
    print("File not found.")
