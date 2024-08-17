""" Calcul du complete homogenious symmetric polynomial
The complete homogeneous symmetric polynomial of degree k in n variables X1,
..., Xn, written hk for k = 0, 1, 2, ..., is the sum of all monomials of total
degree k in the variables.


Dans le papier -> PHI_{n,r}(z_1,...,z_n) = \sum_{i_j \geq 0, i_1+...+i_n = r} 
	\prod_{j=1}^{n}z_j^{i_j}

Sur wikipedia -> h_k(x_1, x_2, ..., x_n)
https://en.wikipedia.org/wiki/Complete_homogeneous_symmetric_polynomial
"""

# Cache pour les valeurs de h
# {
# 	(k, X): h
# }
h_cache = {}

# Cache pour les valeurs de p
# {
# 	(k, X): p
# }
p_cache = {}

def h(k, X):
	""" Calcul du complete homogenious symmetric polynomial

	kh_k = \sum_{i = 1}^{k}h_{k-i}p_i
	"""
	# Si c'est dans le cache, on retourne la valeur
	if (k, tuple(X)) in h_cache:
		return h_cache[(k, tuple(X))]
	
	# Sinon, on la calcule
	if k == 0: # h_0 = 1
		res = 1
	else:
		res = 0
		for i in range(1, k+1):
			res += h(k-i, X) * p(i, X)
		res /= k


	h_cache[(k, tuple(X))] = res

	return res
	

def p(k, X):
	""" Newton's identities
	https://en.wikipedia.org/wiki/Newton%27s_identities#A_variant_using_complete_homogeneous_symmetric_polynomials
	"""

	# Si c'est dans le cache, on retourne la valeur
	if (k, tuple(X)) in p_cache:
		return p_cache[(k, tuple(X))]

	n = len(X)

	res = 0
	for i in range(1, n+1):
		res += X[i-1] ** k

	p_cache[(k, tuple(X))] = res

	return res

	