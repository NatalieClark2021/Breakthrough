
class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1
    
    def printMoves(self):
        return self.value