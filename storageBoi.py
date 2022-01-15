class StorageBoi:
    def __init__(self, pricE = [None, None], urL = '', titlE = '', descriptioN = ''):
        self.price = pricE;
        self.url = urL;
        self.title = titlE;
        self.description = descriptioN;
    
    def outlist(self):
        return [self.price, self.title, self.description, self.url];