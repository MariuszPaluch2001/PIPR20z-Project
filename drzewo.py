class Drzewo(object):
    "Generic tree node."
    def __init__(self, pozycja, children=None, bicie=False):
        self.pozycja = pozycja
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    
  
    def puste(self):
        return len(self.children) == 0
    
    def add_child(self, node):
        self.children.append(node)

    def traverse(self, node):
        if node is not None:
            for child_node in node.children:
                self.traverse(child_node) 
        return

    # function to print all path from root 
    # to leaf in binary tree 
    def printPaths(self, root): 
        # list to store path 
        path = [] 
        self.printPathsRec(root, path, 0) 

    # Helper function to print path from root  
    # to leaf in binary tree 
    def printPathsRec(self, root, path, pathLen): 
        
        # Base condition - if binary tree is 
        # empty return 
        if root is None: 
            return
    
        # add current root's data into  
        # path_ar list 
        
        # if length of list is gre 
        if(len(path) > pathLen):  
            path[pathLen] = root.pozycja
        else: 
            path.append(root.pozycja) 
    
        # increment pathLen by 1 
        pathLen = pathLen + 1
    
        if len(root.children) == 0:
            
            # leaf node then print the list 
            self.printArray(path, pathLen) 
        else: 
            # try for left and right subtree 
            for child_node in root.children:
                self.printPathsRec(child_node, path, pathLen)
    
    # Helper function to print list in which  
    # root-to-leaf path is stored 
    def printArray(self, ints, len): 
        for p in ints[0 : len]: 
            print(p," ",end="") 
        print() 