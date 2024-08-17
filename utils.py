""" Fonctions génériques 
"""
from decimal import Decimal
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def dicothomie(f, min, max, valeur):
	""" Calcule la valeur de x pour laquelle f(x) = valeur
	f est une fonction continue et croissante.
	"""
	x = (min + max) // 2
	while max - min > 1:
		if f(x) < valeur:
			max = x
		else:
			min = x

		# print(f"min = {min}, max = {max}")
		x = (min + max) // 2
	return x, f(x)


def plot(x, y, x_name, y_name, title):
	""" Plot the results
	"""

	plt.plot(x, y, "b:o")
	plt.xlabel(x_name)
	plt.ylabel(y_name)
	plt.title(title)
	plt.show()


def plot3d(x, y, z, x_name, y_name, z_name, title):
	""" Plot the results as a surface plot
	"""

	fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

	# Make data.
	X = np.unique(np.array(y))
	Y = np.unique(np.array(x))
	X, Y = np.meshgrid(X, Y)
	# Z, tableau en 2D, de taille (x, y)
	Z = np.array(z).reshape(X.shape)

	# Plot the surface.
	surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
												linewidth=0, antialiased=False)

	plt.xlabel(y_name)
	plt.ylabel(x_name)
	ax.set_zlabel(z_name)
	plt.title(title)

	plt.show()