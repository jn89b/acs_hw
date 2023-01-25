"""
Binary tree node class used for kill chain calculations
left is survival, right is killed, 
this is for independent events 
inspiration from https://www.educative.io/answers/binary-trees-in-python

Insert Node root with level and name

Use insert method and define the data, name, and survive
    - if survive is true then do the following:
        - check if left child exists
        - If it does then insert the data and name into the left child
        - check if right child exists
        - If it does then insert the 1-data and opposite_name into the RIGHT child
    - if survive is false then do the following:
        - check if right child exists
        - If it does then insert the data and name into the right child
        - check if left child exists
        - If it does then insert the 1-data and opposite_name into the LEFT child

"""
import numpy as np

class Node():
    
    def __init__(self, data, name, level):
        self.data = data
        self.level = level
        self.leftChild = None
        self.rightChild = None
        self.name = name

    def insert(self, data, name, survive=False):
        if self.data:
            
            current_level = self.level 
            
            if survive == True:
                #left side is survive, right side is killed
                opposite_name = "opposite_"+str(name)

                if self.leftChild:
                    self.leftChild.insert(data, name)                    
                    return                     

                else:
                    self.leftChild = Node(data, name, 
                                          self.level+1)
                    
                    if self.rightChild:
                        self.rightChild.insert(1-data, opposite_name)
                    
                    else:
                        self.rightChild = Node(1-data, opposite_name, 
                                               self.level+1)
                    return 
                
            else:
                #left side is survive, right side is killed

                if current_level+1 == self.level:
                    # print("current level", current_level)
                    return
                
                opposite_name = "opposite_"+str(name)
                print("inserting", data, name)
                print("opposite", opposite_name, 1-data)
            
                if self.rightChild:
                    print("child exists")

                    self.rightChild.insert(data, name)
                    return 
                    
                
                else:
                    print("new child")
                    self.rightChild = Node(data, name, self.level+1)
                    
                    if self.leftChild:
                        self.leftChild.insert(1-data, opposite_name)
                    
                    else:
                        self.leftChild = Node(1-data, opposite_name, 
                                               self.level+1)
                    return 
                
    def printTree(self):
        if self.leftChild:
            self.leftChild.printTree()
            print("left", self.leftChild.data)
            print("level", self.leftChild.level)
        if self.rightChild:
            self.rightChild.printTree()
            print("right", self.rightChild.data)
            print("level", self.rightChild.level)

        print("\n")

    def get_values(self):
        while self.leftChild:
            print("left values", self.leftChild.data)
            self = self.leftChild

    def get_chain(self, search_value, survive=False):
        """get the chain of values based on search value,
        if kill chain is true we look for the right child 
        if false we look for the left child"""
        
        values = []
        levels = []
        while self.data != search_value:
            if survive == False:
                values.append(self.rightChild.data)
                self = self.rightChild
                print("right", values)
                
            else:
                print(self.leftChild.data)
                values.append(self.leftChild.data)
                self = self.leftChild
                print("left", values)

            
        return np.prod(values)
                        
            
if __name__ == '__main__':
    
    #toy example from lecture
    
    #lets add stuff to the tree 
    ## This is the simple toy problem from the book
    root = Node(1.0,"root", 0) #defaults to killed
    print("\n")
    # root.insert(1.0) #defaults to killed
    root.insert(0.8, "p_k") #defaults to killed
    print("\n")
    root.insert(0.9, "p_a") #defaults to killed
    # print("\n")
    root.insert(0.6, "p_a") #defaults to killed
    root.insert(0.7, "p_b") #defaults to killed
    root.insert(0.3, "p_c") #defaults to killed
    
    # root.printTree()
    killed_value = root.get_chain(0.7, survive=True)
    root.get_values()
    
    
    #%% jammer active
    p_jammer_active = 1.0
    p_detection_of_ohiostan = 0.45
    p_russian_jammer_does_its_job = 0.2 #heard it sucks from reports
    p_russian_jammer_doesnt_do_its_job = 1.0 - p_russian_jammer_does_its_job
    
    hw_root = Node(p_jammer_active, "jammer_active", 0)
    hw_root.insert(p_detection_of_ohiostan, "detection_of_ohiostan")
    hw_root.insert(p_russian_jammer_does_its_job, "russian_jammer_does_its_job")
    
    blackjack_killed_p = hw_root.get_chain(p_russian_jammer_does_its_job, survive=False)
    print("blackjack killed", blackjack_killed_p)
    
    
    
    
    

