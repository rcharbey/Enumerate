#
# Raphael Charbey, 2014
#
from igraph import Graph
import sys
import json
import profile
sys.path.append("/home/raphael/MPRI/Stage MPRI/sources/patterns/PATTERNS")
import patterns_5

class Vsub:
  def __init__(self,v,g):
    self.vsub = [v, None, None, None, None]
    self.neighbors_vsub = [[], [], [], [], []]
    self.degree_vsub = [0, 0, 0, 0, 0]
    self.des = 0
    self.length_vsub = 1
    self.index_vsub = [-1]*len(g.vs)
    self.index_vsub[v.index] = 0
    self.vext = []
    self.adjacency_matrix_vsub = [[False]*5]*5

GLOBAL_POWER_TABLE = [0, 6, 36, 216, 1296]
GLOBAL_POWER_DIFFERENCES_TABLE = [6, 30, 180, 1080]

def create_graph(name):
    path = "./FBSAMPLE/"+name+"/friends.jsons"
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
  
def degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, conflict, referee, degree_vsub, dic_pos_count, pos_count):
    i = 0
    list_of_conflictual_vertices = []
    index_of_referee = -1
    while i < length_vsub:
        if degree_vsub[i] == conflict:
            list_of_conflictual_vertices.append(i)
        elif degree_vsub[i] == referee:
            index_of_referee = i
            pos_count[vsub[i].index][dic_pos_count[referee]-1] += 1
        else:
            pos_count[vsub[i].index][dic_pos_count[degree_vsub[i]]-1] += 1
        i += 1
    for index_of_conflictual_vertex in list_of_conflictual_vertices:
        if adjacency_matrix_vsub[index_of_conflictual_vertex][index_of_referee] or adjacency_matrix_vsub[index_of_referee][index_of_conflictual_vertex]:
            pos_count[vsub[index_of_conflictual_vertex].index][dic_pos_count[degree_vsub[index_of_conflictual_vertex]][0]-1] += 1
        else:
            pos_count[vsub[index_of_conflictual_vertex].index][dic_pos_count[degree_vsub[index_of_conflictual_vertex]][1]-1] += 1

def calculate_neighbors_degree(v, neighbors_vsub, degree_vsub):
    result = 0
    for n in neighbors_vsub[v]:
        result += 1+degree_vsub[n]
    return result
      
def disambiguate2122(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pat_count, pos_count):
    if degree_vsub[4] == 2 and adjacency_matrix_vsub[max(neighbors_vsub[4][0], neighbors_vsub[4][1])][min(neighbors_vsub[4][0], neighbors_vsub[4][1])]:
        pat_count[21-1] += 1
        pos_count[vsub[4].index][51-1] += 1
        i = 0
        while i <= 3:
            if degree_vsub[i] == 2:
                pos_count[vsub[i].index][50-1] += 1
            else:
                pos_count[vsub[i].index][52-1] += 1
            i += 1
        return
    nd = calculate_neighbors_degree(4, neighbors_vsub, degree_vsub)
    if nd == 7:
        pat_count[21-1] += 1
        pos_count[vsub[4].index][50-1] += 1
        i = 0
        while i <= 3:
            if degree_vsub[i] == 2:
                if adjacency_matrix_vsub[4][i]:
                    pos_count[vsub[i].index][50-1] += 1
                else:
                    pos_count[vsub[i].index][51-1] += 1
            else:
                pos_count[vsub[i].index][52-1] += 1
            i += 1
    elif nd == 10:
        pat_count[21-1] += 1
        degree_vsub2 = list(degree_vsub)
        i = 4
        while i >= 0:
            for n in neighbors_vsub[i]:
                degree_vsub2[n] += 1
            i -= 1
        i = 0
        while i <= 4:
            if degree_vsub2[i] == 7:
                pos_count[vsub[i].index][50-1] += 1
            elif degree_vsub2[i] == 8:
                pos_count[vsub[i].index][51-1] += 1
            else:
                pos_count[vsub[i].index][52-1] += 1
            i += 1
        return
    pat_count[22-1] += 1
    i = 0
    while i <= 4:
        pos_count[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
        i += 1
    
def disambiguate1317(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pat_count, pos_count):
    d = degree_vsub[4]
    if d == 1 and degree_vsub[neighbors_vsub[4][0]] == 2:
        pat_count[13-1] += 1
        pos_count[vsub[4].index][25-1] += 1
        pos_count[vsub[3].index][26-1] += 1
        i = 0
        while i <= 2:
            if degree_vsub[i] == 2:
                pos_count[vsub[i].index][27-1] += 1
            else:
                pos_count[vsub[i].index][28-1] += 1
            i += 1
    elif d == 2 and adjacency_matrix_vsub[max(neighbors_vsub[4][0], neighbors_vsub[4][1])][min(neighbors_vsub[4][0], neighbors_vsub[4][1])]:
        pat_count[13-1] += 1
        pos_count[vsub[4].index][27-1] += 1
        i = 0
        while i <= 4:
            if degree_vsub[i] == 2:
                if i in neighbors_vsub[4]:
                    pos_count[vsub[i].index][27-1] += 1
                else:
                    pos_count[vsub[i].index][26-1] += 1
            else:
                pos_count[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
            i += 1
    else:
        pat_count[17-1] += 1
        if degree_vsub[4] == 2:
            if degree_vsub[neighbors_vsub[4][0]] == degree_vsub[neighbors_vsub[4][1]]:
                pos_count[vsub[4].index][37-1] += 1
                i = 0
                while i <= 3:
                    if degree_vsub[i] == 2:
                        pos_count[vsub[i].index][38-1] += 1
                    else:
                        pos_count[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
                    i += 1
            else:
                pos_count[vsub[4].index][38-1] += 1
                i = 0
                while i <= 3:
                    if degree_vsub[i] == 2:
                        if i in neighbors_vsub[4]:
                            pos_count[vsub[i].index][37-1] += 1
                        else:
                            pos_count[vsub[i].index][38-1] += 1
                    else:
                        pos_count[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
                    i += 1
        else:
            i = 0
            while i <= 4:
                if degree_vsub[i] == 2 :
                    if i in neighbors_vsub[3]:
                        pos_count[vsub[i].index][38-1] += 1
                    else:
                        pos_count[vsub[i].index][37-1] += 1
                else:
                    pos_count[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
                i += 1

def index_pattern(vsub, neighbors_vsub, length_vsub, adjacency_matrix_vsub, degree_vsub, des, pat_count, pos_count, patterns, power_table, power_differences_table):
    pattern_matching = patterns[des]
    if pattern_matching[0] == 2122:
        disambiguate2122(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pat_count, pos_count)
    elif pattern_matching[0] == 1317:
        disambiguate1317(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pat_count, pos_count)
    else:
        pat_count[pattern_matching[0]-1] += 1
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
                pos_count[vsub[i].index][pattern_matching[1][1]-1] += 1
                i += 1
            for index_of_conflictual_vertex in list_of_conflictual_vertices:
                if adjacency_matrix_vsub[index_of_conflictual_vertex][index_of_referee1] or adjacency_matrix_vsub[index_of_referee1][index_of_conflictual_vertex] or adjacency_matrix_vsub[index_of_referee2][index_of_conflictual_vertex] or adjacency_matrix_vsub[index_of_conflictual_vertex][index_of_referee2]:
                    pos_count[vsub[index_of_conflictual_vertex].index][pattern_matching[1][degree_vsub[index_of_conflictual_vertex]][0]-1] += 1
                else:
                    pos_count[vsub[index_of_conflictual_vertex].index][pattern_matching[1][degree_vsub[index_of_conflictual_vertex]][1]-1] += 1
        elif pattern_matching[0] == 12:
            degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, 1, 2, degree_vsub, pattern_matching[1], pos_count)
        elif pattern_matching[0] == 18:
            degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, 3, 1, degree_vsub, pattern_matching[1], pos_count)
        elif pattern_matching[0] == 26:
            degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, 3, 1, degree_vsub, pattern_matching[1], pos_count)
        else:
            i = 0
            while i < length_vsub:
                pos_count[vsub[i].index][pattern_matching[1][degree_vsub[i]]-1] += 1
                i += 1
       
def calculate_des(index_vsub, length_vsub, neighbors_vsub, power_table):
    des = 0
    list_of_degrees = [0]*length_vsub
    i = length_vsub-1
    while i >= 0:
        temp = 0
        for neighbor in neighbors_vsub[i]:
            list_of_degrees[index_vsub[neighbor.index]] += 1
            temp += 1
        des += power_table[temp+list_of_degrees[i]]
        i -= 1
    return des

def extend_subgraph(list_neighbors, vsub, neighbors_vsub, length_vsub, index_vsub, adjacency_matrix_vsub, degree_vsub, des, vext, 
                    v, k, pat_count, pos_count, patterns, power_table, power_differences_table):
    if length_vsub > 1:
        index_pattern(vsub, neighbors_vsub, length_vsub, adjacency_matrix_vsub, degree_vsub, des, pat_count, pos_count, patterns, power_table, power_differences_table)
        if length_vsub == k:
            return
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
        extend_subgraph(list_neighbors, vsub, neighbors_vsub, length_vsub+1, index_vsub, adjacency_matrix_vsub, degree_vsub, 
                        des+des2+power_table[degree_vsub[length_vsub]], vext2, v, k, pat_count, pos_count, patterns, power_table, power_differences_table)
        index_vsub[w.index] = -1
        for neighbor in neighbors_vsub[length_vsub]:
            adjacency_matrix_vsub[length_vsub][neighbor] = False
            degree_vsub[neighbor] -= 1
        degree_vsub[length_vsub] = 0
        neighbors_vsub[length_vsub] = []
        
def enumerate_from_v(v,pos_count,pat_count,adjacency_matrix_vsub,length,list_neighbors,k): 
    patterns = patterns_5.PATTERNS
    power_table = GLOBAL_POWER_TABLE
    power_differences_table = GLOBAL_POWER_DIFFERENCES_TABLE
    vsub = [v, None, None, None, None]
    neighbors_vsub = [[], [], [], [], []]
    degree_vsub = [0, 0, 0, 0, 0]
    des = 0
    length_vsub = 1
    index_vsub = [-1]*length
    index_vsub[v.index] = 0
    vext = []
    for u in list_neighbors[v.index]:
	if u.index > v.index:
	    vext.append(u)
	else:
	    break
    if vext:
	extend_subgraph(list_neighbors, vsub, neighbors_vsub, length_vsub, index_vsub, adjacency_matrix_vsub, degree_vsub, des, vext, v, k, pat_count, 
			pos_count, patterns, power_table, power_differences_table)
  
  
def characterize_with_patterns(graph, k):
    vs = graph.vs
    length = len(vs)
    pat_count = 30*[0]
    pos_count = []
    i = 0
    while i < length:
        pos_count.append(73*[0])
        i += 1
    list_neighbors = create_list_neighbors(graph)
    adjacency_matrix_vsub = [[False]*5]*5
    for v in vs:
       enumerate_from_v(v,pos_count,pat_count,adjacency_matrix_vsub,length,list_neighbors,k)
    return (pat_count, pos_count) 
 
def main():
    graph = create_graph(sys.argv[1])
    #graph = Graph.Formula("A-B, B-C, C-A, B-D")
    print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
    #couple = characterize_with_patterns(graph, 5)
    #print couple[0]
    #for co in couple[1]:
      #print co
    vsub = Vsub(graph.vs[0],graph)
    print vsub.adjacency_matrix_vsub
    
#profile.run('main()')
main()

