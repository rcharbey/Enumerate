import argparse
import sys
sys.path.append("../Methodes_graphe")
import methods_graph
import enumerate
import enumerate_mobystar

parser = argparse.ArgumentParser(description="main")
parser.add_argument('k', help="taille maximale des patterns a enumerer")
parser.add_argument('dossier', help="emplacement dans data de ego")
parser.add_argument('nom', help="nom de ego")
parser.add_argument('--option', '-o', nargs='+')
args = parser.parse_args()

if args.option == None :
    triple = methods_graph.create_graph(args.dossier, args.nom)
    graph = triple[0]
else:
    graph = enumerate_mobystar.create_graph_tel()
print "|N| = "+str(len(graph.vs)) +",  |E| = "+str(len(graph.es)) 
couple = enumerate.characterize_with_patterns(graph, int(args.k))
print couple[0]

