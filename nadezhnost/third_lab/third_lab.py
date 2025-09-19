class RadioStation:
    def __init__(self, name, frequency):
        self.name: str = name
        self.frequency: int = frequency


class Dispetcherskaya(RadioStation):
    def __init__(self, name, frequency):
        super().__init__(name, frequency)

    def zayavochka(self, name, frequency):
        zayavochka = dict()
        zayavochka.setdefault(name, frequency)

    def Cheking(self, list):
        pass


first = RadioStation("Boba Bebe", 31221)
second = RadioStation("Bebe", 31221)
zayava = Dispetcherskaya(second.name, second.frequency)
ALl_zayavas = dict()

