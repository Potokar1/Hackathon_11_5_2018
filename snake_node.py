
# This class is an abstraction of the snake body nodes of a row and a col
class Snake_Node():
    # Create a tail node
    def __init__(self,row,col):
        self.row = row
        self.col = col

    # Used to check the value of the node [row,col]
    def get_node(self):
        return [self.row,self.col]
    # Change the row of the snake node
    def change_row(self,value):
        self.row += value
    # Change the col of the snake node
    def change_col(self,value):
        self.col += value
    # Return the row where the snake node is
    def get_row(self):
        return self.row
    # Return the col where the snake node is
    def get_col(self):
        return self.col
