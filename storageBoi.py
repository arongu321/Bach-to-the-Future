class StorageBoi:
    def __init__(self, pricE = [None, None, None], urL = '', titlE = '',
    descriptioN = '', categorY = ''):
        self.price = pricE[0];
        self.currency = pricE[1];
        self.transaction = pricE[2];
        self.url = urL;
        self.title = titlE;
        self.description = descriptioN;
        self.category = categorY;
    
    def outlist(self):
        return [self.price, self.currency, self.transaction, self.title,
         self.description, self.url];