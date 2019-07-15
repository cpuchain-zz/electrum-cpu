from pythonforandroid.recipe import CythonRecipe
from pythonforandroid.toolchain import current_directory
import shutil
import glob

class CPUpowerRecipe(CythonRecipe):

    url = 'https://github.com/cpuchain/cpupower_python/archive/master.zip'

    patches = ['./setup.patch']
    depends = ['setuptools']

recipe = CPUpowerRecipe()
