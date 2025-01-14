# -*- coding: utf-8 -*-

import os
import sys

import numpy as np

import subprocess
import pytest


@pytest.mark.light
def test_clutrr_cli_v1():
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'

    cmd = [
        sys.executable,
        './bin/clutrr-cli.py',
        '--train', 'data/clutrr-emnlp/data_d83ecc3e/1.3_test.csv',
        '-s', 'concat',
        '-V', '128',
        '-b', '8',
        '-d', '2',
        '--test-max-depth', '2',
        '--hops', '2', '2',
        '-e', '1',
        '-m', '3',
        '-t', 'min',
        '-k', '20',
        '-i', '1.0',
        '-r', 'linear',
        '-R', '0',
        '--debug'
    ]

    p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out_str = out.decode("utf-8")
    err_str = err.decode("utf-8")
    assert p.returncode == 0, f"Process exited with {p.returncode} code\nOutput: {out_str}\nError: {err_str}"

    sys.stdout = sys.stderr

    lines = out_str.split("\n")

    sanity_check_flag_1 = False

    for line in lines:
        if 'Batch 1/13' in line:
            value = float(line.split()[5])
            np.testing.assert_allclose(value, 0.3143, atol=1e-3, rtol=1e-3)
        if 'Batch 2/13' in line:
            value = float(line.split()[5])
            np.testing.assert_allclose(value, 0.3090, atol=1e-3, rtol=1e-3)
        if 'Batch 3/13' in line:
            value = float(line.split()[5])
            np.testing.assert_allclose(value, 0.2931, atol=1e-3, rtol=1e-3)
        if 'Batch 4/13' in line:
            value = float(line.split()[5])
            np.testing.assert_allclose(value, 0.2587, atol=1e-3, rtol=1e-3)

            sanity_check_flag_1 = True

    assert sanity_check_flag_1, f"Process had wrong output.\nOutput: {out_str}\nError: {err_str}"


if __name__ == '__main__':
    pytest.main([__file__])
