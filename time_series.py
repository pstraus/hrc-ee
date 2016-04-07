#! /bin/python
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import random

def test_function():
	db_name = ''
	search_term = ''
	column = ''
#	x = range(100)
#	y = [a * 2 + random.randint(-20,20) for a in x]
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
	return mpld3.fig_to_html(fig)
#	mpld3.show()
	#graph_out = def_tseries(db_name, search_term, column)
	

def tseries(db_name, search_term, column):
	pass
if __name__ == "__main__":
	test_function()
