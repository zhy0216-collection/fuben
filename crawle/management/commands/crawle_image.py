# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import requests
from fuben.models import ComicBook
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

class Command(BaseCommand):
    help = "crawle comic image"

    def handle(self, *args, **options):
        if args[0] == "cover":
            crawle_cover()


def crawle_cover():
    for cb in ComicBook.objects.all():
        if not cb.cover:
            _comic_book_crawle_cover(cb)

def _comic_book_crawle_cover(comic_book):
    headers = {'refer': comic_book.original_link}
    r = requests.get(comic_book.original_cover_url, headers=headers)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    comic_book.cover.save("%s.jpg"%comic_book.name, File(img_temp), save=True)
