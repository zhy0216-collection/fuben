# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from pyquery import PyQuery as pq
from fuben.models import ComicBook, ComicVolume, ComicPage

class Command(BaseCommand):
    help = "crawle comic"

    def handle(self, *args, **options):
        crawle_comic_book()


base_url = "http://manhua.dmzj.com"

def crawle_comic_book():
    print "start book"
    url = "http://manhua.dmzj.com/tags/fubenshenxing.shtml"
    d = pq(url=url)
    sources = [_.original_link for _ in ComicBook.objects.all()]

    for div in d("#hothit div.pic"):
        info = {}
        original_link = base_url + pq(div).find("a").attr("href")
        if original_link in sources:
            continue
        name = pq(div).find("p.t").text()
        last_volume = pq(div).find("p.d").text()
        if u"[完]" in name:
            name = name[:-3]
            info["finished"] = True
        info["name"] = name
        info["last_volume"] = last_volume
        info["original_link"] = original_link
        info["original_cover_url"] = base_url + pq(div).find("img").attr("src")

        book = ComicBook.objects.create(**info)
        

def crawle_comic_volume():
    print "start volume"


def crawle_comic_page():
    print "start page"



