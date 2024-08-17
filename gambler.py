""" Fonctions utiles pour calculer m avec la méthode du gambler
"""

from scipy.stats import poisson
from itertools import product

from utils import dicothomie
from numpy import roots

from chsp import h

alpha = lambda a, b: a / b


def compute_m( a = 100, b = 100, epsilon=0.1, ratio=1/3, m_min=0, m_max=400):
	""" Calcule une valeur de M pour un epsilon donné
	Avec alpha le rapport entre la difficulté de l'honnête et de l'adversaire

	Alpha = bloc honnete / bloc adversaire
	Si alpha = 1, 1 bloc honnête = 1 blocs adversaire
	Si alpha = 4, 1 bloc honnête = 4 blocs adversaire
	Si alpha = 1/4, 1 bloc honnête = 1/4 blocs adversaire
	"""

	m, res = dicothomie(
		lambda m: proba_perte(m, a, b, ratio),
		m_min, m_max, epsilon
	)
	return m, res


def proba_perte(m, a, b, ratio):
	""" Calcule la probabilité qu'un attaquant réussisse à rattraper l'honnête
	pour un m donné

	P_\text{rattrape} = 
		1 - \sum_{k=0}^{m-1} (
			\frac{\lambda^k * e^{- \lambda}} {k!} * 
			(1 - P_\text{ruin}(k))
		)
	"""

	# On calcule le lambda
	lambda_ = compute_lambda(m, a, b, ratio)

	sum_term = 0
	for k in range(0, m*a):
		poisson_prob = poisson.pmf(k, lambda_)
		sum_term += poisson_prob * (1 - p_ruin(m*a - (b*k), a, b, ratio))
	P_rattrape = 1 - sum_term
	return P_rattrape


def compute_lambda(M, a, b, ratio):
	""" Lambda dans la formule du gamblers
	"""
	a_prob = A(alpha(a, b), ratio)
	b_prob = B(alpha(a, b), ratio)

	return round(a_prob * M / b_prob)
	

def p_ruin_simplifie(m, a, b, ratio):
	""" Probabilité de ruine pour un m donné
	/!\ Quand les racines sont distinctes !
	
	P_\text{ruin}(M) =
		\sum_{j=1}^{\nu} \eta^M_j (
			\prod_{i\neq j} \frac{1 - \eta_i}{\eta_j - \eta_i}
		)
	"""

	eta = compute_eta(a, b, ratio)
	
	nu = len(eta)

	# On calcule la probabilité de ruine
	sum_term = 0
	for j in range(0, nu):
		prod_term = 1
		for i in range(0, nu):
			if i != j:
				prod_term *= (1 - eta[i]) / (eta[j] - eta[i])
		sum_term += eta[j] ** m * prod_term
	return sum_term


def p_ruin(m, a, b, ratio):
	""" Probabilité de ruine pour un m donné

	P_{ruin}(M) = 
		\sum_{n=1}^{v}
			\Phi_{n,M-n+1}(\eta_1,...,\eta_n)
			\prod_{j=1}^{n-1}(1-\eta_j)
	"""

	etas = compute_eta(a, b, ratio)
	
	nu = len(etas)

	# On calcule la probabilité de ruine
	sum_term = 0
	for n in range(1, nu+1):
		prod_term = 1
		for j in range(1, n):
			prod_term *= (1 - etas[j])
		sum_term += phi(n, m-n+1, etas[:n]) * prod_term
	return sum_term


def phi_pur(n, r, z):
	""" Calcul de phi dans la ruine du joueur
	Mode bourrin -> on génère toutes les combinaisons possibles

	\Phi_{n,r}(z_1,...,z_n) =
		\sum_{i_j \geq 0, i_1+...+i_n = r}
			\prod_{j=1}^{n}z_j^{i_j}
	"""
	
	# On génère toutes les combinaisons possibles
	combinations = list(filter(lambda x: sum(x) == r, product(range(r+1), repeat=n)))
	res = 0
	for comb in combinations:
		prod = 1
		for j in range(0, n):
			prod *= z[j] ** comb[j]
		res += prod
	return res


def phi(n, r, z):
	""" Calcul de phi dans la ruine du joueur en utilisant la formule de Newton
	https://en.wikipedia.org/wiki/Complete_homogeneous_symmetric_polynomial
	https://en.wikipedia.org/wiki/Newton%27s_identities#A_variant_using_complete_homogeneous_symmetric_polynomials
	"""
	res = h(r, z)
	return res


def A(al, ratio):
	""" Probabilité de création d'un bloc adversarial
	"""
	q = ratio
	p = 1 - q
	return (q * al) / (p + q * al)
	

B = lambda al, ratio: 1 - A(al, ratio)


def compute_eta(a, b, ratio):
	""" On cherche les eta solutions du polynome
	B(\alpha)x^{k} + A(\alpha)x^{-l} = 1
	avec k la valeur d'un bloc honnête, et l la valeur d'un bloc adversarial
	"""
	honnete = a
	adversaire = b

	# La liste doit faire nu longueur
	nu = honnete + adversaire + 1 
	polynome = [0] * nu

	# L'honnête est sur le premier facteur
	polynome[0] = B(alpha(a, b), ratio)

	# L'adversaire est sur le dernier facteur
	polynome[-1] = A(alpha(a, b), ratio)

	# Le 1 est sur le facteur -adversaire
	polynome[-adversaire-1] = -1

	eta = roots(polynome)

	# solution in the unit disk |z| < 1 of the complex plane
	# On supprime les racines qui ne sont pas dans le disque unité
	eta = [e for e in eta if abs(e) < 0.9999999999]


	return eta
