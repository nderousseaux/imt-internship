from math import factorial

from decimal import Decimal
from functions import proba_point, proba_point_condition
from gamblers import p_ruin, lambda_

""" Fonctions utiles pour calculer m.
"""
		


def test_m_droite(m, alpha, ratio):
	""" Calcule la probabilité de succès pour un m donné
	\sum_{i=0}^{\lceil\alpha*M\rceil}
		F(M;i)
		\sum_{h = M}^{2m}
			\sum_{m = 0}^{\lceil\alpha*h\rceil}
				G((M;i),(h;m))

	- Avec alpha le coéfficient directeur de la droite
	- Avec F la probabilité d'attendre un point partant de 0,0
	- Avec G la probabilité d'attendre un point sans passer strictement
		au dessus de la droite.
	"""
	res = Decimal('0')

	for i in range(0, int(alpha*m) + 1):
		a = proba_point((Decimal('0'), Decimal('0')), (m, i), alpha, ratio)
		b = Decimal('0')

		for mal in range(0, int(alpha*2*m) + 1):
			b += proba_point_condition((m, i), (2*m, mal), alpha, ratio)

		res += a * b

	return res
