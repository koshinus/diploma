import untangle
import support_functions as sf
import graph_visualization as gv

# to_parse = untangle.parse('test.xml')
obj = untangle.parse('test.xml').GCC_XML
# print type(obj)

graph = sf.get_classes_graph(obj)
methods_hash = sf.get_methods_hash(obj)

# for key in methods_hash.keys():
# print methods_hash[key]['method_size']

gv.make_graph_visualization(graph, "CPP_classes_graph", methods_hash)

sf.add_inherited_methods_to_classes(graph, obj)
# for Class in sf.get_classes_id_list(obj):
# print Class + ':' + graph[Class]['members']


sf.restructuring_classes_graph(graph, methods_hash)
# for Class in sf.get_classes_id_list(obj):
# print Class + ':' + graph[Class]['members']

gv.make_graph_visualization(graph, "Java_classes_graph", methods_hash)

sf.generate_java_file('test', graph, obj)
