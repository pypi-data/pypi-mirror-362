# -*- coding: utf-8 -*-
# tests/utils.py


import os
from pathlib import Path

from jupyter_analysis_tools.utils import (
    appendToPATH,
    isWindows,
    makeNetworkdriveAbsolute,
    networkdriveMapping,
)

# output of 'net use' command on Windows
outNetUse = r"""Neue Verbindungen werden gespeichert.


Status       Lokal     Remote                    Netzwerk

-------------------------------------------------------------------------------
OK           G:        \\ALPHA\BETA              Microsoft Windows Network
OK           K:        \\GAM\MMA                 Microsoft Windows Network
OK           M:        \\user\drive\uname        Microsoft Windows Network
OK           T:        \\test\foldername         Microsoft Windows Network
OK                     \\psi\folder              Microsoft Windows Network
Der Befehl wurde erfolgreich ausgeführt.
"""


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
        assert (
            captured.out
            == """\
     /tmp/one [exists: False]
     /tmp/two [exists: False]
"""
        )
        assert os.environ["PATH"] == testpath + ":/tmp/one:/tmp/two"

    else:  # Windows edition
        appendToPATH(r"C:\Windows", ("one", "two"), verbose=True)
        captured = capsys.readouterr()
        assert (
            captured.out
            == """\
     C:\\Windows\\one [exists: False]
     C:\\Windows\\two [exists: False]
"""
        )
        assert os.environ["PATH"] == testpath + r";C:\Windows\one;C:\Windows\two"


def test_networkdriveMapping():
    if isWindows():
        map = networkdriveMapping(cmdOutput=outNetUse)
        assert map == {
            "G:": "\\\\ALPHA\\BETA",
            "K:": "\\\\GAM\\MMA",
            "M:": "\\\\user\\drive\\uname",
            "T:": "\\\\test\\foldername",
        }


def test_makeNetworkdriveAbsolute():
    if isWindows():
        filepath = Path(r"M:\some\folders\a file name.ext")
        newpath = makeNetworkdriveAbsolute(filepath, cmdOutput=outNetUse)
        assert filepath != newpath
        assert newpath == Path(r"\\user\drive\uname\some\folders\a file name.ext")
