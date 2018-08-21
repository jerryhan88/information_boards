import os.path as opath
import os

from functools import reduce

DATA_HOME = reduce(opath.join, [opath.expanduser("~"), '_data'])