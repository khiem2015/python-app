import json

from data_io import load_json_data, write_json_data
class AnimeItem:
    def __init__(self, anime_id, title, release_date, image=None, rating=None, link=None):
        self.id = anime_id
        self.title = title
        self.release_date = release_date
        self.image = image
        self.rating = float(rating) if rating else 0
        self.link = link
anime = AnimeItem(1, "One Piece", "01/01/2001")
with open("data.json", "w") as file:
    json.dump(anime.__dict__, file)

    def update(self, new_data:dict):
        for key, value in new_data.items():
            if value:
                self(self, key, value)

    def __str__(self):
        return f"Title: {self.title}\nRelease Date: {self.realease_date}\nRating: {self.rating}\nLink: {self.link}"
    
class AnimeDatabase:
    def __init__(self):
        self.animeList = []
        self.load_data()

    def load_data(self):
        try:
            json_data = load_json_data("data.json")
            self.animeList = [AnimeItem(**item) for item in json_data]
        except FileNotFoundError:
            self.animeList = []
    
    def save_data(self):
        data_to_save = [anime.__dict__ for anime in self.animeList]
        write_json_data("data.json", data_to_save)

    def add(self, anime:AnimeItem):
        self.load_data()
        self.animeList.append(anime)
        self.save_data()

    def get_all(self):
        self.load_data()
        for anime in self.animeList:
            print(anime)
        
    
    def get_by_id(self, id):
        self.load_data()
        for id in self.animeList:
            print(id)

    def update(self, id, new_data:dict):
        self.load_data
        for id in self.animeList:
            if id == id:
                anime.update(new_data)
                self.save_data()
                return True
            return False

    def delete(self,id):
        self.load_data()
        for anime in self.animeList:
            if anime.id == id:
                self.animeList.remove(anime)
                self.save_data()
                return True
            return False
        
    def sort_by_date(self, asc=True):
        self.load_data()
        self.animeList.sort(key=lambda x: x.release_date, reverse=not asc)
        self.save_data()

anime_db = AnimeDatabase()
anime1 = AnimeItem(1, "Naruto", "2002-10-03")
anime2 = AnimeItem(2, "One Piece", "1999-10-20")
anime3 = AnimeItem(3, "Bleach", "2004-10-05")

anime_db.add(anime1)
anime_db.add(anime2)
anime_db.add(anime3)

print("All anime:")
print("_"*100)
for anime in anime_db.get_all():
    print(anime)

id_to_update = 1
new_data = {
    "title": "Naruto Shippuden"
    "release_date": 2007-02-15,
    "rating": 8.8,
    "link": "https://example.com/narutoshippuden"
}

anime_db.update(id_to_update, new_data)

print("Update anime:")
print("_"*100)
print(anime_db.get_by_id(id_to_update))

anime_db.delete(2)

print("All anime:")
print("_"*100)
for anime in anime_db.get_all():
    print(anime)
