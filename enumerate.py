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
    self.adjacency_matrix = [[False]*5]*5
    

GLOBAL_POWER_TABLE = [0, 6, 36, 216, 1296]
GLOBAL_POWER_DIFFERENCES_TABLE = [6, 30, 180, 1080]
LIST_NEIGHBORS = []
PATTERNS = patterns_5.PATTERNS

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
           
def create_LIST_NEIGHBORS(graph):
    vs = graph.vs
    es = graph.es
    LIST_NEIGHBORS = []
    for v in vs:
        LIST_NEIGHBORS.append([])
    for e in es:
        LIST_NEIGHBORS[e.target].append(vs[e.source])
        LIST_NEIGHBORS[e.source].append(vs[e.target])
    for l in LIST_NEIGHBORS:
        l.sort(key =lambda vertex: vertex.index,  reverse = True)
    return LIST_NEIGHBORS  
  
def in_neighborhood_vsub(v, vsub, list_neighbors):
    for n in list_neighbors:
        if vsub.index[n.index] != -1:
            return True
    return False
  
def degree_disambiguation(vsub, conflict, referee, dic_pos_count, pos_count):
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
        if vsub.adjacency_matrix[index_of_conflictual_vertex][index_of_referee] or vsub.adjacency_matrix[index_of_referee][index_of_conflictual_vertex]:
            pos_count[vsub.vertices[index_of_conflictual_vertex].index][dic_pos_count[vsub.degree[index_of_conflictual_vertex]][0]-1] += 1
        else:
            pos_count[vsub.vertices[index_of_conflictual_vertex].index][dic_pos_count[vsub.degree[index_of_conflictual_vertex]][1]-1] += 1

def calculate_neighbors_degree(v, vsub):
    result = 0
    for n in vsub.neighbors[v]:
        result += 1+vsub.degree[n]
    return result
      
def disambiguate2122(pattern_matching, vsub, pat_count, pos_count):
    if vsub.degree[4] == 2 and vsub.adjacency_matrix[max(vsub.neighbors[4][0], vsub.neighbors[4][1])][min(vsub.neighbors[4][0], vsub.neighbors[4][1])]:
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
    nd = calculate_neighbors_degree(4, vsub)
    if nd == 7:
        pat_count[21-1] += 1
        pos_count[vsub.vertices[4].index][50-1] += 1
        i = 0
        while i <= 3:
            if vsub.degree[i] == 2:
                if vsub.adjacency_matrix[4][i]:
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
    
def disambiguate1317(pattern_matching, vsub, pat_count, pos_count):
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
    elif d == 2 and vsub.adjacency_matrix[max(vsub.neighbors[4][0], vsub.neighbors[4][1])][min(vsub.neighbors[4][0], vsub.neighbors[4][1])]:
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

def index_pattern(vsub, pat_count, pos_count):
    pattern_matching = patterns[des]
    if pattern_matching[0] == 2122:
        disambiguate2122(pattern_matching, vsub, pat_count, pos_count)
    elif pattern_matching[0] == 1317:
        disambiguate1317(pattern_matching, vsub, pat_count, pos_count)
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
                if vsub.adjacency_matrix[index_of_conflictual_vertex][index_of_referee1] or vsub.adjacency_matrix[index_of_referee1][index_of_conflictual_vertex] or vsub.adjacency_matrix[index_of_referee2][index_of_conflictual_vertex] or vsub.adjacency_matrix[index_of_conflictual_vertex][index_of_referee2]:
                    pos_count[vsub.vertices[index_of_conflictual_vertex].index][pattern_matching[1][vsub.degree[index_of_conflictual_vertex]][0]-1] += 1
                else:
                    pos_count[vsub.vertices[index_of_conflictual_vertex].index][pattern_matching[1][vsub.degree[index_of_conflictual_vertex]][1]-1] += 1
        elif pattern_matching[0] == 12:
            degree_disambiguation(vsub, 1, 2, pattern_matching[1], pos_count)
        elif pattern_matching[0] == 18:
            degree_disambiguation(vsub, 3, 1, pattern_matching[1], pos_count)
        elif pattern_matching[0] == 26:
            degree_disambiguation(vsub, 3, 1, pattern_matching[1], pos_count)
        else:
            i = 0
            while i < vsub.length:
                pos_count[vsub.vertices[i].index][pattern_matching[1][vsub.degree[i]]-1] += 1
                i += 1
       
def calculate_des(vsub):
    des = 0
    list_of_degrees = [0]*vsub.length
    i = vsub.length-1
    while i >= 0:
        temp = 0
        for neighbor in vsub.neighbors[i]:
            list_of_degrees[vsub.index[neighbor.index]] += 1
            temp += 1
        des += POWER_TABLE[temp+list_of_degrees[i]]
        i -= 1
    return des

def extend_subgraph(vsub, vext, v, pat_count, pos_count):
    if vsub.length > 1:
        index_pattern(vsub, pat_count, pos_count)
        if vsub.length == 5:
            return
    while vext:
        w = vext.pop()
        w_in_vsub = vsub.length
        vext2 = list(vext)
        des2 = 0
        for u in LIST_NEIGHBORS[w.index]:
            if u.index >= v.index:
                u_in_vsub = vsub.index[u.index]
                if u_in_vsub != -1 :
                    vsub.neighbors[w_in_vsub].append(u_in_vsub)
                    vsub.degree[w_in_vsub] += 1
                    des2 += POWER_DIFFERENCES_TABLE[vsub.degree[u_in_vsub]]
                    vsub.degree[u_in_vsub] += 1
                    vsub.adjacency_matrix[w_in_vsub][u_in_vsub] = True
                elif not in_neighborhood_vsub(v, vsub, LIST_NEIGHBORS[u.index]):
                    vext2.append(u)
            else:
                break
        vsub.vertices[w_in_vsub] = w
        vsub.index[w.index] = w_in_vsub
        vsub.length += 1
        modif_def = des2 + POWER_TABLE[vsub.degree[w_in_vsub]]
        vsub.des += modif_def
        extend_subgraph(vsub, vext2, v, pat_count, pos_count)
        vsub.des -= modif_def
        vsub.length -= 1
        vsub.index[w.index] = -1
        for neighbor in vsub.neighbors[w_in_vsub]:
            vsub.adjacency_matrix[w_in_vsub][neighbor] = False
            vsub.degree[neighbor] -= 1
        vsub.degree[w_in_vsub] = 0
        vsub.neighbors[w_in_vsub] = []
        
        
def enumerate_from_v(v,pos_count,pat_count,vsub):
    vsub.vertices[0] = v
    vsub.length = 1
    vsub.index[v.index] = 0
    vext = []
    for u in LIST_NEIGHBORS[v.index]:
        if u.index > v.index:
            vext.append(u)
        else:
            break
    if vext:
        extend_subgraph(vsub, vext, v, pat_count, pos_count)
  
def characterize_with_patterns(graph):
    vs = graph.vs
    length = len(vs)
    pat_count = 30*[0]
    pos_count = []
    i = 0
    while i < length:
        pos_count.append(73*[0])
        i += 1
    vsub = Vsub(len(graph.vs))
    for v in vs:
      enumerate_from_v(v,pos_count,pat_count,vsub)
    return (pat_count, pos_count) 
 
def main():
    #graph = create_graph(sys.argv[1])
    graph = Graph.Formula("A-B, B-C, C-A, B-D")
    global LIST_NEIGHBORS
    LIST_NEIGHBORS = create_LIST_NEIGHBORS(graph)
    print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
    couple = characterize_with_patterns(graph)
    print couple[0]
    #for co in couple[1]:
      #print co
    
#profile.run('main()')
main()

