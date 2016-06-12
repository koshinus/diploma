import untangle
import support_functions as sf
import graph_visualization as gv
from subprocess import call

#call(['gccxml', argv[1]])
# to_parse = untangle.parse('test.xml')
obj = untangle.parse('test1.xml').GCC_XML
# print type(obj)
'''
method_hash = {}
for Method in obj.Method:
	method_hash[str(Method['id'])] = str(Method['overrides'])
print method_hash
'''
graph = sf.get_classes_graph(obj)
methods_hash = sf.get_methods_hash(obj)

# for key in methods_hash.keys():
# print methods_hash[key]['method_size']

gv.make_graph_visualization(graph, "CPP_classes_graph", methods_hash)


for x in sf.get_classes_id_list(obj):
	lst = [y + '/' + methods_hash[y]['name'] for y in graph[x]['members'].split(' ') if y in methods_hash.keys()]
	print graph[x]['name'] + ':' + ' '.join(lst)

sf.add_inherited_methods_to_classes(graph, methods_hash)
# for Class in sf.get_classes_id_list(obj):
# print Class + ':' + graph[Class]['members']

for x in sf.get_classes_id_list(obj):
	lst = [y + '/' + methods_hash[y]['name'] for y in graph[x]['members'].split(' ') if y in methods_hash.keys()]
	print graph[x]['name'] + ':' + ' '.join(lst)

sf.restructuring_classes_graph(graph, methods_hash)
# for Class in sf.get_classes_id_list(obj):
# print Class + ':' + graph[Class]['members']

gv.make_graph_visualization(graph, "Java_classes_graph", methods_hash)

sf.generate_java_file('test', graph, obj)
