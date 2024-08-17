import networkx as nx

class Playground():
	"""Calcule expérimentalement le nombre de chemins possible entre deux points
	du quart de plan positif.
	Tout en restant dans une zone définie par une condition.
	"""

	def __init__(self, depart, arrivee, condition=lambda x, y: True):
		self.depart = depart
		self.arrivee = arrivee
		self.condition = condition

		self.graph = nx.Graph()

		self.next_node_id = 0

		# On crée le noeud de départ
		start_node = self.start_node = self.create_node(self.arrivee)

		# On vérifie que le point de départ est dans la zone
		if not self.out_of_bounds(self.arrivee):
		
			# On crée le graphe
			self.compute_all_paths(start_node,self.arrivee)

	def compute_all_paths(self, previous_edge, arrivee):
		"""Calcule tous les chemins possibles entre depart et arrivee
		"""

		if (
			arrivee[0] > self.depart[0] and 
			not self.out_of_bounds((arrivee[0]-1, arrivee[1]))
		):
			ng = self.create_node((arrivee[0]-1, arrivee[1]))
			self.create_edge(previous_edge, ng)
			self.compute_all_paths(ng, (arrivee[0]-1, arrivee[1]))

		if (
			arrivee[1] > self.depart[1] and
			not self.out_of_bounds((arrivee[0], arrivee[1]-1))
		):
			ng = self.create_node((arrivee[0], arrivee[1]-1))
			self.create_edge(previous_edge, ng)
			self.compute_all_paths(ng, (arrivee[0], arrivee[1]-1))
	
	def out_of_bounds(self, point):
		if point[0] < self.depart[0] or point[1] < self.depart[1]:
			return True
		return not self.condition(point[0], point[1])

	def create_node(self, node):
		node_id = self.next_node_id
		self.next_node_id += 1
		self.graph.add_node(node_id, label=f"{node[0]},{node[1]}")
		return node_id
	
	def create_edge(self, n1, n2):
		self.graph.add_edge(n1, n2)

	def number_of_paths(self):
		# Si l'arrivee == depart
		if self.arrivee[0] == self.depart[0] and self.arrivee[1] == self.depart[1]:
			return 1

		# On compte le nombre de noeud qui n'ont qu'une seule arête
		d = dict(self.graph.degree)
		return len([k for k, v in d.items() if v == 1 and k != self.start_node])
