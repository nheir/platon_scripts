import types
from ple_parser import parse_syntax

import argparse

def clean(env):
    glob = {}
    exec("", glob)
    for k in glob:
        if k in env and glob[k] == env[k]:
            del env[k]

    exclude_types = [types.ModuleType, types.FunctionType]
    for k, v in list(env.items()):
        if v is None:
            del env[k]
            continue

        for t in exclude_types:
            if isinstance(v, t):
                del env[k]
                continue

def run(code, name, env):
    bytecode = compile(code, name, "exec")
    exec(bytecode, env)
    clean(env)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="PLaton Emulator",
        description="Emulate the execution of a PLaton exercice in PLaton"
    )
    parser.add_argument("exercice", help="exercice file")
    parser.add_argument(
        "-e", "--env",
        help="define an environment variable, use @file to use file content",
        metavar="var=foo",
        action="append",
        default=[]
    )
    parser.add_argument(
        "-i", "--input",
        help="define the input.code content from file",
        metavar="input_file"
    )

    args = parser.parse_args()

    env = {}
    for entry in args.env:
        if "=" in entry:
            k,v = entry.split('=', maxsplit=1)
            if v[0] == '@':
                with open(v[1:], 'r') as f:
                    v = f.read()
            env[k] = v
        else:
            env[entry] = ''

    with open(args.exercice, "r") as f:
        variables = parse_syntax(f.read())

    if args.input:
        with open(args.input, "r") as f:
            input = f.read()
    else:
        input = ''

    environment = variables
    environment.update(env)

    if 'builder' in variables:
        run(variables['builder'], 'builder', variables)

    print("Title: ", variables['title'])
    print("Statement: ", variables['statement'])
    print("Input: ", input)

    variables['input'] = { "code": input }

    keys = list(variables)

    variables['grade'] = -1
    variables['feedback'] = []
    run(variables['grader'], 'grader', variables)

    print("Grade: ", variables['grade'])
    for feedback in variables['feedback']:
        print("-", feedback['type'])
        for line in feedback['content'].splitlines():
            print(" ", line)

    print({k:v for k,v in variables.items() if k not in keys})
    print(variables.keys())
