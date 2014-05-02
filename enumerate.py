from igraph import Graph
import sys
import json
import profile

GLOBAL_POWER_TABLE = [0, 6, 36, 216, 1296]
GLOBAL_POWER_DIFFERENCES_TABLE = [6, 30, 180, 1080]

GLOBAL_PATTERNS = {
      12:(1, {1:1}), #1
      48:(2, {1:2, 2:3}), #2
      108:(3, {2:4}), #3
      84:(4, {1:5, 2:6}), #4
      234:(5, {1:7, 3:8}), #5
      294:(6, {1:9, 2:10, 3:11}), #6
      144:(7, {2:12}), #7
      504:(8,  {2:13,  3:14}),  #8
      864:(9,  {3:15}),  #9
      120:(10,  {1:16,  2:[17, 18]}),  #10
      1320:(11,  {1:19,  4:20}),  #11
      270:(12,  {1:[21, 22],  2:23,  3:24}),  #12
      330:(1317,  {1:25,  2:[26,  27],  3:28},  {1:36,  2:[37, 38],  3:39}),  #13 ou 17
      480:(14,  {1:29,  2:30,  3:31}),  #14
      1380:(15,  {1:32,  2:33,  4:34}),  #15
      180:(16,  {2:35}),  #16
      690:(18,  {1:40,  2:41,  3:[42, 43]}),  #18
      1590:(19,  {1:44,  2:45,  3:46,  4:47}),  #19
      1440:(20,  {2:48,  4:49}),  #20 
      540:(2122,  {2:[50,  51],  3:52},  {2:53,  3:54}),  #21 ou 22
      1950:(23,  {1:55,  3:56,  4:57}),  #23
      1800:(24,  {2:58,  3:59,  4:60}),  #24
      2700:(25,  {2:61,  4:62}),  #25
      900:(26,  {2:63,  3:[64,  65]}),  #26
      2160:(27,  {3:66,  4:67}),  #27
      3060:(28,  {2:68,  3:69,  4:70}),  #28
      4320:(29,  {3:71,  4:72}),  #29
      6480:(30,  {4:73})#30
     }

def create_graph(name):
    path = "./export_sample/"+name+"/friends.jsons"
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
  
def degree_disambiguation(vsub, length_vsub, adjacency_matrix_vsub, conflict, referee, degree_vsub, dic_ps, ps):
    i = 0
    list_of_conflictual_vertices = []
    index_of_referee = -1
    while i < length_vsub:
        if degree_vsub[i] == conflict:
            list_of_conflictual_vertices.append(i)
        elif degree_vsub[i] == referee:
            index_of_referee = i
            ps[vsub[i].index][dic_ps[referee]-1] += 1
        else:
            ps[vsub[i].index][dic_ps[degree_vsub[i]]-1] += 1
        i += 1
    for index_of_conflictual_vertex in list_of_conflictual_vertices:
        if adjacency_matrix_vsub[index_of_conflictual_vertex][index_of_referee] or adjacency_matrix_vsub[index_of_referee][index_of_conflictual_vertex]:
            ps[vsub[index_of_conflictual_vertex].index][dic_ps[degree_vsub[index_of_conflictual_vertex]][0]-1] += 1
        else:
            ps[vsub[index_of_conflictual_vertex].index][dic_ps[degree_vsub[index_of_conflictual_vertex]][1]-1] += 1

def calculate_neighbors_degree(v, neighbors_vsub, degree_vsub):
    result = 0
    for n in neighbors_vsub[v]:
        result += 1+degree_vsub[n]
    return result
      
def disambiguate2122(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pt, ps):
    if degree_vsub[4] == 2 and adjacency_matrix_vsub[max(neighbors_vsub[4][0], neighbors_vsub[4][1])][min(neighbors_vsub[4][0], neighbors_vsub[4][1])]:
        pt[21-1] += 1
        ps[vsub[4].index][51-1] += 1
        i = 0
        while i <= 3:
            if degree_vsub[i] == 2:
                ps[vsub[i].index][50-1] += 1
            else:
                ps[vsub[i].index][52-1] += 1
            i += 1
        return
    nd = calculate_neighbors_degree(4, neighbors_vsub, degree_vsub)
    if nd == 7:
        pt[21-1] += 1
        ps[vsub[4].index][50-1] += 1
        i = 0
        while i <= 3:
            if degree_vsub[i] == 2:
                if adjacency_matrix_vsub[4][i]:
                    ps[vsub[i].index][50-1] += 1
                else:
                    ps[vsub[i].index][51-1] += 1
            else:
                ps[vsub[i].index][52-1] += 1
            i += 1
    elif nd == 10:
        pt[21-1] += 1
        degree_vsub2 = list(degree_vsub)
        i = 4
        while i >= 0:
            for n in neighbors_vsub[i]:
                degree_vsub2[n] += 1
            i -= 1
        i = 0
        while i <= 4:
            if degree_vsub2[i] == 7:
                ps[vsub[i].index][50-1] += 1
            elif degree_vsub2[i] == 8:
                ps[vsub[i].index][51-1] += 1
            else:
                ps[vsub[i].index][52-1] += 1
            i += 1
        return
    pt[22-1] += 1
    i = 0
    while i <= 4:
        ps[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
        i += 1
    
def disambiguate1317(pattern_matching, vsub, neighbors_vsub, adjacency_matrix_vsub, degree_vsub, pt, ps):
    d = degree_vsub[4]
    if d == 1 and degree_vsub[neighbors_vsub[4][0]] == 2:
        pt[13-1] += 1
        ps[vsub[4].index][25-1] += 1
        ps[vsub[3].index][26-1] += 1
        i = 0
        while i <= 2:
            if degree_vsub[i] == 2:
                ps[vsub[i].index][27-1] += 1
            else:
                ps[vsub[i].index][28-1] += 1
            i += 1
    elif d == 2 and adjacency_matrix_vsub[max(neighbors_vsub[4][0], neighbors_vsub[4][1])][min(neighbors_vsub[4][0], neighbors_vsub[4][1])]:
        pt[13-1] += 1
        ps[vsub[4].index][27-1] += 1
        i = 0
        while i <= 4:
            if degree_vsub[i] == 2:
                if i in neighbors_vsub[4]:
                    ps[vsub[i].index][27-1] += 1
                else:
                    ps[vsub[i].index][26-1] += 1
            else:
                ps[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
            i += 1
    else:
        pt[17-1] += 1
        if degree_vsub[4] == 2:
            if degree_vsub[neighbors_vsub[4][0]] == degree_vsub[neighbors_vsub[4][1]]:
                ps[vsub[4].index][37-1] += 1
                i = 0
                while i <= 3:
                    if degree_vsub[i] == 2:
                        ps[vsub[i].index][38-1] += 1
                    else:
                        ps[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
                    i += 1
            else:
                ps[vsub[4].index][38-1] += 1
                i = 0
                while i <= 3:
                    if degree_vsub[i] == 2:
                        if i in neighbors_vsub[4]:
                            ps[vsub[i].index][37-1] += 1
                        else:
                            ps[vsub[i].index][38-1] += 1
                    else:
                        ps[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
                    i += 1
        else:
            i = 0
            while i <= 4:
                if degree_vsub[i] == 2 :
                    if i in neighbors_vsub[3]:
                        ps[vsub[i].index][38-1] += 1
                    else:
                        ps[vsub[i].index][37-1] += 1
                else:
                    ps[vsub[i].index][pattern_matching[2][degree_vsub[i]]] += 1
                i += 1

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
                    v, k, pt, ps, patterns, power_table, power_differences_table):
    if length_vsub > 1:
        index_pattern(vsub, neighbors_vsub, length_vsub, adjacency_matrix_vsub, degree_vsub, des, pt, ps, patterns, power_table, power_differences_table)
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
                        des+des2+power_table[degree_vsub[length_vsub]], vext2, v, k, pt, ps, patterns, power_table, power_differences_table)
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
    while i < length:
        ps.append(73*[0])
        i += 1
    list_neighbors = create_list_neighbors(graph)
    patterns = GLOBAL_PATTERNS
    power_table = GLOBAL_POWER_TABLE
    power_differences_table = GLOBAL_POWER_DIFFERENCES_TABLE
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
    #graph = Graph.Formula("A-B, B-C, C-A, B-D")
    print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
    couple = characterize_with_patterns(graph, 5)
    print couple[0]
    #for co in couple[1]:
      #print co
    
#profile.run('main()')
main()

