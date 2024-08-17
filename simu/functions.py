from math import floor
from decimal import Decimal
from utils import binom



def nb_chemins_x_y(a, b):
	""" Retourne le nombre de chemins possibles pour aller de a à b
	"""
	return binom(
		(b[0] - a[0]) + (b[1] - a[1]),
		b[1] - a[1]
	)

def nb_chemins_x_y_quart(a, b):
	""" Calcule le nombre de chemins pour aller de a à b
	tout en restant sous la droite de coefficient directeur 1/4
	"""
	m = a[0]
	beta = b[1]
	alpha = a[1]

	# {M + \beta - \alpha \choose M} \\
	# &\quad - \sum_{i = \lfloor \frac{M}{4} \rfloor + 1}^\beta {5i - M - \alpha - 1 \choose i - \alpha} \\
	# &\qquad \times \frac{2M - 4\beta + 1}{2M + \beta - 5i + 1} \\
	# &\qquad \times {2M + \beta - 5i + 1 \choose \beta - i}

	a = binom(m + beta - alpha, m)
	b = Decimal('0')
	for i in range(floor(m / 4) + 1, beta + 1):
		b += (
			binom(5 * i - m - alpha - 1, i - alpha) *
			((Decimal('2') * m - Decimal('4') * beta + Decimal('1')) / (Decimal('2') * m + beta - Decimal('5') * i + Decimal('1'))) *
			binom(2 * m + beta - Decimal('5') * i + Decimal('1'), beta - i)
		)

	return a - b

def nb_chemins_x_y_1(a, b):
	""" Calcule le nombre de chemins pour aller de a à b
	tout en restant sous la droite de coefficient directeur 1
	"""
	m = a[0]
	m2 = b[0]
	beta = b[1]
	alpha = a[1]

	return binom(m + beta - alpha, m) - binom(m + beta - alpha, m2 - alpha + Decimal('1'))


def proba_point(a, b, alpha, ratio):
	""" Retourne la probabilité d'attendre un point en b en partant de a
	"""

	return (
		nb_chemins_x_y(a, b) *
		(
			(mu(alpha, ratio) ** (b[0] - a[0])) *
			((Decimal('1') - mu(alpha, ratio)) ** (b[1] - a[1]))
		)
	)

def proba_point_condition(a, b, alpha, ratio):
	""" Retourne la probabilité d'attendre un point en b en partant de a
		sans passer strictement au dessus de la droite.
	"""

	if alpha == Decimal('0.25'):
		return proba_point_condition_quart(a, b, ratio)
	elif alpha == Decimal('1'):
		return proba_point_condition_1(a, b, ratio)
	elif alpha == Decimal('4'):
		return proba_point_condition_4(a, b, ratio)
	else:
		raise ValueError("Alpha non géré")

def proba_point_condition_quart(a, b, ratio):
	""" Retourne la probabilité d'attendre un point en b en partant de a
	tout en restant sous la droite de coefficient directeur 1/4
	"""
	m = a[0]
	alpha = a[1]
	beta = b[1]

	return mu(Decimal('1'), ratio) ** (beta - alpha) * (Decimal('1') - mu(Decimal('1'), ratio)) ** (m) * nb_chemins_x_y_quart(a, b)

def proba_point_condition_1(a, b, ratio):
	""" Retourne la probabilité d'attendre un point en b en partant de a
	tout en restant sous la droite de coefficient directeur 1
	"""
	m = a[0]
	beta = b[1]
	alpha = a[1]

	return mu(Decimal('1'), ratio) ** (beta - alpha) * (Decimal('1') - mu(Decimal('1'), ratio)) ** (m) * nb_chemins_x_y_1(a, b)

def proba_point_condition_4(a, b, ratio):
	""" Retourne la probabilité d'attendre un point en b en partant de a
	tout en restant sous la droite de coefficient directeur 4
	"""
	raise ValueError("Non implémenté")
	return Decimal('0')
