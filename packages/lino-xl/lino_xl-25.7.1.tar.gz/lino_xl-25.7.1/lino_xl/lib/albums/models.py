# -*- coding: UTF-8 -*-
# Copyright 2008-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import os
from os.path import join, exists
import glob
from pathlib import Path
from datetime import datetime

from django.db import models
from django.db.models.fields.files import FieldFile
from django.conf import settings
from django.utils.text import format_lazy
# from lino.api import string_concat
from django.utils.translation import pgettext_lazy as pgettext
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError

from lino.utils.html import E, join_elems, tostring
from lino.api import dd, rt, _
from lino.core.gfks import gfk2lookup
from lino.core.utils import model_class_path
from lino import mixins
from lino.mixins.sequenced import Sequenced
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser, OfficeStaff, OfficeOperator
from lino.mixins import Hierarchical
from lino.utils.mldbc.mixins import BabelDesignated
# from lino.modlib.uploads.mixins import UploadBase, safe_filename, FileUsable, GalleryViewable
from lino.modlib.uploads.mixins import UploadBase, safe_filename, GalleryViewable
from lino.core import constants


def filename_leaf(name):
    i = name.rfind('/')
    if i != -1:
        return name[i + 1:]
    return name


class Album(BabelDesignated, Hierarchical):

    class Meta(object):
        abstract = dd.is_abstract_model(__name__, 'Album')
        verbose_name = _("Album")
        verbose_name_plural = _("Albums")


dd.inject_field('uploads.Upload', 'album',
                dd.ForeignKey("albums.Album", blank=True, null=True))


class AlbumDetail(dd.DetailLayout):
    main = """
    treeview_panel general
    """

    general = """
    designation id parent
    FilesByAlbum #AlbumsByAlbum
    """


class Albums(dd.Table):
    model = 'albums.Album'
    required_roles = dd.login_required(OfficeStaff)

    column_names = "designation parent *"
    detail_layout = "albums.AlbumDetail"
    insert_layout = "designation parent"


from lino.modlib.uploads.ui import Uploads


class FilesByAlbum(Uploads):
    master_key = "album"
    default_display_modes = {None: constants.DISPLAY_MODE_GALLERY}
    column_names = "file description thumbnail *"


class AlbumsByAlbum(Albums):
    label = "Albums"
    master_key = "parent"
