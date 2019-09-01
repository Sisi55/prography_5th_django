from django.db import models

# Create your models here.

class Info(object):

    def __init__(self,n):
        self.number = n

    def to_dict(self):

        dest = {
            u'number': self.number
        }

        return dest


class Post(object):

    def __init__(self,title,contents,time,n):
        self.title = title
        self.contents = contents
        self.time = time
        self.number = n
    #title
    #contents
    #페이지 번호 ?
    #날짜 -- 작성하면 저장, 수정하면 덮어쓰기

    def to_dict(self):

        dest = {
            u'title': self.title,
            u'contents': self.contents,
            u'time': self.time,
            u'number': self.number
        }

        return dest


# class City(object):
#     def __init__(self, name, state, country, capital=False, population=0,
#                  regions=[]):
#         self.name = name
#         self.state = state
#         self.country = country
#         self.capital = capital
#         self.population = population
#         self.regions = regions

    # def to_dict(self):
    #     # [START_EXCLUDE]
    #     dest = {
    #         u'name': self.name,
    #         u'state': self.state,
    #         u'country': self.country
    #     }

    #     if self.capital:
    #         dest[u'capital'] = self.capital

    #     if self.population:
    #         dest[u'population'] = self.population

    #     if self.regions:
    #         dest[u'regions'] = self.regions

    #     return dest