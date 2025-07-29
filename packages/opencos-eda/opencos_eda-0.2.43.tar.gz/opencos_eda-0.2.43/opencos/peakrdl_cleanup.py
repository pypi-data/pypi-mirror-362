#!/usr/bin/env python3

import sys
import os

def run(file_in, file_out):
    with open(file_in) as f:
        lines = f.readlines()

    with open(file_out, 'w') as f:
        f.write('// verilator lint_off MULTIDRIVEN\n')
        for line in lines:
            f.write(line)
        f.write('// verilator lint_on  MULTIDRIVEN\n')

if __name__ == '__main__':
    assert len(sys.argv) == 3, f'{sys.argv=}'
    file_in = sys.argv[1]
    file_out = sys.argv[2]
    run(file_in, file_out)
