from graphviz import Digraph


def make_graph_visualization(graph, f_name, methods_hash):
	dot = Digraph('Classes Graph')
	dot.attr('node', shape='box')
	for key in graph.keys():
		methods_str = '()\n'.join([methods_hash[x]['name'] for x in graph[key]['members'].split(' ')
							if x in methods_hash.keys()])
		dot.node(key, label=graph[key]['name'] + '\n_______\n' + methods_str + '()')
	for key in graph.keys():
		if graph[key]['childs'] == '': continue
		for child in graph[key]['childs'].split(' '):
			dot.edge(key, child)
	#print(dot.source)
	dot.render(f_name, None, True)
