#!/usr/bin/python
##This Python file uses the following encoding: utf-8
##
## (C) 2015 Muthiah Annamalai,
## Licensed under GPL Version 3
##
## class contains tools for mainpulating tamil source files

import sys
from .tamil import tamilInterpreter
from .tamil_scanner import tamilLex
from .tamil_serializer import SerializerXML
from .transform import make_mock_interpreter

def get_ast(filename):
    debug = False
    safe_mode = False
    lexer = tamilLex(filename, debug, encoding="UTF-8")
    parse_eval = tamilInterpreter(lexer=lexer, debug=debug, safe_mode=safe_mode)
    parse_tree = parse_eval.parse()
    return parse_tree,parse_eval


def serializeSourceFile(srcfilename, debug=False, tgtfile=None):
    parse_tree,_ = get_ast(filename=srcfilename)
    serializeParseTree(parse_tree, debug=False, filename=tgtfile)


def serializeParseTree(parsetree, debug=False, filename=None):
    interp = make_mock_interpreter(parsetree)
    SerializerXML(interp, debug, filename=filename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tamil_program_utils.py <srcfile1> <srcfile2> ...")
        sys.exit(255)
    for srcfile in sys.argv[1:]:
        print("processing =>",srcfile)
        serializeSourceFile(srcfile)
