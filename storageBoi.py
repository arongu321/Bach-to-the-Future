class StorageBoi:
    """
    This class will be used to store data of a single listing that was found.
    """
    def __init__(self, pricE = [None, None, None], urL = '', titlE = '',
    descriptioN = '', categorY = ''):
        """
        The price input will be in a list form where to first element is the
        float of the price, the second element will be the currency, USD or
        CAD, etc. And finally the third element will be the description of the
        transaction type.
        * Title = String
        * Price = [Price (float), 'currency'(string), 'Free, auction, contact,
         buy, or sell']
        * Description = string
        * Link = string
        """
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