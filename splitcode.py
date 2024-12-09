
#*****************************************************************************
#  Copyright (C) 2023 Dominique Revuz < dominique dot revuz at univ-eiffel . fr>
#
#  Distributed under the terms of Creative Commons Attribution-ShareAlike 3.0
#  Creative Commons CC-by-SA 3.0
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  The full text of the CC-By-SA 3.0 is available at:
#
#            https://creativecommons.org/licenses/by-sa/3.0/
#            https://creativecommons.org/licenses/by-sa/3.0/fr/
#*****************************************************************************

# copyright dominique  Revuz 2023 

import re
import sys

ERROR="no"

LISTOFVARIABLES=['title', 'code_before', 'statement', 'soluce', 'code_after', 'checks_args_stdin', 'taboo']

debug = False
EXTENSION=".c"
VARSPLIT="// PL:"
START1="// PL:"
START2= "/* PL:"
END2="PL:== */"
END1="// PL:=="
STRIPSTR=""


def splitLine(line):
    line = line.strip()
    name,value = line[len(VARSPLIT):].split("=",1)
    name = name.strip()
    value = value.strip()

    return name,value


def splitcodefile(arg):
    with open(arg,"r") as f:
        return splitcodelist([line.strip() for line in f.readlines()])

def splitcodestring(s):
    return splitcodelist(s.split('\n'))

def splitcodelist(lines):
    
    state = None
    dict={"error":ERROR}

    if "EXTENSION" not in globals():
        dict['title']="Constantes non définies : EXTENSION etc pour le fichier splitcode"
        return dict

    
    for line in lines:
            if state == None:
                if line.startswith(VARSPLIT+"title="):
                    dict['title']= line[len(VARSPLIT+"title="):]
                    if debug : print(f"Title = <{dict['title']}>")
                elif line.startswith(START1) and not "==" in line:
                    name,value = splitLine(line)
                    dict[name]= value
                elif line.startswith(START2):
                    state= "info"
                    name =  line[6:].split("==")[0]
                    if debug : print(f"Starting info state :<{name}>")
                    multi="\n"
                elif line.startswith(START1):
                    state= "code"
                    name =  line[len(START1):].split("==")[0]
                    if debug : print(f"Starting code state :<{name}>")
                    multi="\n"
                continue
            elif state == "info":
                if line.startswith(END2):
                    dict[name]= multi
                    state=None
                    multi=""
                    if debug : print(f"Closing info state :<{name}>")
                else:
                    multi +=  line[len(STRIPSTR):] + "\n"
            else:     
                if line.startswith(END1):
                    if debug : print(f"Closing {state} state :<{name}>")
                    dict[name]= multi
                    state=None
                else:
                    multi +=  line + "\n"

    return(dict)




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: splitcode.py [--debug] [file ...] ")
        sys.exit(1)
    errors = ""
    for filename in sys.argv[1:]:
        if filename == "--debug":
            debug = True
            continue
        dico = splitcodefile(filename)
        for i in LISTOFVARIABLES:
            if not i in dico:
                errors += f" '{i}' variable not defined in {filename}\n"

        if errors:
            print(f"Error while reading the file {filename}\n"+ errors, file=sys.stderr)
            errors = "\n"

    if errors:
        sys.exit(1)
