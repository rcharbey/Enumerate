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
  def __init__(self,length):
    self.vertices = [None, None, None, None, None]
    self.neighbors = [[], [], [], [], []]
    self.degree = [0, 0, 0, 0, 0]
    self.des = 0
    self.length = 1
    self.index = [-1]*length
    #self.vsub.index[v.index] = 0
    self.adjacency_matrix = [[False]*5]*5
    

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
  
def in_neighborhood_vsub.vertices(v, vsub.index, list_neighbors):
    for n in list_neighbors:
        if not vsub.index[n.index] == -1:
            return True
    return False
  
def degree_disambiguation(vsub.vertices, vsub.length, adjacency_matrix_vsub.vertices, conflict, referee, vsub.degree, dic_pos_count, pos_count):
    i = 0
    list_of_conflictual_vertices = []
    index_of_referee = -1
    while i < vsub.length:
        if vsub.degree[i] == conflict:
            list_of_conflictual_vertices.append(i)
        elif vsub.degree[i] == referee:
            index_of_referee = i
            pos_count[vsub.vertices[i].index][dic_pos_count[referee]-1] += 1
        else:
            pos_count[vsub.vertices[i].index][dic_pos_count[vsub.degree[i]]-1] += 1
        i += 1
    for index_of_conflictual_vertex in list_of_conflictual_vertices:
        if adjacency_matrix_vsub.vertices[index_of_conflictual_vertex][index_of_referee] or adjacency_matrix_vsub.vertices[index_of_referee][index_of_conflictual_vertex]:
            pos_count[vsub.vertices[index_of_conflictual_vertex].index][dic_pos_count[vsub.degree[index_of_conflictual_vertex]][0]-1] += 1
        else:
            pos_count[vsub.vertices[index_of_conflictual_vertex].index][dic_pos_count[vsub.degree[index_of_conflictual_vertex]][1]-1] += 1

def calculate_neighbors_degree(v, vsub.neighbors, vsub.degree):
    result = 0
    for n in vsub.neighbors[v]:
        result += 1+vsub.degree[n]
    return result
      
def disambiguate2122(pattern_matching, vsub.vertices, vsub.neighbors, adjacency_matrix_vsub.vertices, vsub.degree, pat_count, pos_count):
    if vsub.degree[4] == 2 and adjacency_matrix_vsub.vertices[max(vsub.neighbors[4][0], vsub.neighbors[4][1])][min(vsub.neighbors[4][0], vsub.neighbors[4][1])]:
        pat_count[21-1] += 1
        pos_count[vsub.vertices[4].index][51-1] += 1
        i = 0
        while i <= 3:
            if vsub.degree[i] == 2:
                pos_count[vsub.vertices[i].index][50-1] += 1
            else:
                pos_count[vsub.vertices[i].index][52-1] += 1
            i += 1
        return
    nd = calculate_neighbors_degree(4, vsub.neighbors, vsub.degree)
    if nd == 7:
        pat_count[21-1] += 1
        pos_count[vsub.vertices[4].index][50-1] += 1
        i = 0
        while i <= 3:
            if vsub.degree[i] == 2:
                if adjacency_matrix_vsub.vertices[4][i]:
                    pos_count[vsub.vertices[i].index][50-1] += 1
                else:
                    pos_count[vsub.vertices[i].index][51-1] += 1
            else:
                pos_count[vsub.vertices[i].index][52-1] += 1
            i += 1
    elif nd == 10:
        pat_count[21-1] += 1
        vsub.degree2 = list(vsub.degree)
        i = 4
        while i >= 0:
            for n in vsub.neighbors[i]:
                vsub.degree2[n] += 1
            i -= 1
        i = 0
        while i <= 4:
            if vsub.degree2[i] == 7:
                pos_count[vsub.vertices[i].index][50-1] += 1
            elif vsub.degree2[i] == 8:
                pos_count[vsub.vertices[i].index][51-1] += 1
            else:
                pos_count[vsub.vertices[i].index][52-1] += 1
            i += 1
        return
    pat_count[22-1] += 1
    i = 0
    while i <= 4:
        pos_count[vsub.vertices[i].index][pattern_matching[2][vsub.degree[i]]] += 1
        i += 1
    
def disambiguate1317(pattern_matching, vsub.vertices, vsub.neighbors, adjacency_matrix_vsub.vertices, vsub.degree, pat_count, pos_count):
    d = vsub.degree[4]
    if d == 1 and vsub.degree[vsub.neighbors[4][0]] == 2:
        pat_count[13-1] += 1
        pos_count[vsub.vertices[4].index][25-1] += 1
        pos_count[vsub.vertices[3].index][26-1] += 1
        i = 0
        while i <= 2:
            if vsub.degree[i] == 2:
                pos_count[vsub.vertices[i].index][27-1] += 1
            else:
                pos_count[vsub.vertices[i].index][28-1] += 1
            i += 1
    elif d == 2 and adjacency_matrix_vsub.vertices[max(vsub.neighbors[4][0], vsub.neighbors[4][1])][min(vsub.neighbors[4][0], vsub.neighbors[4][1])]:
        pat_count[13-1] += 1
        pos_count[vsub.vertices[4].index][27-1] += 1
        i = 0
        while i <= 4:
            if vsub.degree[i] == 2:
                if i in vsub.neighbors[4]:
                    pos_count[vsub.vertices[i].index][27-1] += 1
                else:
                    pos_count[vsub.vertices[i].index][26-1] += 1
            else:
                pos_count[vsub.vertices[i].index][pattern_matching[2][vsub.degree[i]]] += 1
            i += 1
    else:
        pat_count[17-1] += 1
        if vsub.degree[4] == 2:
            if vsub.degree[vsub.neighbors[4][0]] == vsub.degree[vsub.neighbors[4][1]]:
                pos_count[vsub.vertices[4].index][37-1] += 1
                i = 0
                while i <= 3:
                    if vsub.degree[i] == 2:
                        pos_count[vsub.vertices[i].index][38-1] += 1
                    else:
                        pos_count[vsub.vertices[i].index][pattern_matching[2][vsub.degree[i]]] += 1
                    i += 1
            else:
                pos_count[vsub.vertices[4].index][38-1] += 1
                i = 0
                while i <= 3:
                    if vsub.degree[i] == 2:
                        if i in vsub.neighbors[4]:
                            pos_count[vsub.vertices[i].index][37-1] += 1
                        else:
                            pos_count[vsub.vertices[i].index][38-1] += 1
                    else:
                        pos_count[vsub.vertices[i].index][pattern_matching[2][vsub.degree[i]]] += 1
                    i += 1
        else:
            i = 0
            while i <= 4:
                if vsub.degree[i] == 2 :
                    if i in vsub.neighbors[3]:
                        pos_count[vsub.vertices[i].index][38-1] += 1
                    else:
                        pos_count[vsub.vertices[i].index][37-1] += 1
                else:
                    pos_count[vsub.vertices[i].index][pattern_matching[2][vsub.degree[i]]] += 1
                i += 1

def index_pattern(vsub.vertices, vsub.neighbors, vsub.length, adjacency_matrix_vsub.vertices, vsub.degree, des, pat_count, pos_count, patterns, power_table, power_differences_table):
    pattern_matching = patterns[des]
    if pattern_matching[0] == 2122:
        disambiguate2122(pattern_matching, vsub.vertices, vsub.neighbors, adjacency_matrix_vsub.vertices, vsub.degree, pat_count, pos_count)
    elif pattern_matching[0] == 1317:
        disambiguate1317(pattern_matching, vsub.vertices, vsub.neighbors, adjacency_matrix_vsub.vertices, vsub.degree, pat_count, pos_count)
    else:
        pat_count[pattern_matching[0]-1] += 1
        if pattern_matching[0] == 10:
            i = 0
            list_of_conflictual_vertices = []
            index_of_referee1 = -1
            index_of_referee2 = -1
            while i < vsub.length:
                if vsub.degree[i] == 2:
                    list_of_conflictual_vertices.append(i)
                else:
                    if index_of_referee1 == -1:
                        index_of_referee1 = i
                    else:
                        index_of_referee2 = i
                pos_count[vsub.vertices[i].index][pattern_matching[1][1]-1] += 1
                i += 1
            for index_of_conflictual_vertex in list_of_conflictual_vertices:
                if adjacency_matrix_vsub.vertices[index_of_conflictual_vertex][index_of_referee1] or adjacency_matrix_vsub.vertices[index_of_referee1][index_of_conflictual_vertex] or adjacency_matrix_vsub.vertices[index_of_referee2][index_of_conflictual_vertex] or adjacency_matrix_vsub.vertices[index_of_conflictual_vertex][index_of_referee2]:
                    pos_count[vsub.vertices[index_of_conflictual_vertex].index][pattern_matching[1][vsub.degree[index_of_conflictual_vertex]][0]-1] += 1
                else:
                    pos_count[vsub.vertices[index_of_conflictual_vertex].index][pattern_matching[1][vsub.degree[index_of_conflictual_vertex]][1]-1] += 1
        elif pattern_matching[0] == 12:
            degree_disambiguation(vsub.vertices, vsub.length, adjacency_matrix_vsub.vertices, 1, 2, vsub.degree, pattern_matching[1], pos_count)
        elif pattern_matching[0] == 18:
            degree_disambiguation(vsub.vertices, vsub.length, adjacency_matrix_vsub.vertices, 3, 1, vsub.degree, pattern_matching[1], pos_count)
        elif pattern_matching[0] == 26:
            degree_disambiguation(vsub.vertices, vsub.length, adjacency_matrix_vsub.vertices, 3, 1, vsub.degree, pattern_matching[1], pos_count)
        else:
            i = 0
            while i < vsub.length:
                pos_count[vsub.vertices[i].index][pattern_matching[1][vsub.degree[i]]-1] += 1
                i += 1
       
def calculate_des(vsub.index, vsub.length, vsub.neighbors, power_table):
    des = 0
    list_of_degrees = [0]*vsub.length
    i = vsub.length-1
    while i >= 0:
        temp = 0
        for neighbor in vsub.neighbors[i]:
            list_of_degrees[vsub.index[neighbor.index]] += 1
            temp += 1
        des += power_table[temp+list_of_degrees[i]]
        i -= 1
    return des

def extend_subgraph(list_neighbors, vsub, vext, v, k, pat_count, pos_count, patterns, power_table, power_differences_table):
    if vsub.length > 1:
        index_pattern(vsub.vertices, vsub.neighbors, vsub.length, adjacency_matrix_vsub.vertices, vsub.degree, des, pat_count, pos_count, patterns, power_table, power_differences_table)
        if vsub.length == k:
            return
    while vext:
        w = vext.pop()
        vext2 = list(vext)
        des2 = 0
        for u in list_neighbors[w.index]:
            if u.index >= v.index:
                if not vsub.index[u.index] == -1 :
                    vsub.neighbors[vsub.length].append(vsub.index[u.index])
                    vsub.degree[vsub.length] += 1
                    des2 += power_differences_table[vsub.degree[vsub.index[u.index]]]
                    vsub.degree[vsub.index[u.index]] += 1
                    adjacency_matrix_vsub.vertices[vsub.length][vsub.index[u.index]] = True
                elif not in_neighborhood_vsub.vertices(v, vsub.index, list_neighbors[u.index]):
                    vext2.append(u)
            else:
                break
        vsub.vertices[vsub.length] = w
        vsub.index[w.index] = vsub.length
        extend_subgraph(list_neighbors, vsub.vertices, vsub.neighbors, vsub.length+1, vsub.index, adjacency_matrix_vsub.vertices, vsub.degree, 
                        des+des2+power_table[vsub.degree[vsub.length]], vext2, v, k, pat_count, pos_count, patterns, power_table, power_differences_table)
        vsub.index[w.index] = -1
        for neighbor in vsub.neighbors[vsub.length]:
            adjacency_matrix_vsub.vertices[vsub.length][neighbor] = False
            vsub.degree[neighbor] -= 1
        vsub.degree[vsub.length] = 0
        vsub.neighbors[vsub.length] = []
        
def enumerate_from_v(v,pos_count,pat_count,vsub): 
    patterns = patterns_5.PATTERNS
    power_table = GLOBAL_POWER_TABLE
    power_differences_table = GLOBAL_POWER_DIFFERENCES_TABLE
    vsub.vertices[0] = v
    vsub.length = 1
    vsub.index[v.index] = 0
    vext = []
    for u in list_neighbors[v.index]:
	if u.index > v.index:
	    vext.append(u)
	else:
	    break
    if vext:
	extend_subgraph(list_neighbors, vsub, vext, v, k, pat_count, pos_count, patterns, power_table, power_differences_table)
  
  
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
    vsub = Vsub(len(g.vs))
    for v in vs:
      enumerate_from_v(v,pos_count,pat_count,vsub)
    return (pat_count, pos_count) 
 
def main():
    graph = create_graph(sys.argv[1])
    #graph = Graph.Formula("A-B, B-C, C-A, B-D")
    print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
    #couple = characterize_with_patterns(graph, 5)
    #print couple[0]
    #for co in couple[1]:
      #print co
    
#profile.run('main()')
main()

