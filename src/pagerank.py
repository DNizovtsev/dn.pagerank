'''
Created on Jan 2, 2010

'''

class PageRank(object):
    
    def __init__(self,nodes_dict,nodes_num = None):
        '''
            iterable object in format:
        '''
        self.iterations = 100
        self.dampening_factor = 0.85
        self.scale_dampening_factor = False
        self.convergence = 0.000001
        self.link_sink_nodes = True
        
        self.nodes_dict = nodes_dict
        self.nodes_num = nodes_num
        if not self.nodes_num:
            self.nodes_num = len(self.nodes_dict)
        

    def calculate(self):
        # initialize the pagerank vector;
        source = {}
        for n_name in self.nodes_dict: source[n_name] = 1.0 / self.nodes_num

        dampening_value = (1.0 - self.dampening_factor)/self.nodes_num
        for i in xrange(self.iterations):
            dest = {}

            if self.scale_dampening_factor:
                average_rank = reduce(lambda s,el: s+el,source.values())
                average_rank *= dampening_value
            else:
                average_rank = 1.0 - self.dampening_factor
            
            for n_name in self.nodes_dict:        
                node = self.nodes_dict[n_name]
                dest.setdefault(n_name,0)
                
                if not node.isSink():
                    num_out_nodes = node.getNumNodes()
                    out_degree = source[n_name] / num_out_nodes 
                    
                    for n_to_name in node.dest_nodes:
                        dest.setdefault(n_to_name,0)
                        dest[n_to_name] +=  out_degree
                    
            sink_sum = 0
            for n_name in dest:
                dest[n_name] =  self.dampening_factor * dest[n_name] + dampening_value
                if self.link_sink_nodes and self.nodes_dict[n_name].isSink(): sink_sum += dest[n_name]


            if self.link_sink_nodes:
                sink_sum *= self.dampening_factor / self.nodes_num
                dest = dict([(k,v + sink_sum) for (k,v) in dest.items() ])
            
            error = reduce(lambda s,n_name: abs(dest[n_name] - source[n_name]),dest.keys()) / self.nodes_num
            
            source = self.normalize(dest)
            if error < self.convergence: break
              
            
        return source
        
    def normalize(self,vector):
        sum = reduce(lambda s,el: s+el,vector.values())
        #avoid division by zero
        if not sum: sum = 1
        return dict([(u,float(c)/sum) for (u,c) in vector.items( )])

        
class Node(object):
    
    def __init__(self,name,dest_nodes = None):
        self.name = name
        self.dest_nodes = dest_nodes
        if not self.dest_nodes:
            self.dest_nodes = []
        
    def getNumNodes(self):
        return len(self.dest_nodes)
        
    def isSink(self):
        if len(self.dest_nodes):
            return False
        else: 
            return True 
    
        
def edgesToNodesDict(edges):
    nodes = {}
     
    for ed in edges:
        n_from = ed[0]
        n_to = ed[1]
        if not nodes.has_key(n_from):
            nodes[n_from] = Node(n_from,[n_to])
        else:    
            nodes[n_from].dest_nodes.append(n_to)
        
        #add la    
        if not nodes.has_key(n_to):
            nodes[n_to] = Node(n_to)
    
    return nodes
        
    
if __name__ == '__main__':
    
#    nodes = edgesToNodesDict([('John','Joey'),
#                              ('John','James'),
#                              ('Joey','John'),
#                              ('James','Joey')
#                              ])
   
    nodes = edgesToNodesDict([('1','2'),
                              ('2','1'),
                              ('3','4'),
                              ('1','4')
                              ])

 
    for n in nodes:
        print n,nodes[n].dest_nodes
    pr = PageRank(nodes)
    print pr.calculate()