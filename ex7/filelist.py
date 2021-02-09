#!/usr/bin/env python3

from autotest import filelist_test,res_code
from sys import argv

required = ["README",
            "ex3.py",
            ]

try:
    if not filelist_test(argv[1], required, format='zip'):
        exit(-1)
except:
    res_code("zipfile",output="Testing zip file failed...")
    exit(-1)
