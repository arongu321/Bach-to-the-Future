class StorageBoi:
    def __init__(self, pricE = [None, None], urL = '', titlE = '',
    descriptioN = '', categorY = ''):
        self.price = pricE;
        self.url = urL;
        self.title = titlE;
        self.description = descriptioN;
        self.category = categorY;
    
    def outlist(self):
        return [self.price, self.title, self.description, self.url];