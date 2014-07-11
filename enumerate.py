#
# Raphael Charbey, 2014
#
from igraph import Graph
import sys
import json
import profile
sys.path.append("/home/raphael/Algopol/sources/patterns/PATTERNS")
sys.path.append("~/patterns/PATTERNS")
import patterns_5
import time

DICT = [
    {   "[1]":(1,1,[(1,1)]) #0
    }
    ,
    {
        "[1]":(2,2,[(1,2)]), #1
        "[1, 1]":(3,1,[(1,1)])
    }
    ,
    {
        "[2]":(4,1,[(3,3),(2,4)]), #2
        "[2, 2]":(7,1,[(1,1),(2,2)]),
        "[1]":(5,2,[(1,1),(2,2)]),
        "[1, 2]":(6,1,[(2,2),(1,3)]),
        "[1, 2, 2]":(8,2,[(2,2),(1,1)])
    }
    ,
    {
        "[1]":(6,3,[(2,1)]), #3
        "[1, 1]":(8,1,[(2,1)]),
        "[1, 1, 1]":(9,1,[(1,1)])
    }
    ,
    {
        "[4]":(10,5,[(1,1),(2,2),(3,3),(4,4)]), #4
        "[3]":(12,2,[(4,4),(3,3),(5,5),(2,2)]),
        "[3, 4]":(13,1,[(4,4),(3,3),(2,2),(1,1)]),
        "[2]":(12,2,[(2,2),(1,1),(3,3),(4,4)]),
        "[2, 4]":(17,3,[(1,1),(2,2),(3,3),(4,4)]),
        "[2, 3]":(14,3,[(1,1),(2,2),(4,4),(5,5)]),
        "[2, 3, 4]":(18,3,[(1,1),(2,2),(3,3),(4,4)]),
        "[1]":(10,1,[(2,2),(3,3),(4,4),(5,5)]),
        "[1, 4]":(16,5,[(1,1),(2,2),(3,3),(4,4)]),
        "[1, 3]":(17,3,[(4,4),(3,3),(2,2),(5,5)]),
        "[1, 3, 4]":(21,2,[(4,4),(5,5),(3,3),(1,1)]),
        "[1, 2]":(13,1,[(1,1),(2,2),(3,3),(4,4)]),
        "[1, 2, 4]":(21,2,[(1,1),(3,3),(5,5),(4,4)]),
        "[1, 2, 3]":(18,3,[(4,4),(3,3),(2,2),(1,1)]),
        "[1, 2, 3, 4]":(24,5,[(1,1),(2,2),(3,3),(4,4)])
    }
    ,
    {
        "[2]":(12,4,[(1,1),(3,2)]), #5
        "[2, 2]":(17,4,[(2,2),(3,1)]),
        "[2, 2, 2]":(22,1,[(2,2),(1,1)]),
        "[1]":(11,2,[(1,1),(2,2)]),
        "[1, 2]":(15,2,[(3,3),(1,2)]),
        "[1, 2, 2]":(19,4,[(2,2),(3,1)]),
        "[1, 2, 2, 2]":(25,1,[(1,1),(2,2)])
    }
    ,
    {
        "[3]":(13,4,[(1,1),(2,2),(3,3)]), #6
        "[2]":(15,2,[(1,1),(3,3),(2,2)]),
        "[2, 3]":(20,3,[(1,1),(2,2),(3,3)]),
        "[1]":(14,1,[(2,3),(4,4),(5,5)]),
        "[1, 3]":(21,5,[(3,1),(2,2),(4,4)]),
        "[1, 2]":(19,3,[(4,3),(2,2),(1,1)]),
        "[1, 2, 3]":(24,3,[(2,1),(5,5),(4,4)]),
        "[1, 1]":(18,4,[(3,3),(2,2),(1,1)]),
        "[1, 1, 3]":(26,2,[(3,3),(2,2),(1,1)]),
        "[1, 1, 2]":(23,3,[(3,3),(2,2),(1,1)]),
        "[1, 1, 2, 3]":(28,3,[(2,2),(3,3),(1,1)])
    }
    ,
    {
        "[2]":(17,1,[(3,3),(2,4)]), #7
        "[2, 2]":(22,1,[(1,1),(2,2)]),
        "[1]":(17,1,[(2,4),(3,3)]),
        "[1, 2]":(21,1,[(2,5),(3,4)]),
        "[1, 2, 2]":(26,3,[(3,1),(2,2)]),
        "[1, 1]":(22,1,[(2,2),(1,1)]),
        "[1, 1, 2]":(26,3,[(2,2),(3,1)]),
        "[1, 1, 2, 2]":(27,3,[(1,1),(2,2)])
    }
    ,
    {
        "[2]":(19,1,[(3,3),(2,4)]), #8
        "[2, 2]":(25,2,[(2,2),(1,1)]),
        "[1]":(18,1,[(2,4),(3,3)]),
        "[1, 2]":(24,4,[(3,1),(2,3)]),
        "[1, 2, 2]":(28,2,[(2,1),(3,3)]),
        "[1, 1]":(26,1,[(2,2),(3,3)]),
        "[1, 1, 2]":(27,1,[(2,2),(3,1)]),
        "[1, 1, 2, 2]":(29,2,[(1,1),(2,2)])
    }
    ,
    {
        "[1]":(23,1,[(2,3)]), #9
        "[1, 1]":(28,1,[(3,2)]),
        "[1, 1, 1]":(29,1,[(2,1)]),
        "[1, 1, 1, 1]":(30,1,[(1,1)])
    }
]

def create_graph(name):
    path = "./data/"+name+"/friends.jsons"
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
            if vertex_to_index[jr["id"]] > vertex_to_index[neighbor["id"]]:
                list_of_edges.append((vertex_to_index[jr["id"]], vertex_to_index[neighbor["id"]]))      
    f.close()
    graph = Graph(list_of_edges)
    for v in graph.vs:
        v["name"] = index_to_vertex[v.index]
    return graph
           
def create_list_neighbors(graph):
    vs = graph.vs
    es = graph.es
    list_neighbors = []
    for v in vs:
        list_neighbors.append([])
    for e in es:
        list_neighbors[e.target].append(vs[e.source])
        list_neighbors[e.source].append(vs[e.target])
    for l in list_neighbors:
        l.sort(key =lambda vertex: vertex.index,  reverse = True)
    return list_neighbors  
  
def in_neighborhood_vsub(v, index_vsub, list_neighbors):
    for n in list_neighbors:
        if not index_vsub[n.index] == -1:
            return True
    return False
    
def add_to_classes_neighbors_new(classes_neighbors_new,classe_neighbor):
    i = 0
    if len(classes_neighbors_new) == 0:
        classes_neighbors_new.append(classe_neighbor)
        return
    while i < len(classes_neighbors_new):
        if classe_neighbor <= classes_neighbors_new[i]:
            classes_neighbors_new.insert(i,classe_neighbor)
            return
        i += 1
    classes_neighbors_new.append(classe_neighbor)

def index_pattern(vsub, id_vsub, classes_vsub, classes_neighbors_new, length_vsub, adjacency_matrix_vsub, k, pt, ps):
    dict_temp = DICT[id_vsub][str(classes_neighbors_new)]
    new_id_vsub = dict_temp[0]
    pt[new_id_vsub - 1] += 1
    new_classes_vsub = [0]*k
    i = 0
    while i < length_vsub-1:
        if adjacency_matrix_vsub[length_vsub-1][i]:
            new_classes_vsub[i] = dict_temp[2][classes_vsub[i]-1][0]
        else:
            new_classes_vsub[i] = dict_temp[2][classes_vsub[i]-1][1]
        i += 1
    new_classes_vsub[i] = dict_temp[1]
    return (new_id_vsub,new_classes_vsub)
    

def extend_subgraph(list_neighbors, vsub, length_vsub, index_vsub, adjacency_matrix_vsub, id_vsub, classes_vsub, vext, 
                    v, k, pt, ps):
    while vext:
        w = vext.pop()
        vext2 = list(vext)
        classes_neighbors_new = []
        for u in list_neighbors[w.index]:
            if u.index >= v.index:
                if index_vsub[u.index] == -1 :
                    if not in_neighborhood_vsub(v, index_vsub, list_neighbors[u.index]):
                        vext2.append(u)
                else:
                    #classes_neighbors_new.append(classes_vsub[index_vsub[u.index]])
                    add_to_classes_neighbors_new(classes_neighbors_new,classes_vsub[index_vsub[u.index]])
                    adjacency_matrix_vsub[length_vsub][index_vsub[u.index]] = True
            else:
                break
        #classes_neighbors_new.sort()
        vsub[length_vsub] = w
        index_vsub[w.index] = length_vsub
        couple = index_pattern(vsub, id_vsub, classes_vsub, classes_neighbors_new, length_vsub+1, adjacency_matrix_vsub, k, pt, ps)
        if length_vsub != k-1:
            extend_subgraph(list_neighbors, vsub, length_vsub+1, index_vsub, adjacency_matrix_vsub, couple[0], couple[1],
                        vext2, v, k, pt, ps)
        index_vsub[w.index] = -1
        adjacency_matrix_vsub[length_vsub] = [False]*k
  
def characterize_with_patterns(graph, k):
    vs = graph.vs
    length = len(vs)
    pt = 30*[0]
    ps = []
    i = 0
    patterns = patterns_5.PATTERNS
    while i < length:
        ps.append(73*[0])
        i += 1
    list_neighbors = create_list_neighbors(graph)
    for v in vs:
        id_vsub = 0
        length_vsub = 1
        index_vsub = [-1]*length
        temp = 0
        adjacency_matrix_vsub = []
        vsub = []
        neighbors_vsub = []
        classes_vsub = []
        while temp < k:
            adjacency_matrix_vsub.append([False]*k)
            vsub.append(None)
            neighbors_vsub.append([])
            classes_vsub.append(0)
            temp += 1
        classes_vsub[0] = 1
        vsub[0] = v
        index_vsub[v.index] = 0
        vext = []
        for u in list_neighbors[v.index]:
            if u.index > v.index:
               vext.append(u)
            else:
               break
        if vext:
            extend_subgraph(list_neighbors, vsub, length_vsub, index_vsub, adjacency_matrix_vsub, id_vsub, classes_vsub, vext, v, k, pt, ps)
    return (pt, ps) 
 
def main(k, file_graph):
    begin = time.time()
    plot = open("plot.txt","a")
    graph = create_graph(file_graph)
    print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
    couple = characterize_with_patterns(graph, int(k))
    print couple[0]
    plot.write("D" + "," + str(len(graph.vs)) + "," + str(len(graph.es)) + "," + str(time.time()-begin) + "\n")
    return couple
