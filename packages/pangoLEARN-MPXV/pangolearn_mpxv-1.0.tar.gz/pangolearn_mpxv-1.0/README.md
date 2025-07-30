# pangoLEARN-MPXV

from importlib.resources import files
data_text = files('mypkg.data').joinpath('data1.txt').read_text()