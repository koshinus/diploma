from graphviz import Digraph


def make_graph_vis(graph, f_name):
	dot = Digraph('Classes Graph')
	dot.attr('node', shape='Box')
	for key in graph.keys():
		dot.node(key, graph[key]['name'])
	for key in graph.keys():
		for child in graph[key]['childs'].split(' '):
			dot.edge(key, child)
	print(dot.source)
	dot.render(f_name, None, True)
