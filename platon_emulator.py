import types
from ple_parser import parse_syntax

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

def run(code, env):
    exec(code, env)
    clean(env)

if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "r") as f:
        variables = parse_syntax(f.read())

    with open(sys.argv[2], "r") as f:
        input = f.read()

    environment = variables

    if 'builder' in variables:
        run(variables['builder'], variables)

    print("Title: ", variables['title'])
    print("Statement: ", variables['statement'])
    print("Input: ", input)

    variables['input'] = input

    keys = list(variables)

    variables['grade'] = -1
    variables['feedback'] = []
    run(variables['grader'], variables)

    print("Grade: ", variables['grade'])
    for feedback in variables['feedback']:
        print("-", feedback['type'])
        for line in feedback['content'].splitlines():
            print(" ", line)

    print({k:v for k,v in variables.items() if k not in keys})
    print(variables.keys())
