def get_classes_id_list(untangle_obj):
	return [str(Class['id']) for Class in untangle_obj.Class]


# --------------------------------------------------------------------
def get_classes_graph(untangle_obj):
	def form_class_hash(untangle_class):
		def get_class_childs(class_id):
			return ' '.join([str(Class['id']) for Class in untangle_obj.Class if class_id in Class['bases'].split(' ')])

		# <Class id="_152" name="b" context="_1" mangled="1b" demangled="b" location="f1:10"
		# file="f1" line="10" artificial="1" size="64" align="64"
		# members="_198 _199 _200 _201 _202 _203 " bases="_130 ">
		# <Base type="_130" access="public" virtual="0" offset="0"/>
		# </Class>
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


# --------------------------------------------------------------------
def get_methods_hash(untangle_obj):
	def get_method_hash(untangle_method):
		method_hash = {}
		# <Method id="_202" name="a_show" returns="_160" virtual="1" overrides="_188 " context="_152"
		# access="public" mangled="_ZN1b6a_showEv" demangled="b::a_show()" location="f1:12" file="f1"
		# line="12" endline="12" inline="1"/>
		method_hash['name'] = str(untangle_method['name'])
		method_hash['returns'] = str(untangle_method['returns'])
		method_hash['virtual'] = str(untangle_method['virtual'])
		method_hash['overrides'] = str(untangle_method['overrides'])
		method_hash['access'] = str(untangle_method['access'])
		method_hash['file'] = str(untangle_method['file'])
		method_hash['line'] = str(untangle_method['line'])
		method_hash['endline'] = str(untangle_method['endline'])
		if untangle_method['pure_virtual'] == '1':
			method_hash['method_size'] = 1
		else:
			method_hash['method_size'] = 1 + \
				int(str(untangle_method['endline'])) - int(str(untangle_method['line']))
		method_hash['inline'] = str(untangle_method['inline'])
		return method_hash

	methods_hash = {}
	for Method in untangle_obj.Method:
		methods_hash[str(Method['id'])] = get_method_hash(Method)
	return methods_hash


# --------------------------------------------------------------------
def add_inherited_methods_to_classes(graph, untangle_obj):
	def add_inherited_methods_to_class(base_id, child_id):
		def get_inherited_methods():
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

		graph[child_id]['members'] += get_inherited_methods() + ' '

	to_view = [x for x in graph.keys() if graph[x]['bases'] == '']
	while to_view:
		base_class = to_view.pop(0)
		childs = graph[base_class]['childs'].split(' ')
		if childs == ['']: continue
		to_view += childs
		for child in childs:
			add_inherited_methods_to_class(base_class, child)


# --------------------------------------------------------------------
def restructuring_classes_graph(graph, methods_hash):
	def number_of_code_lines_in_inherited_methods(base_id, child_id):
		base_members = graph[base_id]['members'].split(' ')
		child_members = graph[child_id]['members'].split(' ')
		sum_of_code_lines = \
			sum(methods_hash[x]['method_size'] for x in child_members if x in base_members and x != '')
		return sum_of_code_lines

	def get_key_with_max_val(d):
		v = list(d.values())
		k = list(d.keys())
		return k[v.index(max(v))]

	to_view = [x for x in graph.keys() if graph[x]['childs'] == '']
	while to_view:
		child_class = to_view.pop(0)
		if graph[child_class]['bases'] == '': continue
		bases = [x for x in graph[child_class]['bases'].split(' ') if x != '']
		to_view += [x for x in bases if x not in to_view]
		bases_hash = {}
		for base in bases:
			bases_hash[base] = number_of_code_lines_in_inherited_methods(base, child_class)
		chosen_base = get_key_with_max_val(bases_hash)
		base_members = graph[chosen_base]['members'].split(' ')
		child_members = graph[child_class]['members'].split(' ')
		graph[child_class]['members'] = ' '.join(x for x in child_members if x not in base_members)
		graph[child_class]['bases'] = chosen_base
		for base in bases:
			if base != chosen_base: graph[base]['childs'] = \
				' '.join(x for x in graph[base]['childs'].split(' ') if x != child_class)


# --------------------------------------------------------------------
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
		f.write('}\n\n')

	f = open(f_name + '.java', 'w')
	method_list = [str(Method['id']) for Method in untangle_obj.Method]
	f.write('package ' + f_name)
	f.write('\n\nclass ' + f_name + '\n{\n\n')
	for key in graph.keys(): write_class_to_file(key)
	f.write('}\n')
