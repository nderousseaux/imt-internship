import math
from decimal import Decimal

m = 100

res = 0

l = (1/3 * 1/4 * m) / (2/3)


for k in range(0, m-1 		+1):
	res += (
		(
			(l**k * math.exp(-l))/
			(math.factorial(k))
			
		) *
		(1 - (0.7) ** (m - k))
	)


print(1-res)