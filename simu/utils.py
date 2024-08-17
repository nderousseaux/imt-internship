from math import factorial
from decimal import Decimal

""" Quelques fonctions utiles pour le projet
"""

def binom(x, y):
	if y > x:
		return Decimal(0)
	
	x = int(x)
	y = int(y)
	return Decimal(
		factorial(x) //
		(factorial(y) * factorial(x - y))
	)
