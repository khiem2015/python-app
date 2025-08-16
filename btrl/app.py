class book:
    def __init__(self, title, id, author, averageRating, publicationDate ):
        self.title = title
        self.id = id
        self.author = author
        self.averageRating  = averageRating
        self.publicationDate = publicationDate
        def __str__(self):
            return (
                f"ID: {self.id}\n"
                f"Title: {self.title}\n"
                f"Author: {self.author}"
                f"Rating: {self.average_rating}\n"
                f"Publication Date: {self.publication_date}\n"
            )
    class bookCollection:
        def __init__():

         def add(self, id):
            if book.id == id:
                return False
            else:
                return True
         def update(self, id, new_data):
            for key, value in new_data.items():
                if value is not None:
                    setattr(self, key, value)
        
         def delete(self, id):
            for key, value in book:
                if id == id:
                    self.book.remove()
        
         def sort_by_title(self, asc=True):
            self.anime_list.sort(key=lambda x: x.title, reverse=asc)
# end
class Homework:
    def __init__(self, lập_trình, làm_toán, làm_văn, mỹ_thuật, priority):
        self.lập_trình = lập_trình
        self.làm_toán = làm_toán
        self.làm_văn = làm_văn
        self.mỹ_thuật = mỹ_thuật
        self.priority = priority
        
        priority = Homework("1-low, 2-normal, 3-important")
    class HomworkList:
        def __init__(self):
           self.HomworkList = []
           self.load_data()

    def load_data(self):
        try:
            json_data = load_data("data.json")
            self.HomworkList = [Homework(**item) for item in json_data]
        except FileNotFoundError:
            self.HomworkList = []          

        def add(self, Homework:Homework):
        self.load_data()
        self.HomworkList.append(Homework)
        self.save_data()
