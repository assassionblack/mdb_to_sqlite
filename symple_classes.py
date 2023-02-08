class Tovar:
    def __init__(self, tovar):
        (self.id, self.magazine, self.opisanie, self.kod, self.tsena,
         self.razmery, self.category, self.raspr, self.firm) = tovar


class Magazine:
    def __init__(self, magazine):
        (self.id, self.magazine) = magazine


class Raspr:
    def __init__(self, raspr):
        (self.id, self.raspr_flag) = raspr


class Category:
    def __init__(self, category):
        (self.id, self.category) = category


class CatInMag:
    def __init__(self, cat_in_mag):
        (self.id, self.cat, self.mag) = cat_in_mag
