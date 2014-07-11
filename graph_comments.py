import sys
import json
from igraph import *
import math

def create_graph_comments(folder, name):
    path = "./data/"+folder+"/"+name+"/statuses.jsons"
    f = open(path, 'r')
    dict_of_edges = {}
    index_to_vertex = {}
    vertex_to_index = {}
    nb_comments_per_alter = []
    nb_of_vertices = 0
    nb_comments = 0
    for line in f:
        nb_comments += 1
        jr = json.loads(line)
        if not "comments" in jr:
            continue
        list_current_com = []
        for comment in jr["comments"]:
            if not comment["from"]["id"] == name and not comment["from"]["id"] in vertex_to_index:
                nb_comments_per_alter.append(0)
                vertex_to_index[comment["from"]["id"]] = nb_of_vertices
                index_to_vertex[nb_of_vertices] = comment["from"]["id"]
                nb_of_vertices += 1
            if not comment["from"]["id"] == name:
                nb_comments_per_alter[vertex_to_index[comment["from"]["id"]]] += 1
        for comment in jr["comments"]:
            if not comment["from"]["id"] == name : 
                for comment_second in jr["comments"]:
                    if not comment_second["from"]["id"] == name:
                        id_comment = vertex_to_index[comment["from"]["id"]]
                        id_second = vertex_to_index[comment_second["from"]["id"]]
                        if id_comment < id_second:
                            if (id_comment, id_second) not in dict_of_edges:
                                dict_of_edges[(id_comment, id_second)] = 1
                            else:
                                dict_of_edges[(id_comment, id_second)] += 1
    f.close()
    graph = Graph(dict_of_edges.keys())
    for v in graph.vs:
        v["name"] = index_to_vertex[v.index]
        v["size"] = 10+10*math.log(nb_comments_per_alter[vertex_to_index[v["name"]]])
    for e in graph.es():
        e["width"] = 1+math.log(dict_of_edges[e.tuple])
    print nb_comments
    return graph
    
    
def create_graph_friends(folder, name):
    path = "./data/"+folder+"/"+name+"/friends.jsons"
    f = open(path, 'r')
    list_of_edges = []
    index_to_vertex = {}
    vertex_to_index = {}
    nb_of_vertices = 0
    for line in f:
        jr = json.loads(line)
        if not "mutual" in jr:
            continue
        if not jr["id"] in vertex_to_index:
            vertex_to_index[jr["id"]] = nb_of_vertices
            index_to_vertex[nb_of_vertices] = jr["id"]
            nb_of_vertices += 1
        for neighbor in jr["mutual"]:
            if not neighbor["id"] in vertex_to_index:
                vertex_to_index[neighbor["id"]] = nb_of_vertices
                index_to_vertex[nb_of_vertices] = neighbor["id"]
                nb_of_vertices += 1
            if vertex_to_index[jr["id"]] < vertex_to_index[neighbor["id"]]:
                list_of_edges.append((vertex_to_index[jr["id"]], vertex_to_index[neighbor["id"]]))      
    f.close()
    graph = Graph(list_of_edges)
    for v in graph.vs:
        v["name"] = index_to_vertex[v.index]
    return graph
     
     
def fusion(graph1, graph2):
    vs1 = graph1.vs
    vs2 = graph2.vs
    dict_of_edges = {}
    for e2 in graph2.es:
        e2["ok"] = 0
    for e1 in graph1.es:
        e1["ok"] = 0
        for e2 in graph2.es:
            if vs1[e1.source]["name"] == vs2[e2.source]["name"] and vs1[e1.target]["name"] == vs2[e2.target]["name"]:
                dict_of_edges[(e1.source, e1.target)] = 3
                e2["ok"] = 1
                e1["ok"] = 1
                break
        if e1["ok"] == 0:
            dict_of_edges[(e1.source, e1.target)] = 1
    for e2 in graph2.es:
        if e2["ok"] == 0:
            i = 0
            while i < len(vs1):
                if vs1[i]["name"] == vs2[e2.source]["name"]:
                    id_source = i
                if vs1[i]["name"] == vs2[e2.target]["name"]:
                    id_target = i
                i += 1
            if id_source < id_target:
                dict_of_edges[(id_source, id_target)] = 2
            else:
                dict_of_edges[(id_target, id_source)] = 2
    graph = Graph(dict_of_edges.keys())
    return (graph, dict_of_edges)
    
        
    
g1 = create_graph_friends(sys.argv[1], sys.argv[2])
g2 = create_graph_comments(sys.argv[1], sys.argv[2])
couple = fusion(g1, g2)
graph = couple[0]
dict_of_edges = couple[1]
layout=graph.layout("auto")


for e in graph.es:
    e["width"] = 2
    if dict_of_edges[(e.source, e.target)] == 3:
        e["color"] = "red"    
    if dict_of_edges[(e.source, e.target)] == 1:
        e["color"] = "rgba(0,0,0,0)"
plot(graph,layout=layout,bbox=(800,800))

for e in graph.es:
    if dict_of_edges[(e.source, e.target)] == 1:
        e["color"] = "black"
    if dict_of_edges[(e.source, e.target)] == 2:
        e["color"] = "rgba(0,0,0,0)"
plot(graph,layout=layout,bbox=(800,800))
        
