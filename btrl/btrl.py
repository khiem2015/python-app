class AnimeItem:
    def __init__(self, id, title, release_date, image=None, rating=None, link=None, ):
        self.id = id
        self.title = title
        self.realease_date = release_date
        self.rating = rating
        self.image = image
        self.rating = float(rating) if rating else 0
        self.link = link

    def update(self, new_data:dict):
        for attribute, value in new_data.items():
            if value:
                setattr(self, attribute, value)

    def __str__(self):
        return f"Title: {self.title}\nRelease Date: {self.realease_date}\nRating: {self.rating}\nLink: {self.link}\nImage: {self.image}"
    
anime1 = AnimeItem(1, "Jujutsu no Kaisen", "01/01/2022")
anime2 = AnimeItem(1, "Kimetsu no Yaiba", "01/05/2022")
anime3 = AnimeItem(1, "Attack on Titan", "05/05/2019")
animes = [anime1, anime2, anime3]

for anime in animes:
    print(anime)
anime4 = AnimeItem(4,
                   "One Piece",
                   "01/01/1999"
                   )
animes.append(anime4)
for anime in animes:
    print(anime)

id_to_delete = 2
animes.pop(id_to_delete)
for anime in animes:
    print(anime)

update_data = {"rating": 9.5}
anime1.update(update_data)
print(anime1)


anime1 = AnimeItem(1, "Jujutsu no Kaisen", "01/01/2022")

new_data = {"title": "Jujutsu no Kaisen 2"}
anime1.update(new_data)
print(anime1.title)
print(anime1.realease_date)

class AnimeList:
    def __init__(self):
        self.anime_list = []
        
    def create(self, anime:AnimeItem):
        self.anime_list.append(anime)

    
    def get_all(self):
        return self.anime_list
    
    def get_by_id(self, id):
            result = None
            for anime in self.anime_list:
                if anime.id == id:
                    result = anime
                    break
            return result
                
    def update(self, id, new_data:dict):
        for anime in self.anime_list:
            if anime.id == id:
                anime.update(new_data)
                return True
        return False
    
    def delete(self, id):
        for anime in self.anime_list:
            if id == id:
                self.anime_list.remove(anime)
                return True
            return False
    
    
    def sort_by_title(self, asc=True):
        self.anime_list.sort(key=lambda x: x.title, reverse=asc)

    def sort_by_rating(self, asc=True):
        self.anime_list.sort(key=lambda x: x.rating, reverse=asc)

    def sort_by_release_date(self, asc=True):
        self.anime_list.sort(key=lambda x: x.release_date, reverse=asc)


    
