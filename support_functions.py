def get_classes_names_list(untangle_obj):
	return [str(Class['name']) for Class in untangle_obj.Class]


def get_classes_id_list(untangle_obj):
	return [str(Class['id']) for Class in untangle_obj.Class]


def get_classes_members_list(untangle_obj):
	return [str(Class['members']) for Class in untangle_obj.Class]


def get_classes_roots_list(untangle_obj):
	return [str(Class['id']) for Class in untangle_obj.Class if Class['bases'] == '']


def get_classes_childs_hash(untangle_obj):
	def get_class_childs(class_id):
		return ' '.join([str(Class['id']) for Class in untangle_obj.Class if class_id in Class['bases'].split(' ')])

	childs = {}
	for Class in untangle_obj.Class:
		childs[str(Class['id'])] = get_class_childs(Class['id'])
	return childs


def get_classes_graph(untangle_obj):
	def form_class_hash(untangle_class):
		def get_class_childs(class_id):
			return ' '.join([str(Class['id']) for Class in untangle_obj.Class if class_id in Class['bases'].split(' ')])

		class_hash = {}
		class_hash['file'] = str(untangle_class['file'])
		class_hash['childs'] = get_class_childs(untangle_class['id'])
		class_hash['bases'] = str(untangle_class['bases'])
		class_hash['members'] = str(untangle_class['members'])
		class_hash['abstract'] = str(untangle_class['abstract'])
		class_hash['name'] = str(untangle_class['name'])
		return class_hash

	graph = {}
	for Class in untangle_obj.Class:
		graph[str(Class['id'])] = form_class_hash(Class)
	return graph


def get_classes_leafs(graph, untangle_obj):
	return [str(Class['id']) for Class in untangle_obj.Class if graph[str(Class['id'])]['childs'] == '']


def add_inherited_methods_to_classes(graph, untangle_obj):
	def add_inherited_methods_to_class(base_id, child_id, untangle_obj):
		def get_inherited_methods(base_id, child_id, untangle_obj):
			def get_method_name_by_id(method_id):
				for Method in untangle_obj.Method:
					if Method['id'] == method_id: return Method['name']

			def get_method_id_by_name(method_name):
				for Method in untangle_obj.Method:
					if Method['name'] == method_name: return Method['id']

			methods_list = [str(Method['id']) for Method in untangle_obj.Method]
			bases_members = [get_method_name_by_id(x) for x in graph[base_id]['members'].split(' ') if
							 x in methods_list]
			childs_members = [get_method_name_by_id(x) for x in graph[child_id]['members'].split(' ') if
							  x in methods_list]
			return ' '.join([get_method_id_by_name(x) for x in bases_members if x not in childs_members])

		graph[child_id]['members'] += get_inherited_methods(base_id, child_id, untangle_obj) + ' '

	to_view = get_classes_roots_list(untangle_obj)
	while to_view:
		base_class = to_view.pop(0)
		childs = graph[base_class]['childs'].split(' ')
		if childs == ['']: continue
		to_view += childs
		for child in childs:
			add_inherited_methods_to_class(base_class, child, untangle_obj)


def restructuring_classes_graph(graph, untangle_obj):
	def number_of_inherited_methods(base_id, child_id):
		base_members = graph[base_id]['members'].split(' ')
		child_members = graph[child_id]['members'].split(' ')
		return sum(1 for method in child_members if method in base_members)

	def get_key_with_max_val(d):
		v = list(d.values())
		k = list(d.keys())
		return k[v.index(max(v))]

	to_view = get_classes_leafs(graph, untangle_obj)
	while to_view:
		child_class = to_view.pop(0)
		if graph[child_class]['bases'] == '': continue
		bases = [x for x in graph[child_class]['bases'].split(' ') if x != '']
		to_view += bases
		bases_hash = {}
		for base in bases:
			bases_hash[base] = number_of_inherited_methods(base, child_class)
		chosen_base = get_key_with_max_val(bases_hash)
		base_members = graph[chosen_base]['members'].split(' ')
		child_members = graph[child_class]['members'].split(' ')
		graph[child_class]['members'] = ' '.join(x for x in child_members if x not in base_members)
		graph[child_class]['bases'] = chosen_base


def generate_java_file(f_name, graph, untangle_obj):
	def write_class_to_file(class_id):
		def get_method_name_by_id(method_id):
			return [str(Method['name']) for Method in untangle_obj.Method if Method['id'] == method_id][0]

		base_id = graph[class_id]['bases']
		if base_id == '':
			f.write('class ' + graph[class_id]['name'] + '\n{\n\n')
		else:
			f.write('class ' + graph[class_id]['name'] + ' extends ' + graph[base_id]['name'] + '\n{\n\n')
		for method in [x for x in graph[class_id]['members'].split(' ') if x in method_list]:
			f.write('void ' + get_method_name_by_id(method) + '() {}\n\n')
		f.write('}\n')

	f = open(f_name + '.java', 'w')
	method_list = [str(Method['id']) for Method in untangle_obj.Method]
	f.write('package ' + f_name)
	f.write('\n')
	f.write('class ' + f_name + '\n{\n')
	for key in graph.keys(): write_class_to_file(key)
	f.write('}\n')
