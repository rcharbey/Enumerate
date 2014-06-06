#
# Raphael Charbey, 2014
#
from igraph import Graph
import sys
import json
import profile
sys.path.append("/home/raphael/MPRI/Stage MPRI/sources/patterns/PATTERNS")
import patterns_5

GLOBAL_POWER_TABLE = [0, 6, 36, 216, 1296]
GLOBAL_POWER_DIFFERENCES_TABLE = [6, 30, 180, 1080]

DICT = [
{
    "1 ":(2,2,[(1,2])),
    "1,1 ":(3,1,[(1,1])),
}
,
{
    "2":(4,1,[(2,2),(2,4])),
    "2,2":(7,1,[(1,1),(1,1])),
    "1":(5,2,[(1,1),(2,2])),
    "1,2":(6,1,[(2,2),(1,3])),
    "1,2,2":(8,2,[(2,2),(1,1])),
}
,
{
    "1":(6,3,[(2,1])),
    "1,1":(8,1,[(2,1])),
    "1,1,1":(9,1,[(1,1])),
}
,
{
    "4":(10,5,[(1,1),(2,2),(3,3),(4,4])),
    "3":(12,2,[(4,4),(3,3),(5,5),(2,2])),
    "3,4":(13,1,[(4,4),(3,3),(2,2),(1,1])),
    "2":(12,2,[(2,2),(1,1),(3,3),(4,4])),
    "2,4":(17,3,[(1,1),(2,2),(3,3),(4,4])),
    "2,3":(14,3,[(1,1),(2,2),(4,4),(5,5])),
    "2,3,4":(18,3,[(1,1),(2,2),(3,3),(4,4])),
    "1":(10,1,[(2,2),(3,3),(4,4),(5,5])),
    "1,4":(16,5,[(1,1),(2,2),(3,3),(4,4])),
    "1,3":(17,3,[(4,4),(3,3),(2,2),(5,5])),
    "1,3,4":(21,2,[(4,4),(5,5),(3,3),(1,1])),
    "1,2":(13,1,[(1,1),(2,2),(3,3),(4,4])),
    "1,2,4":(21,2,[(1,1),(3,3),(5,5),(4,4])),
    "1,2,3":(18,3,[(4,4),(3,3),(2,2),(1,1])),
    "1,2,3,4":(24,5,[(1,1),(2,2),(3,3),(4,4])),
}
,
{
    "2":(12,4,[(1,1),(3,2])),
    "2,2":(17,4,[(2,2),(3,1])),
    "2,2,2":(22,1,[(2,2),(1,1])),
    "1":(11,2,[(1,1),(2,2])),
    "1,2":(15,2,[(3,3),(1,2])),
    "1,2,2":(19,4,[(2,2),(3,1])),
    "1,2,2,2":(25,1,[(1,1),(2,2])),
}
,
{
    "3":(13,4,[(1,1),(2,2),(3,3])),
    "2":(15,2,[(1,1),(3,3),(2,2])),
    "2,3":(20,3,[(1,1),(2,2),(3,3])),
    "1":(14,1,[(2,3),(4,4),(5,5])),
    "1,3":(21,5,[(3,1),(2,2),(4,4])),
    "1,2":(19,3,[(4,3),(2,2),(1,1])),
    "1,2,3":(24,3,[(2,1),(5,5),(4,4])),
    "1,1":(18,4,[(3,3),(2,2),(1,1])),
    "1,1,3":(26,2,[(3,3),(2,2),(1,1])),
    "1,1,2":(23,3,[(3,3),(2,2),(1,1])),
    "1,1,2,3":(28,3,[(2,2),(3,3),(1,1])),
}
,
{
    "2":(17,1,[(3,3),(2,4])),
    "2,2":(22,1,[(1,1),(2,2])),
    "1":(17,1,[(2,4),(3,3])),
    "1,2":(21,1,[(2,5),(3,4])),
    "1,2,2":(26,3,[(3,1),(2,2])),
    "1,1":(22,1,[(2,2),(1,1])),
    "1,1,2":(26,3,[(2,2),(3,1])),
    "1,1,2,2":(27,3,[(1,1),(2,2])),
}
,
{
    "2":(19,1,[(3,3),(2,4])),
    "2,2":(25,2,[(2,2),(1,1])),
    "1":(18,1,[(2,4),(3,3])),
    "1,2":(24,4,[(3,1),(2,3])),
    "1,2,2":(28,2,[(2,1),(3,3])),
    "1,1":(26,1,[(2,2),(3,3])),
    "1,1,2":(27,1,[(2,2),(3,1])),
    "1,1,2,2":(29,2,[(1,1),(2,2])),
}
,
{
    "1":(23,1,[(2,3])),
    "1,1":(28,1,[(3,2])),
    "1,1,1":(29,1,[(2,1])),
    "1,1,1,1":(30,1,[(1,1])),
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

def calculate_neighbors_degree(v, neighbors_vsub, degree_vsub):
    result = 0
    for n in neighbors_vsub[v]:
        result += 1+degree_vsub[n]
    return result

def index_pattern(vsub, neighbors_vsub, length_vsub, adjacency_matrix_vsub, degree_vsub, des, pt, ps, patterns, power_table, power_differences_table):
    pattern_matching = patterns[des]
    if pattern_matching[0] == 2122:
        disambiguate2122(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pt, ps)
    elif pattern_matching[0] == 1317:
        disambiguate1317(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pt, ps)
    else:
        pt[pattern_matching[0]-1] += 1
        if pattern_matching[0] == 10:
            i = 0
            list_of_conflictual_vertices = []
            index_of_referee1 = -1
            index_of_referee2 = -1
            while i < length_vsub:
                if degree_vsub[i] == 2:
                    list_of_conflictual_vertices.append(i)
                else:
                    if index_of_referee1 == -1:
                        index_of_referee1 = i
                    else:
                        index_of_referee2 = i
                ps[vsub[i].index][pattern_matching[1][1]-1] += 1
                i += 1
            for index_of_conflictual_vertex in list_of_conflictual_vertices:
                if adjacency_matrix_vsub[index_of_conflictual_vertex][index_of_referee1] or adjacency_matrix_vsub[index_of_referee1][index_of_conflictual_vertex] or adjacency_matrix_vsub[index_of_referee2][index_of_conflictual_vertex] or adjacency_matrix_vsub[index_of_conflictual_vertex][index_of_referee2]:
                    ps[vsub[index_of_conflictual_vertex].index][pattern_matching[1][degree_vsub[index_of_conflictual_vertex]][0]-1] += 1
                else:
                    ps[vsub[index_of_conflictual_vertex].index][pattern_matching[1][degree_vsub[index_of_conflictual_vertex]][1]-1] += 1
        elif pattern_matching[0] == 12:
            degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, 1, 2, degree_vsub, pattern_matching[1], ps)
        elif pattern_matching[0] == 18:
            degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, 3, 1, degree_vsub, pattern_matching[1], ps)
        elif pattern_matching[0] == 26:
            degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, 3, 1, degree_vsub, pattern_matching[1], ps)
        else:
            i = 0
            while i < length_vsub:
                ps[vsub[i].index][pattern_matching[1][degree_vsub[i]]-1] += 1
                i += 1


def extend_subgraph(list_neighbors, vsub, neighbors_vsub, length_vsub, index_vsub, adjacency_matrix_vsub, degree_vsub, des, vext, 
                    v, k, pt, ps, patterns, power_table, power_differences_table):
    if length_vsub > 1:
        index_pattern(vsub, neighbors_vsub, length_vsub, adjacency_matrix_vsub, degree_vsub, des, pt, ps, patterns, power_table, power_differences_table)
    while vext:
        w = vext.pop()
        vext2 = list(vext)
        des2 = 0
        for u in list_neighbors[w.index]:
            if u.index >= v.index:
                if not index_vsub[u.index] == -1 :
                    neighbors_vsub[length_vsub].append(index_vsub[u.index])
                    degree_vsub[length_vsub] += 1
                    des2 += power_differences_table[degree_vsub[index_vsub[u.index]]]
                    degree_vsub[index_vsub[u.index]] += 1
                    adjacency_matrix_vsub[length_vsub][index_vsub[u.index]] = True
                elif not in_neighborhood_vsub(v, index_vsub, list_neighbors[u.index]):
                    vext2.append(u)
            else:
                break
        vsub[length_vsub] = w
        index_vsub[w.index] = length_vsub
        if length_vsub != k-1:
            extend_subgraph(list_neighbors, vsub, neighbors_vsub, length_vsub+1, index_vsub, adjacency_matrix_vsub, degree_vsub, 
                        des+des2+power_table[degree_vsub[length_vsub]], vext2, v, k, pt, ps, patterns, power_table, power_differences_table)
        else :
            index_pattern(vsub, neighbors_vsub, length_vsub + 1, adjacency_matrix_vsub, degree_vsub, des+des2+power_table[degree_vsub[length_vsub]], pt, ps, patterns, power_table, power_differences_table)  
        index_vsub[w.index] = -1
        for neighbor in neighbors_vsub[length_vsub]:
            adjacency_matrix_vsub[length_vsub][neighbor] = False
            degree_vsub[neighbor] -= 1
        degree_vsub[length_vsub] = 0
        neighbors_vsub[length_vsub] = []
  
def characterize_with_patterns(graph, k):
    vs = graph.vs
    length = len(vs)
    pt = 30*[0]
    ps = []
    i = 0
    patterns = patterns_5.PATTERNS
    power_table = GLOBAL_POWER_TABLE
    power_differences_table = GLOBAL_POWER_DIFFERENCES_TABLE
    while i < length:
        ps.append(73*[0])
        i += 1
    list_neighbors = create_list_neighbors(graph)
    for v in vs:
        vsub = [v, None, None, None, None]
        neighbors_vsub = [[], [], [], [], []]
        degree_vsub = [0, 0, 0, 0, 0]
        des = 0
        length_vsub = 1
        index_vsub = [-1]*length
        adjacency_matrix_vsub = [[False]*5]*5
        index_vsub[v.index] = 0
        vext = []
        for u in list_neighbors[v.index]:
            if u.index > v.index:
               vext.append(u)
            else:
               break
        if vext:
            extend_subgraph(list_neighbors, vsub, neighbors_vsub, length_vsub, index_vsub, adjacency_matrix_vsub, degree_vsub, des, vext, v, k, pt, 
                            ps, patterns, power_table, power_differences_table)
    return (pt, ps) 
 
def main():
    graph = create_graph(sys.argv[1])
    #graph = Graph.Formula(" A-B, A-C, A-D, A-E, B-C, C-D, C-F, D-E, D-F, D-G, E-G, E-H, F-G, G-H ")
    print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
    couple = characterize_with_patterns(graph, 5)
    print couple[0]
    return couple


main()