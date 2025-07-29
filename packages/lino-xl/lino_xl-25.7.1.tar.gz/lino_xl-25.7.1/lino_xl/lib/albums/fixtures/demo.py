# -*- coding: UTF-8 -*-
# Copyright 2009-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino import logger
from lino.api import rt, dd, _
from lino.utils import Cycler
from lino.modlib.uploads.mixins import make_uploaded_file

try:
    from lino_book import DEMO_DATA
except ImportError:
    DEMO_DATA = None


def objects():
    Album = rt.models.albums.Album
    Upload = rt.models.uploads.Upload
    Volume = rt.models.uploads.Volume

    demo_date = dd.demo_date()

    top = Album(**dd.str2kw("designation", _("All")))
    yield top
    yield Album(parent=top, **dd.str2kw("designation", _("Furniture")))
    yield Album(parent=top, **dd.str2kw("designation", _("Things")))
    yield Album(parent=top, **dd.str2kw("designation", _("Services")))

    books = Album(parent=top, **dd.str2kw("designation", _("Books")))
    yield books

    yield Album(parent=books, **dd.str2kw("designation", _("Biographies")))
    yield Album(parent=books, **dd.str2kw("designation", _("Business")))
    yield Album(parent=books, **dd.str2kw("designation", _("Culture")))
    yield Album(parent=books, **dd.str2kw("designation", _("Children")))
    yield Album(parent=books, **dd.str2kw("designation", _("Medicine")))

    thrill = Album(parent=books, **dd.str2kw("designation", _("Thriller")))
    yield thrill

    if DEMO_DATA is None:
        logger.info("No demo data because lino_book is not installed")
        return

    for cover in """\
MurderontheOrientExpress.jpg Murder_on_the_orient_express_cover
StormIsland.jpg Storm_island_cover
AndThenThereWereNone.jpg And_then_there_were_none
FirstThereWereTen.jpg First_there_were_ten
""".splitlines():
        name, description = cover.split()
        src = DEMO_DATA / "images" / name
        file = make_uploaded_file(name, src, demo_date)
        yield Upload(album=thrill,
                   file=file,
                   description=description.replace('_', ' '))

    photos_album = Album(parent=top, **dd.str2kw("designation", _("Photos")))
    yield photos_album

    # photos_vol = Volume.objects.get(ref="photos")
    for obj in Upload.objects.filter(volume__ref="photos"):
        obj.album = photos_album
        yield obj
