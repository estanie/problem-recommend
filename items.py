# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaekjoonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    prob_num = scrapy.Field()
    prob_title = scrapy.Field()
    prob_solve_date = scrapy.Field()
    prob_url = scrapy.Field()
    pass

class RankingItem(scrapy.Item):
    prob_num = scrapy.Field()
    prob_title = scrapy.Field()
    prob_url = scrapy.Field()
    prob_solve_count = scrapy.Field()
    prob_already_solve = scrapy.Field()