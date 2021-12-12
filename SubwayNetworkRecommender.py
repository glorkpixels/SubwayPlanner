from pyvis import network as net
from IPython.core.display import display, HTML
import networkx as nx
from networkx.algorithms.distance_measures import center

import matplotlib.pyplot as plt
G=net.Network(height='1800px', width='100%',heading='')
Gx = nx.Graph()

linenames = []
linenext = []
linesalll = []

with open('Vienna subway.csv') as f:
    for line in f:
        #print(line)
        parsed = line.split(";")
        if(parsed[0] != "Start"):
            linenames.append(parsed[0])
            linenext.append(parsed[1])
            linesalll.append(parsed[0])
            linesalll.append(parsed[1])

listofstop = list(dict.fromkeys(linesalll))  
print("Total Number of Stops: " + str(len(listofstop)))    

for i in listofstop:
    #print(i)
    G.add_node(i)
    Gx.add_node(i)

for i in range(len(linenames)):
    G.add_edge(linenames[i], linenext[i], weight = 1)
    Gx.add_edge(linenames[i], linenext[i], weight = 1)
            
            

print("----------------------------------------------")
print("PRE PROCESSED METRO GRAPH")
print("Diamer:" + str(nx.diameter(Gx)))
print("Radius:" + str(nx.radius(Gx)))
print("Periphery:" +str(nx.periphery(Gx)))
print("Center:" +str(nx.center(Gx)))

Centernode = nx.center(Gx)
G.show('mygraph.html')
display(HTML('mygraph.html'))

print("Average shortest path: "+ str(nx.average_shortest_path_length(Gx)))

print("----------------------------------------------")
aver = int(nx.average_shortest_path_length(Gx))

pos = nx.spring_layout(Gx)

c = center(Gx)

        
propsedlinestops = []

for i in listofstop:
    if(i != Centernode):
        #print(nx.shortest_path_length(Gx, source="Schwedenplatz", target=i))
        
        distancefromcenter = nx.shortest_path_length(Gx, source=Centernode[0], target=i)
        
        if distancefromcenter  == aver-2:
            propsedlinestops.append(i)

         
lenx = len(propsedlinestops)

for x in range(lenx-1):
    Gx.add_edge(propsedlinestops[x], propsedlinestops[x+1], weight = 1)
    G.add_edge(propsedlinestops[x], propsedlinestops[x+1], weight = 1)
    
         
        
    
Gx.add_edge(propsedlinestops[lenx-1], propsedlinestops[0], weight = 1)
G.add_edge(propsedlinestops[lenx-1], propsedlinestops[0], weight = 1)

nx.draw_networkx_nodes(Gx, pos, nodelist=set(Gx.nodes)-set(c))
nx.draw_networkx_edges(Gx, pos)
nx.draw_networkx_nodes(Gx, pos, nodelist=c, node_color='r')

nx.draw_networkx_nodes(Gx, pos, nodelist=propsedlinestops, node_color='g')
nx.draw_networkx_labels(Gx, pos)

print("----------------------------------------------")
print("PROCESSED METRO GRAPH")
print("Diamer:" + str(nx.diameter(Gx)))
print("Radius:" + str(nx.radius(Gx)))
print("Periphery:" +str(nx.periphery(Gx)))
print("Center:" +str(nx.center(Gx)))
print("Average shortest path: "+ str(nx.average_shortest_path_length(Gx)))

print("----------------------------------------------")


print("New metro line proposed: \n")
for i in propsedlinestops:
    print(i) 
    print("|")
    print("v")
print(propsedlinestops)
plt.show()

G.show('mygraph.html')
display(HTML('mygraph.html'))
