"""Test that the interface is working."""
import os
from ycv import build_materials

def test_interface():
    os.chdir("examples")
    os.system("ls ")
    build_materials("fancyJob", {"cv": "cv.yaml"})
