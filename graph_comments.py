import sys
import json
from igraph import *
import math


def create_graph(folder, name):
    path = "./data/"+folder+"/"+name+"/friends.jsons"
    f = open(path, 'r')
    dict_of_edges = {}
    index_to_vertex = {}
    index_to_graph_in = {}
    vertex_to_index = {}
    nb_of_vertices = 0
    for line in f:
        jr = json.loads(line)
        if not "mutual" in jr:
            continue
        if not jr["id"] in vertex_to_index:
            vertex_to_index[jr["id"]] = nb_of_vertices
            index_to_vertex[nb_of_vertices] = jr["id"]
            index_to_graph_in[nb_of_vertices] = 1
            nb_of_vertices += 1
        for neighbor in jr["mutual"]:
            if not neighbor["id"] in vertex_to_index:
                vertex_to_index[neighbor["id"]] = nb_of_vertices
                index_to_vertex[nb_of_vertices] = neighbor["id"]
                index_to_graph_in[nb_of_vertices] = 1
                nb_of_vertices += 1
            if vertex_to_index[jr["id"]] < vertex_to_index[neighbor["id"]]:
                dict_of_edges[(vertex_to_index[jr["id"]], vertex_to_index[neighbor["id"]])] = 1      
    f.close()
    path = "./data/"+folder+"/"+name+"/statuses.jsons"
    f = open(path, 'r')
    nb_comments_per_alter = []
    nb_comments = 0
    for line in f:
        nb_comments += 1
        jr = json.loads(line)
        if not "comments" in jr:
            continue
        list_current_com = []
        for v in vertex_to_index:
            nb_comments_per_alter.append(0)
        for comment in jr["comments"]:
            if not comment["from"]["id"] == name :
                if not comment["from"]["id"] in vertex_to_index:
                    nb_comments_per_alter.append(0)
                    vertex_to_index[comment["from"]["id"]] = nb_of_vertices
                    index_to_vertex[nb_of_vertices] = comment["from"]["id"]
                    index_to_graph_in[nb_of_vertices] = 2
                    nb_of_vertices += 1
                else:
                    nb_comments_per_alter[vertex_to_index[comment["from"]["id"]]] += 1
                    index_to_graph_in[vertex_to_index[comment["from"]["id"]]] = 3
        for comment in jr["comments"]:
            if not comment["from"]["id"] == name : 
                for comment_second in jr["comments"]:
                    if not comment_second["from"]["id"] == name:
                        id_comment = vertex_to_index[comment["from"]["id"]]
                        id_second = vertex_to_index[comment_second["from"]["id"]]
                        if id_comment < id_second:
                            if (id_comment, id_second) not in dict_of_edges:
                                dict_of_edges[(id_comment, id_second)] = -1
                            else:
                                dict_of_edges[(id_comment, id_second)] = dict_of_edges[(id_comment, id_second)] * 2
    f.close()
    graph = Graph(dict_of_edges.keys())
    for v in graph.vs:
        v["name"] = index_to_vertex[v.index]
        v["size"] = 10+10*math.log(1+nb_comments_per_alter[vertex_to_index[v["name"]]])
    graph = Graph(dict_of_edges.keys())
    return (graph, index_to_graph_in, dict_of_edges)
    
    
triple = create_graph(sys.argv[1], sys.argv[2])
graph = triple[0]
index_to_graph_in = triple[1]
dict_of_edges = triple[2]
print index_to_graph_in

layout = graph.layout("kk")


for e in graph.es:
    e["color"] = "black"
    e["width"] = 2
    if dict_of_edges[(e.source, e.target)] > 1:
        e["color"] = "red"    
    if dict_of_edges[(e.source, e.target)] < 0:
        e["color"] = "rgba(0,0,0,0)"
    for v in graph.vs:
        if index_to_graph_in[v.index] == 2:
            v["color"] = "rgba(0,0,0,0)"
plot(graph,layout=layout,bbox=(800,800))

for e in graph.es:
    if dict_of_edges[(e.source, e.target)] < 0:
        e["color"] = "black"
    if dict_of_edges[(e.source, e.target)] > 0:
        e["color"] = "rgba(0,0,0,0)"
    e["width"] = 1+math.log(abs(dict_of_edges[e.tuple]))
    for v in graph.vs:
        v["color"] = "red"
        if index_to_graph_in[v.index] == 1:
            v["color"] = "rgba(0,0,0,0)"
plot(graph,layout=layout,bbox=(800,800))
        
        
#Super families Milo
#David.o.fourquet@gmail.com
