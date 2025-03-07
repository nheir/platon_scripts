def parse_syntax(input_text):
    data = {}
    lines = input_text.strip().split('\n')
    key = None
    multiline_key = None
    multiline_value = []

    includes = []

    for line in lines:
        if multiline_key:
            # Inside a multiline block
            if line == '==':
                # End of multiline block
                data[multiline_key] = '\n'.join(multiline_value)
                multiline_key = None
                multiline_value = []
            else:
                # Add line to multiline value
                multiline_value.append(line)
        else:
            # Ignore comments
            if line.startswith('//') or line.startswith('#'):
                pass
            elif line.startswith("@extends"):
                file = line.split(' ', 1)[1].strip()
                with open(file, "r") as f:
                    ret, incs = parse_syntax(f.read())
                data.update(ret)
                includes.extend(incs)
            elif line.startswith("@include"):
                file = line.split(' ', 1)[1].strip()
                includes.append(file)
            # Single-line or start of multiline block
            elif '==' in line:
                # Start of multiline block
                multiline_key = line.split('==')[0].strip()
            elif '=' in line:
                # Single-line key-value pair
                key, value = map(str.strip, line.split('=', 1))
                if value.startswith("@extends"):
                    file = value.split(' ', 1)[1].strip()
                    with open(file, "r") as f:
                        ret,incs = parse_syntax(f.read())
                    data[key] = ret
                    includes.extend(incs)
                elif value.startswith("@copycontent"):
                    file = value.split(' ', 1)[1].strip()
                    with open(file, "r") as f:
                        ret = f.read()
                    data[key] = ret
                else:
                    data[key] = eval(value)

    return data,includes

if __name__ == "__main__":
    import sys
    with open(sys.argv[1], "r") as f:
        ret = parse_syntax(f.read())

    print(ret)
