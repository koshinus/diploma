import untangle
import support_functions

#to_parse = untangle.parse('test.xml')
obj = untangle.parse('test.xml').GCC_XML

graph = support_functions.get_classes_graph(obj)

support_functions.add_inherited_methods_to_classes(graph, obj)
for Class in support_functions.get_classes_id_list(obj):
	print Class + ':' + graph[Class]['members']


support_functions.restructuring_classes_graph(graph, obj)
for Class in support_functions.get_classes_id_list(obj):
	print Class + ':' + graph[Class]['members']

support_functions.generate_java_file('test', graph, obj)