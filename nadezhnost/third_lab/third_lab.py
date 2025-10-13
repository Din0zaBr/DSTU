class RadioStashion():
    def __init__(self, name, frequency):
        self.name = name
        self.frequency = frequency


class RadioStashionManager():
    def __init__(self):
        self.radio_list = []

    def add_radio(self, name, frequency):
        while True:
            try:
                self.radio_list.append(RadioStashion(name, int(frequency)))
            except:
                print('нужен формат int')
                frequency = input('Введите частоту: ')
            else:
                break

    def find_radio(self):
        frequency_to_names = {}
        for station in self.radio_list:
            frequency_to_names.setdefault(station.frequency, []).append(station.name)

        duplicates = {freq: names for freq, names in frequency_to_names.items() if len(names) > 1}

        if not duplicates:
            print('Норма')
            return

        for freq, names in sorted(duplicates.items()):
            print(f'Частота {freq}: {", ".join(names)}')

        return [(freq, names) for freq, names in duplicates.items()]


radio = RadioStashionManager()
radio.add_radio('Radio 1', 100)
radio.add_radio('Radio 2', 200)
radio.add_radio('Radio 3', 300)
radio.add_radio('Radio 4', 300)
radio.find_radio()
