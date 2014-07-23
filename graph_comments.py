import sys
import json
from igraph import *
import math

tab = [{"from":{"id":"152c8f29a5973494af4c54e8b7c6ae0baff18f20"},"time":1355756436000,"likes":[],"id":"15b0a584c03f810b7780762dd3b6072ad654d868"},
{"from":{"id":"0c67f4be284c7bdfdb3cb42a5ad2de06de4e24db"},"time":1355756475000,"likes":[],"id":"689b650df050a097e2e3f8840b143c8d7e218eaa"},
{"from":{"id":"48b256f0c281944daa4dd39e3964d1db4cc61d82"},"time":1355756504000,"likes":[],"id":"54bead3aa8a36e7073b4d95a5054d8a5bd517887"},
{"from":{"id":"2965291516ddd37337d057905437228ee3148c64"},"time":1355756586000,"likes":[],"id":"bc1119fa2a045b4de8597fa270f369bff54a56d0"},
{"from":{"id":"001d62ff4ef343bd09619b767451498f50ff2ec8"},"time":1355756608000,"likes":[],"id":"c91dcef2dcc20e4693dfd4f2d593cd949e2d4ad3"},
{"from":{"id":"3bdde45207a498d8198619b85752d342cc1aeaec"},"time":1355756638000,"likes":[],"id":"51718626c6d10e47254ba15574423a6ede0552c0"},
{"from":{"id":"370500e3b1b592aab6ebbf08fe35c63bc39375f4"},"time":1355756665000,"id":"4a8a1a07b8b1ea985b6eef60186e8a3b463657dd"},
{"from":{"id":"7ae5efbfecf8821b6087fc1b494403b407f55949"},"time":1355756697000,"likes":[],"id":"eabdd977d9352179cdaa29aad28be5f6bec7538c"},
{"from":{"id":"2d9a379c4e0a253e29aa2c901837385324dd30f9"},"time":1355756715000,"id":"87b9ddbff86ce436d9df82c6a0c2d6e4fc5f4eab"},
{"from":{"id":"591d5f40acbbcaa12d67000aad5c5b4e6d3a4edc"},"time":1355756781000,"likes":[],"id":"1d5c93ef6bfc5ab491afa185b8980512b1f59cdc"},
{"from":{"id":"e7a75a4167ab57522ecee88ee5b85721219c9744"},"time":1355756799000,"id":"1f4fbc2e91bb2e43fd61c99ae4d2cf2c84f1675d"},
{"from":{"id":"ee96363ca2f21d21e7a6fd043ac2bd1d4f6c0fe9"},"time":1355756856000,"likes":[],"id":"d29fd4bf91a11fff84f2a46748af090819d1d2fc"},
{"from":{"id":"0404777b15d82c38d005e352f59a87b45c98fa72"},"time":1355756871000,"id":"08cdf6309b5b98648820b4e71e5eb0801771c55a"},
{"from":{"id":"db39138dd30094884251ff6efc042eebb4f2d7b1"},"time":1355756897000,"id":"1e2400c656e2eaf967d6165ebd8c5dc9a876ecdb"},
{"from":{"id":"b078e0f85a16b2fe744dc4aafe3dc596623142a9"},"time":1355756944000,"likes":[],"id":"46b4920d72694259f7c64734a0e8fc6547541116"},
{"from":{"id":"2d32fe2d26208b09bb447f335924bf5ddf97aed2"},"time":1355757004000,"id":"ac48b7769695dd07c9223acae10e63444c14ba59"},
{"from":{"id":"fc5fb27a93a2f32a41d59890f568aa2a2b223dbe"},"time":1355757066000,"likes":[],"id":"0bd30aeb0a1fa56f9653344a3ff1ab4ae51104d7"},
{"from":{"id":"2913476bebd1e23d772f31d6cdc250d703508044"},"time":1355757094000,"id":"bbb1b06f2b063d6c72a967316a6110190d2139b7"},
{"from":{"id":"7904605783054b2be4587da440b0d874da2b01fa"},"time":1355757208000,"id":"4fb016cc3c346f4ba6a57d06d8b2397301f7f079"},
{"from":{"id":"a06af3e9e1926869ebb5162bfb49a8d4a2d6e2f3"},"time":1355757343000,"likes":[],"id":"874b270014e6a19ee4fede49c2e8ac20657df3d2"},
{"from":{"id":"bb3f9eadfbbf40bef27d1f3a8dadaee6aed47fcb"},"time":1355757354000,"id":"871802bb31a8309fbbd7c2b061c03b5aa7b5e238"},
{"from":{"id":"a627d169a5862a3710b90cfd665e3d8ef3b589ba"},"time":1355757389000,"likes":[],"id":"72b12c1c8f28759f7ea13974a3de10a2bf5db62b"},
{"from":{"id":"c7eb21698c6dea98144a8035e2a94840971843fb"},"time":1355757539000,"likes":[],"id":"4fb3355801b1c0a9d1f40efb910e52dd4a47ca75"},
{"from":{"id":"a3ee2532a3e162352843f24372b6a01157dcf984"},"time":1355757802000,"likes":[],"id":"a0e39683293b12b5935e8c5a520bc76954f59e87"},
{"from":{"id":"0d42b2188922574e0ef458a1e9c3188f30d0ef4c"},"time":1355758023000,"likes":[],"id":"b46aef3a3724004ac762da689579ff467563f7c3"},
{"from":{"id":"498d9e10d4905abc11b34a548d63672ea3dcfda1"},"time":1355758110000,"id":"5d64f799a9354d9835205143bb138a6394517e84"},
{"from":{"id":"03696b9b8fa84a51c7e32511d367029184238a23"},"time":1355758131000,"likes":[],"id":"85cd36b0d24e422befb8cfb941e54c1633b6646c"},
{"from":{"id":"f174564d5d7000128bbf4006b4dcbec1a5d0ffee"},"time":1355758317000,"likes":[],"id":"4e36254fa434e0361db4d5459ec318ad6ebe4ab7"},
{"from":{"id":"816382e303154a13e74be13ac2f31f6713215b41"},"time":1355758460000,"likes":[],"id":"4152b83436d55a54f3de79fd84d0baba5594243c"},
{"from":{"id":"e0e4e5c7fa69176a83a86160e5b7b1b8ec066363"},"time":1355759248000,"likes":[],"id":"6dd9c911c00515b6d122aca460e1a7a4619b15c0"},
{"from":{"id":"8b084d622adc49d3225d7ddb744aa0b81c4c023d"},"time":1355759342000,"id":"91c36493fe28b5c70dae979228068eefc0d6d78a"},
{"from":{"id":"001b18bf6156d518e6911c52fd512c17439a0bc7"},"time":1355759386000,"likes":[],"id":"37a54755a55bbe8e789110bc517adddb72bb4ee4"},
{"from":{"id":"926d0b3ef867e91f9009c15c2f2edabce9611098"},"time":1355759712000,"likes":[],"id":"70355c2d9ba39792765132922495be56b1793b90"},
{"from":{"id":"b80c464882a080ad586e6a2dbd87b31864ed4adf"},"time":1355759893000,"likes":[],"id":"243c074d9cfd7e90216aa0cf2c27b0dc97c0ebc6"},
{"from":{"id":"8c7e47fbc02f23412c068fb1d6e19c60482f7727"},"time":1355759910000,"likes":[],"id":"4b95428fd34a4e45c40228abd9f832352bc5337b"},
{"from":{"id":"0c5033d45690cfa107bba67b379c0dad74932dfd"},"time":1355760791000,"id":"e04d8f01cd74808bbbf66dd2143d59268c433c74"},
{"from":{"id":"0c580f5e527bbd590a036d5878bb2f59071a85cc"},"time":1355761055000,"likes":[],"id":"a2b0922b64188e06f9465c3e989cc918d6b403d2"},
{"from":{"id":"5116932ff6e647e0a2f94c5d944307b49a121928"},"time":1355761089000,"id":"6d320a6ca43efe657c09c96bc2337bb3aab240c9"},
{"from":{"id":"73a01887c3c168fad7b534b313e51717b9a1624d"},"time":1355761108000,"likes":[],"id":"9280bc57e3f55e8de8855b042675862e36d5324"},
{"from":{"id":"e760b153a74ba95767d429bf0d2a72a635507001"},"time":1355762575000,"id":"5ee7100b29809755b8b339eabb0c34bb8d3f6475"},
{"from":{"id":"076238fae14ca54ef61c8cacdd877fe43c3240ad"},"time":1355762588000,"id":"248e4322840f0bde682ea0c935cda5dab7c7826c"},
{"from":{"id":"7a80ea22eee7e6d79ecc41714ccb18c7464960bd"},"time":1355763257000,"likes":[],"id":"261747d9221e38c071ae15c6d871bbdbebc97c38"},
{"from":{"id":"8bedadc98cd0b673717a8aed7a409fbd081dba70"},"time":1355764612000,"likes":[],"id":"644dfb0e24864628f5cbefdcb30a150bf2e212e2"},
{"from":{"id":"f908416a2e02873f31bd0c686b9b7a67b9bbc3f6"},"time":1355766875000,"id":"b95402acccdde6741c47b16790dd9ac9e02a73d8"},
{"from":{"id":"5d12d8635b0ed6f7ed5b104ba374e5077e37c58b"},"time":1355766977000,"id":"88bbdc3672e247bd68135bdcff8f5e3aef7f9f19"},
{"from":{"id":"bac55f1ca8fed2a802e707062b82a13e20ba605e"},"time":1355767237000,"likes":[],"id":"0c8867d1595a336cce8059f414831a1db01e5b5c"},
{"from":{"id":"c4512b361877726136e5c01ac8e7d1b91028d212"},"time":1355767528000,"id":"b5c8a222825f1e34e76f3958b35f5338bf05370a"},
{"from":{"id":"9eda846ef6ed1c0adf98ec2c140d72abc8ca749c"},"time":1355769986000,"likes":[],"id":"20f67b665b2e615023f3924175db0ff07cb5fa97"},
{"from":{"id":"7fb9cbf7da3db74d4539bc5bc8f3c738c38222bd"},"time":1355770766000,"id":"0d67e12f1e815f1c68e37ea4132adbb8eb635750"},
{"from":{"id":"cdbe975f981d839f2087bc994c5b97e5645b59c9"},"time":1355770931000,"id":"5a775d032e479f111a9c0e824123176a620e8fb4"},
{"from":{"id":"7ba60068f6db247af39cd57a00d20b95eb3d2e69"},"time":1355772084000,"likes":[],"id":"b2a9fb88ac2f659253700728d511c4ec89f7c6b9"},
{"from":{"id":"d95b6b62ebba8473b697c3cfcc9e1ae55accf25f"},"time":1355772827000,"id":"3bd8227d9d15e21487b6a31c52c2c2c067173fb0"},
{"from":{"id":"d5a9c7e1eb1ce43838aab20a8a6fbb042ab947ed"},"time":1355774949000,"id":"9cf7fcf1a7c0399ec5557d3568c4cba8c4f55991"},
{"from":{"id":"a06527a374c10fa9f67b17931da62f3d1185fdb2"},"time":1355781826000,"likes":[],"id":"3f583b7f25f2122c39c6fe775cc586973dc35dc5"},
{"from":{"id":"de4ff9ecb743cf9904a1964d9b9c9810632d9a82"},"time":1355806063000,"id":"aaedbcee4d772d5a575b12a338a30fe7c6912452"},
{"from":{"id":"d4f7e537151e791477a74d3cfaf4fea172848c47"},"time":1355810146000,"id":"ae77a22978beda81495f74367216f23a8835b9c6"},
{"from":{"id":"a2584f4afed839b8e9c2478d6562f162c74e5e98"},"time":1355810996000,"id":"f95a29ae0210d3b4c1703a3f9fd3af65d4eb852a"},
{"from":{"id":"8d11c7c8b5d3f46bcc1727c5a0088350e3ec2fac"},"time":1355823095000,"likes":[],"id":"bd14d5c5512cbabc6066c76afd1a2094d23947c6"},
{"from":{"id":"8b0ecb321bbab7ce71e2ae4c33e9f811a09d451b"},"time":1355833363000,"likes":[],"id":"507da7b4ba6874255d78eec6ad96a4f0b7331028"},
{"from":{"id":"3b25289f45d0dc968fa40174a04f0b52cad21e18"},"time":1355862113000,"id":"15dd64577b1e24320773533e0e6639e2f7c1785d"},
{"from":{"id":"0e8f104e2fccbe238f4f09556111d31b6327a9c8"},"time":1355930609000,"likes":[],"id":"c9f13a6846045e7be8e221305998f13801da6dc3"},
{"from":{"id":"ac3c7fb449620e57f608eb8755b03e20ee5e4804"},"time":1356014044000,"id":"4b3a25cfc2523c3e9db76679aa78196a34e66482"},
{"from":{"id":"06931fe98aca5acefd40d97ad4c3d60f8554f2a0"},"time":1356101942000,"id":"7bd40e316a723e1f78248643bc33c5e0f5ba9956"},
{"from":{"id":"3785c15fb9474bd320d417b66721877948259fa9"},"time":1356297289000,"likes":[],"id":"4f708ab1efa16287be7b639e7637aab004062239"},
{"from":{"id":"87c52d6d32af15b23878fdab06b8cd7d2c375be6"},"time":1356388430000,"likes":[],"id":"a733ce4289f25b14c9b5243cb963307ffc0c17a1"},
{"from":{"id":"2fe844519d9e8ad08d221d20c9df90506b8ca4cf"},"time":1357695779000,"likes":[],"id":"8d307f7dce5712e9973c8c7a45f480a13821c74e"}
]

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
        for tt in tab:
            if tt["from"]["id"] == jr["id"]:
                print "yaaaaaaaaaaaa"
            else:
                print tt["from"]["id"]
        if not jr["id"] in vertex_to_index:
            vertex_to_index[jr["id"]] = nb_of_vertices
            index_to_vertex[nb_of_vertices] = jr["id"]
            index_to_graph_in[nb_of_vertices] = 0
            nb_of_vertices += 1
        for neighbor in jr["mutual"]:
            if not neighbor["id"] in vertex_to_index:
                vertex_to_index[neighbor["id"]] = nb_of_vertices
                index_to_vertex[nb_of_vertices] = neighbor["id"]
                index_to_graph_in[nb_of_vertices] = 0
                nb_of_vertices += 1
            if vertex_to_index[jr["id"]] < vertex_to_index[neighbor["id"]]:
                dict_of_edges[(vertex_to_index[jr["id"]], vertex_to_index[neighbor["id"]])] = [0,0]      
    f.close()
    path = "./data/"+folder+"/"+name+"/statuses.jsons"
    f = open(path, 'r')
    nb_comments_per_alter = []
    nb_comments = 0
    for line in f:
        nb_comments += 1
        jr = json.loads(line)
        if jr["from"]["id"] != name:
            continue
        if "comments" in jr:
            list_current_com = []
            for v in vertex_to_index:
                nb_comments_per_alter.append(0)
            for comment in jr["comments"]:
                commenter = comment["from"]["id"]
                if commenter != name :
                    if not commenter in vertex_to_index:
                        nb_comments_per_alter.append(0)
                        vertex_to_index[commenter] = nb_of_vertices
                        index_to_vertex[nb_of_vertices] = commenter
                        index_to_graph_in[nb_of_vertices] = 1
                        nb_of_vertices += 1
                    else:
                        nb_comments_per_alter[vertex_to_index[commenter]] += 1
                        if index_to_graph_in[vertex_to_index[commenter]] == 0:
                            index_to_graph_in[vertex_to_index[commenter]] = 3
            for comment in jr["comments"]:
                if not comment["from"]["id"] == name : 
                    for comment_second in jr["comments"]:
                        if not comment_second["from"]["id"] == name:
                            id_comment = vertex_to_index[comment["from"]["id"]]
                            id_second = vertex_to_index[comment_second["from"]["id"]]
                            if id_comment < id_second:
                                if (id_comment, id_second) not in dict_of_edges:
                                    dict_of_edges[(id_comment, id_second)] = [1,1]
                                else:
                                    if dict_of_edges[(id_comment, id_second)][0] == 0:
                                        dict_of_edges[(id_comment, id_second)][0] = 3
                                    dict_of_edges[(id_comment, id_second)][1] += 1
        #if "likes" in jr:
            #for like in jr["likes"]:
                #if not like["id"] == name:
                    #if not like["id"] in vertex_to_index:
                        #nb_comments_per_alter.append(0)
                        #vertex_to_index[like["id"]] = nb_of_vertices
                        #index_to_vertex[nb_of_vertices] = like["id"]
                        #index_to_graph_in[nb_of_vertices] = 2
                        #nb_of_vertices += 1
                    #else:
                        #if index_to_graph_in[vertex_to_index[like["id"]]] == 0:
                            #index_to_graph_in[vertex_to_index[like["id"]]] = 4
                        #elif index_to_graph_in[vertex_to_index[like["id"]]] == 1:
                            #index_to_graph_in[vertex_to_index[like["id"]]] = 5
                        #elif index_to_graph_in[vertex_to_index[like["id"]]] == 3:
                            #index_to_graph_in[vertex_to_index[like["id"]]] = 6
            #for like in jr["likes"]:
                #if not like["id"] == name:
                    #for like_second in jr["likes"]:
                        #if not like_second["id"] == name:
                            #id_like = vertex_to_index[like["id"]]
                            #id_second = vertex_to_index[like_second["id"]]
                            #if id_like < id_second:
                                #if (id_like, id_second) not in dict_of_edges:
                                    #dict_of_edges[(id_like, id_second)] = [2,1]
                                #else:
                                    #if dict_of_edges[(id_like, id_second)][0] == 0:
                                        #dict_of_edges[(id_like, id_second)][0] = 4
                                    #elif dict_of_edges[(id_like, id_second)][0] == 1:
                                        #dict_of_edges[(id_like, id_second)][0] = 5
                                    #elif dict_of_edges[(id_like, id_second)][0] == 3:
                                        #dict_of_edges[(id_like, id_second)][0] = 6                                       
    f.close()
    graph = Graph(dict_of_edges.keys())
    compteur = 0
    for v in graph.vs:
        if index_to_graph_in[v.index] == 1:
            compteur += 1
            print index_to_vertex[v.index],
            print " - ",
            print v.degree()
    print compteur
    return (graph, index_to_graph_in, dict_of_edges, index_to_vertex)
    
    
triple = create_graph(sys.argv[1], sys.argv[2])
graph = triple[0]
index_to_graph_in = triple[1]
dict_of_edges = triple[2]
index_to_vertex = triple[3]

layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**2.5)

color_dict_vertices = ["lightblue", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "violet", "limegreen", "rgba(0,0,0,0)", "black"]
color_dict_edges = ["darkblue", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "darkviolet", "darkgreen", "rgba(0,0,0,0)", "black"]

plot(graph,layout=layout, vertex_color = [color_dict_vertices[index_to_graph_in[graph_in]] for graph_in in index_to_graph_in], 
     edge_color = [color_dict_edges[dict_of_edges[(e)][0]] for e in dict_of_edges], vertex_size = 10)
     
color_dict_vertices = ["rgba(0,0,0,0)", "lightsalmon", "rgba(0,0,0,0)", "violet", "rgba(0,0,0,0)", "darkorange", "black"]
color_dict_edges = ["rgba(0,0,0,0)", "darkred", "rgba(0,0,0,0)", "darkviolet", "rgba(0,0,0,0)", "orangered", "black"]

for e in graph.es:
    e["width"] = 1+math.log(1+dict_of_edges[e.tuple][1])
     
plot(graph,layout=layout, vertex_color = [color_dict_vertices[index_to_graph_in[graph_in]] for graph_in in index_to_graph_in], 
edge_color = [color_dict_edges[dict_of_edges[(e)][0]] for e in dict_of_edges], vertex_size = 10)

#color_dict_vertices = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "khaki", "rgba(0,0,0,0)", "limegreen", "darkorange", "black"]
#color_dict_edges = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "gold", "rgba(0,0,0,0)", "darkgreen", "orangered", "black"]

#for e in graph.es:
    #e["width"] = 1
    
#plot(graph,layout=layout, vertex_color = [color_dict_vertices[index_to_graph_in[graph_in]] for graph_in in index_to_graph_in], 
#edge_color = [color_dict_edges[dict_of_edges[(e)][0]] for e in dict_of_edges], vertex_size = 10)
        
        
#Super families Milo
#David.o.fourquet@gmail.com
