class Matrix:
    def __init__(self, len_matrix):
        self.matrix = [[0 for _ in range(len_matrix)] for _ in range(len_matrix)]

    def add(self, i, j, len_dug):
        self.matrix[i - 1][j - 1] = len_dug

    def get(self,i,j):
        return self.matrix[i - 1][j - 1]

    def display(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i])