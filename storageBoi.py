class StorageBoi:
    def __init__(self, price = None, urL = '', titlE = '', descriptioN = ''):
        self.price = price;
        self.url = urL;
        self.title = titlE;
        self.description = descriptioN;
    
    def outlist(self):
        return [self.price, self.title, self.description, self.url];