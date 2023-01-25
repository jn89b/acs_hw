import collections 
import numpy as np

class Node():
    def __init__(self, value, level):
        self.value = value
        self.left = None
        self.right = None
        self.level = level
        
    def insert_node(self, value, survive=False):
        
        level = self.level + 1
        if survive == True:
            self.left = Node(value, level)        
            self.right = Node(1-value, level)
            
        else:
            
            self.right = Node(value, level)
            self.left = Node(1-value, level)
            
        return 
        
if __name__ == '__main__':
    
    root = Node(0.5, 0)
    root.insert_node(0.5, survive=True)
                