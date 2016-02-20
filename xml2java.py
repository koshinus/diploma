import untangle
import support_functions as sf
import graph_visualization as gv

#to_parse = untangle.parse('test.xml')
obj = untangle.parse('test.xml').GCC_XML

graph = sf.get_classes_graph(obj)

gv.make_graph_vis(graph, "CPP_classes_graph")

sf.add_inherited_methods_to_classes(graph, obj)
for Class in sf.get_classes_id_list(obj):
	print Class + ':' + graph[Class]['members']


sf.restructuring_classes_graph(graph, obj)
for Class in sf.get_classes_id_list(obj):
	print Class + ':' + graph[Class]['members']

gv.make_graph_vis(graph, "Java_classes_graph")

sf.generate_java_file('test', graph, obj)