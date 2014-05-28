# -*- coding: utf-8 -*-

import datetime

from django.db import models

# Create your models here.

class FuBen(object):
    _INSTANCE = None

    def __init__(self):
        self.name                = u"福本伸行"
        self.en_name             = "FUKUMOTO NOBUYUKI"
        self.nationality         = u"日本"
        self.birthplace          = u"神奈川县"
        self.birthday            = datetime.datetime(1958, 12, 10)

    @classmethod
    def get_instance(cls):
        instance = cls._INSTANCE or cls()
        return instance

    @property 
    def age(self):
        return (datetime.datetime.now() - self.birthday).days/365




class ComicBook(models.Model):

    name                        = models.CharField(max_length=10)
    series                      = models.CharField(max_length=10)
    finished                    = models.BooleanField(default=False)
    last_volume                 = models.ForeignKey("ComicVolume", blank=True)
    volume_count                = models.IntegerField()
    des                         = models.TextField()
    
    original_cover_url          = models.CharField(max_length=120)
    upyun_cover_url             = models.CharField(max_length=120)
    original_link               = models.CharField(max_length=120)


    @property
    def cover_url(self):
        return self.original_cover_url or self.upyun_cover_url




class ComicVolume(models.Model):

    index                       = models.IntegerField() # from 1
    special_series              = models.CharField(max_length=10, default="")
    comic_book                  = models.ForeignKey("ComicBook")
    total_pages                 = models.IntegerField()
    original_link               = models.CharField(max_length=120) 


class ComicPage(models.Model):
    volume                      = models.ForeignKey("ComicVolume")
    page_number                 = models.IntegerField(default=1)

    original_page_url           = models.CharField(max_length=120)
    upyun_page_url              = models.CharField(max_length=120)
    original_link               = models.CharField(max_length=120) 




