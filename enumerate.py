from igraph import *
import sys
sys.path.append("../Methodes_graphe")
import methods_graph

Patterns = {
           "[2, 2]":(1,{2:1}),#1
           "[3, 3, 4]":(2,{3:2,4:3}),#2
           "[6, 6, 6]":(3,{6:4}),#3
           "[3, 3, 5, 5]":(4,{3:5,5:6}),#4
           "[4, 4, 4, 6]":(5,{4:7,6:8}),#5
           "[4, 7, 7, 8]":(6,{4:9,7:10,8:11}),#6
           "[6, 6, 6, 6]":(7,{6:12}),#7
           "[8, 8, 10, 10]":(8, {8:13, 10:14}), #8
           "[12, 12, 12, 12]":(9, {12:15}), #9
           "[3, 3, 5, 5, 6]":(10, {3:16, 5:17, 6:18}), #10
           "[5, 5, 5, 5, 8]":(11, {5:19, 8:20}), #11
           "[3, 4, 4, 6, 7]":(12, {3:21, 4:22, 6:23, 7:24}), #12
           "[3, 6, 7, 7, 9]":(13, {3:25, 6:26, 7:27, 9:28}), #13
           "[4, 4, 8, 9, 9]":(14, {4:29, 8:30, 9:31}), #14
           "[5, 5, 8, 8, 10]":(15, {5:32, 8:33, 10:34}), #15
           "[6, 6, 6, 6, 6]":(16, {6:35}), #16
           "[4, 6, 7, 7, 8]":(17, {4:36, 6:37, 7:38, 8:39}), #17
           "[4, 8, 10, 11, 11]":(18, {4:40, 8:41, 10:42, 11:43}), #18
           "[5, 9, 9, 11, 12]":(19, {5:44, 9:45, 11:46, 12:47}), #19
           "[8, 8, 8, 8, 12]":(20, {8:48, 12:49}), #20
           "[7, 7, 8, 10, 10]":(21, {7:50, 8:51, 10:52}), #21
           "[8, 8, 8, 9, 9]":(22, {8:53, 9:54}), #22
           "[5, 13, 13, 13, 14]":(23, {5:55, 13:56, 14:57}), #23
           "[9, 9, 12, 12, 14]":(24, {9:58, 12:59, 14:60}), #24
           "[10, 10, 10, 14, 14]":(25, {10:61, 14:62}), #25
           "[8, 11, 11, 12, 12]":(26, {8:63, 11:64, 12:65}), #26
           "[13, 13, 13, 13, 16]":(27, {13:66, 16:67}), #27
           "[10, 14, 14, 16, 16]":(28, {10:68, 14:69, 16:70}), #28
           "[15, 15, 18, 18, 18]":(29, {15:71, 18:72}), #29
           "[20, 20, 20, 20, 20]":(30, {20:73})}#30
  
def inNeighborhoodVsub(listNeighbors):
    for v in listNeighbors:
        if v["in_gsub"] == True:
            return True 
    return False
    
def Index_Pattern(gsub,pt,ps):
    #print "apres : " + str(gsub)
    degree_combination = methods_graph.calculate_degree_combination(gsub) 
    patternsMatching = Patterns[str(degree_combination)]
    pt[patternsMatching[0]-1] += 1
    for v in gsub.vs:
        ps[v["id_g"]][patternsMatching[1][v["neighbor_degree"]]-1] += 1
    
def Extend_Subgraph(gsub, listNeighbors, v_ext, v, k, pt, ps):
    if len(gsub.es) > 0:
        Index_Pattern(gsub, pt, ps)
    if len(gsub.vs) == k:
        return
    while v_ext:
        w = v_ext.pop()
        w['id_sub'] = len(gsub.vs)
        gsub.add_vertex(name = w['name'])
        gsub.vs[len(gsub.vs)-1]['id_g'] = w.index
        v_ext_2 = set(v_ext)
        neighbors = w.neighbors()
        for u in neighbors:
            if u.index <= v.index:
                if u['id_sub'] != -1:
                    gsub.add_edge(u['id_sub'], w['id_sub'])
                elif not inNeighborhoodVsub(listNeighbors[u.index]):
                    v_ext_2.add(u)
            else:
                break
        w['in_gsub'] = True
        Extend_Subgraph(gsub, listNeighbors, v_ext_2, v, k, pt, ps)
        gsub.delete_vertices(len(gsub.vs)-1)
        w['in_gsub'] = False
        w['id_sub'] = -1
  
def CharacterizeWithPatterns(g,k):
    Pt = 30*[0]
    Ps = []
    for v in g.vs:
        v['id_sub'] = -1
        v['in_gsub'] = False
        Ps.append(73*[0])
    listNeighbors = methods_graph.create_list_neighbors(g)
    for v in g.vs:
        Vext = []
        for u in listNeighbors[v.index]:
            if u.index > v.index:
                Vext.append(u)
            else:
                break
        if Vext:
            gsub = Graph.Formula()
            v['id_sub'] = 0
            gsub.add_vertex(name = v['name'])
            gsub.vs[0]['id_g'] = v.index
            v['in_gsub'] = True
            Extend_Subgraph(gsub, listNeighbors, Vext, v, k, Pt, Ps)
            g.vs[v.index]['in_gsub'] = False
            g.vs[v.index]['id_sub'] = -1
    return (Pt,Ps) 

print CharacterizeWithPatterns(Graph.Formula("A-B, A-C, A-D, C-D, C-E"), 5)[0]