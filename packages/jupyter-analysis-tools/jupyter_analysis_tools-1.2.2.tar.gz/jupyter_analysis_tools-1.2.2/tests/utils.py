# -*- coding: utf-8 -*-
# tests/utils.py


import os

from jupyter_analysis_tools.utils import appendToPATH, isWindows


def test_appendToPATH(capsys):
    # Setting up a PATH for testing first (platform dependent).
    testpath = "/usr/local/sbin:/usr/local/bin:/sbin:/usr/games:/usr/local/games:/snap/bin"
    if isWindows():
        testpath = "something else"
    os.environ["PATH"] = testpath
    assert os.environ["PATH"] == testpath

    if not isWindows():  # Linux edition
        appendToPATH("/tmp", ("one", "two"), verbose=True)
        captured = capsys.readouterr()
        assert captured.out == """\
     /tmp/one [exists: False]
     /tmp/two [exists: False]
"""
        assert os.environ["PATH"] == testpath+":/tmp/one:/tmp/two"

    else:  # Windows edition
        appendToPATH(r"C:\Windows", ("one", "two"), verbose=True)
        captured = capsys.readouterr()
        assert captured.out == """\
     C:\\Windows\\one [exists: False]
     C:\\Windows\\two [exists: False]
"""
        assert os.environ["PATH"] == testpath+r";C:\Windows\one;C:\Windows\two"
