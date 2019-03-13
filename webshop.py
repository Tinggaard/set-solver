class Vareliste:
    def add(self, v):
        self.varer.append(v)

class Webshop(Vareliste):
    def __init__(self, navn):
        self.navn = navn
        self.varer = []
    
    def search(self, text):
        out = []
        for vare in self.varer:
            if text in vare.navn:
                out.append(vare)
        return out

class Indkøbskurv(Vareliste):
    def __init__(self):
        self.varer = []
    
    def total(self, kupon=None):
        pris = 0
        for v in self.varer:
            pris += v.netPrice()
        if kupon != None:
            pris -= kupon.rabat
        return pris

class Vare:
    def __init__(self, navn, pris, rabat=0):
        self.navn = navn
        self.pris = pris
        self.rabat = rabat
    
    def __repr__(self):
        if self.rabat > 0:
            return "({}, {} kr., {} % off)".format(self.navn, self.pris, self.rabat)
        else:
            return "({}, {} kr.)".format(self.navn, self.pris)
    
    def netPrice(self):
        return self.pris - (self.rabat/100)*self.pris


class Rabatkupon:
    def __init__(self, rabat):
        self.rabat = rabat

shop = Webshop("Computer Bixen")

shop.add(Vare("laptop", 3000))
shop.add(Vare("Playstation 4", 2500))
shop.add(Vare("Playstation 3", 1500, 40))


vogn = Indkøbskurv()
for vare in shop.search("Playstation"):
    vogn.add(vare)

kupon = Rabatkupon(500)
print("Total: ", vogn.total(kupon))