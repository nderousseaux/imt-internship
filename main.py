from decimal import Decimal, getcontext
from fractions import Fraction

from gambler import compute_m, alpha
from utils import plot, plot3d


getcontext().prec = 50
EPSILON = 10e-6

if __name__ == "__main__":

	resultats = []

	for couples in [
		(1,4),
		(1,3),
		(1,2),
		(1,1),
		(2,1),
		(3,1),
		(4,1)
	]:
		# for q in [1/10, 1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 4/10]:
		for q in [1/3]:
			a, b = couples
			res = compute_m(a, b, EPSILON, q)

			print((
				f"alpha = {Fraction(alpha(a,b)).limit_denominator(1000)},\t"
				f"q = {Fraction(q).limit_denominator(1000)},\t"
				f"m = {res[0]}"
			))

			resultats.append((
				alpha(a,b),
				q,
				res
			))

	# On ordonne les résultats en fonction de alpha
	resultats.sort(key=lambda x: x[0])

	plot(
		[x[0] for x in resultats], 
		[x[2][0] for x in resultats],
		"alpha",
		"m",
		"m en fonction de alpha, q = 1/3"
	)

	# plot3d(
	# 	[x[0] for x in resultats],
	# 	[x[1] for x in resultats],
	# 	[x[2][0] for x in resultats],
	# 	"alpha",
	# 	"q",
	# 	"m",
	# 	"m en fonction de alpha et q"
	# )

