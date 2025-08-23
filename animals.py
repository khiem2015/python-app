class animals:
    def __init__(self, lion, tiger, monkey ):
        self.lion = lion
        self.tiger = tiger
        self.monkey = monkey
    class animal_list:
        def __init__(self,name, species, sound):
            self.name = name
            self.species = species
            self.sound = sound

        def sort_zoo(self,animal_list, asc=True):
            self.animal_list.sort(reversed=asc)

        def filter_zoo(begin="L"):