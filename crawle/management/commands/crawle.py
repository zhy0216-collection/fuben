# -*- coding: utf-8 -*-
import gevent.monkey;gevent.monkey.patch_all()
from gevent.pool import Pool
import re
from django.core.management.base import BaseCommand
from pyquery import PyQuery as pq
from fuben.models import ComicBook, ComicVolume, ComicPage

class Command(BaseCommand):
    help = "crawle comic"

    def handle(self, *args, **options):
        if args[0] == "book":
            crawle_comic_book()
        elif args[0] == "volume":
            crawle_comic_volume()
        elif args[0] == "page":
            crawle_comic_page()
        else:
            crawle_comic_book()
            crawle_comic_volume()
            crawle_comic_page()


base_url = "http://manhua.dmzj.com"
_digit_re = re.compile("\d+")

def extract_digit(string):
    r = _digit_re.findall(string)
    if len(r):
        return int(r[0])
    return -1


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

    for book in ComicBook.objects.all():
        d = pq(url=book.original_link)
        for a in d(".cartoon_online_border a"):
            info = {"comic_book": book} 
            info["original_link"] = base_url + pq(a).attr("href")
            info["index"] = extract_digit(pq(a).text())
            ComicVolume.objects.create(**info)



def crawle_comic_page():
    print "start page"
    volumes = ComicVolume.objects.all()
    pool = Pool(1)
    pool.map(_process_single_page, enumerate(volumes))

def _process_single_page(volume_tuple):
    index, v = volume_tuple
    print "start:%s"%index
    d = pq(url=v.original_link)
    content = d.html()
    number_index = content.find("g_max_pic_count")
    limit_page = extract_digit(content[number_index+15:number_index+25])
    print "limit_page:%s"%limit_page
    for i in range(1, limit_page + 1):
        info = {"page_number": i}
        info["volume"] = v
        _t = v.original_link.rsplit(".", 1)
        info["original_link"] = _t[0] + "-%s"%i + ".%s"%_t[1]
        ComicPage.objects.create(**info)


