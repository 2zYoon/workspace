class DWedge:
    def __init__(self, weight, nodes=[]):
        self.weight = weight
        self.nodes = nodes
    
    def __eq__(self, other):
        return self is other

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def get_opposite(self, node):
        if self.nodes[0] == node:
            return self.nodes[1]
        else:
            return self.nodes[0]


class DWnode:
    ##########
    # MASICS #
    ##########

    def __init__(self, name="", weight=1):
        self.weight = weight
        self.edges = []
        self.name = name 

        self.callid = 0

    def __eq__(self, other):
        return self is other

    def __str__(self):
        return (self.name).strip()

    def __repr__(self):
        return (self.name).strip()

    ####################
    # FOR INTERNAL USE #
    ####################

    # internal_is_having_edge: returns True if I have the given edge, otherwise False
    def internal_is_having_edge(self, edge):
        found = False
        for e in self.edges:
            if e == edge:
                found = True
                break
        
        return found

    # internal_get_opposite: returns the opposite node, connected by the given edge
    #                        returns None if failed (e.g., the given edge is invalid)
    def internal_get_opposite(self, edge):
        # first check if the edge is connected to me
        if not self.internal_is_having_edge(edge):
            return None
        
        return edge.get_opposite(self)


    # internal_get_edge_from_node: returns edge from the given node
    #                              if the node is not directly connected, returns None
    def internal_get_edge_from_node(self, node):
        ret = None
        for e in self.edges:
            tmp = self.internal_get_opposite(e)
            if tmp == node:
                ret = tmp
                break
        
        return ret

    # internal_append_edge: adds an edge to self.edges list
    #                       returns nothing
    def internal_append_edge(self, edge):
        self.edges.append(edge)

    # internal_apply: applies a function to all node connected to this
    def internal_apply(self, func, callid):
        if self.callid != callid:
            return
        self.callid += 1
        func(self)

        for e in self.edges:
            self.internal_get_opposite(e).internal_apply(func, callid)



    #############
    # INTERFACE #
    #############

    # connect: connects to node, creating/updating an edge 
    #          self-connection is not allowed, failing silently
    def connect(self, node, weight=1):
        if self == node:
            return

        edge = self.internal_get_edge_from_node(node)

        # already connected, just update the weight
        if edge != None:
            edge.set_weight(weight)    

        # not connected yet, create an edge and connect
        else:
            edge = DWedge(weight, [self, node])
            self.internal_append_edge(edge)
            node.internal_append_edge(edge)

    # disconnect: disconnects from the node, removing the corresponding edge
    #             returns 0 if succeed, non-zero integer otherwise 
    def disconnect(self, node):
        edge = self.internal_get_edge_from_node(node)

        # not connected, do nothing
        if edge == None:
            return 1

        # connected well, disconnect
        else:
            # remove the edge from other's edge list
            # remove the edge from my edge list
            # remove the edge itself
            pass

    # neighbors: returns a list of neighbor nodes
    def neighbors(self):
        ret = []
        for e in self.edges:
            ret.append(self.internal_get_opposite(e))
        return ret

    # print_info: prints several information about the node
    #             including info about itself, neighbors, edges, etc.
    def print_info(self):
        print("[%s]\nweight: %f" % (str(self), self.weight))
        print("connection:")
        for n in self.neighbors():
            print("\t- %s is connected with weight %f" % (str(n), self.internal_get_edge_from_node(n).weight))


def tutorial():
    a = DWnode("Node 1", weight=133)
    b = DWnode("Node 2", weight=5.732)
    c = DWnode("Node 3", weight=335)
    d = DWnode("Node 4")
    #print(a == a, a==b)
    #print(a, b)
    a.connect(b, 10.4)
    b.connect(c, 125)
    a.connect(c, 1006)
    d.connect(a, 333)
    print(a.neighbors())
    print(b.neighbors())
    a.print_info()

    a.internal_apply(print, a.callid)

#tutorial()
