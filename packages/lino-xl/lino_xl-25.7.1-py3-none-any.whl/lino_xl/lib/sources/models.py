# -*- coding: UTF-8 -*-
# Copyright 2024-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import requests
from bs4 import BeautifulSoup
from django.db import models

from lino.api import dd, rt, _
from lino.core.roles import SiteAdmin
from lino.mixins import Referrable
from lino.mixins.human import Human, Born
from lino.mixins.sequenced import Hierarchical
from lino.modlib.comments.mixins import Commentable
from lino.modlib.publisher.mixins import Publishable
from lino.utils.mldbc.mixins import BabelDesignated

SIMULATE_ONLINE_REQUESTS = True
REQUESTS = {
    'https://en.wikipedia.org/wiki/History_of_PDF': 'History of PDF - Wikipedia'}


class Source(Referrable, Hierarchical, Commentable, Publishable):

    class Meta:
        app_label = 'sources'
        abstract = dd.is_abstract_model(__name__, 'Source')
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    memo_command = "src"

    url = models.URLField(_("URL"), blank=True)
    title = models.CharField(_("Title"), max_length=200, blank=True)
    author = dd.ForeignKey("sources.Author", blank=True, null=True)
    copyright_owner = dd.ForeignKey("contacts.Company", verbose_name=_(
        "Copyright owner"), blank=True, null=True)
    year_published = models.CharField(_("Year published"), max_length=200, blank=True)
    license = dd.ForeignKey("sources.License", blank=True, null=True)

    def __str__(self):
        if self.author is None:
            if self.title:
                s = self.title
            elif self.url:
                s = self.url
            else:
                s = super().__str__()
        else:
            s = "{0.title} by {0.author}".format(self)
        return s

    def full_clean(self):
        super().full_clean()
        if self.title or not self.url:
            return
        if SIMULATE_ONLINE_REQUESTS:
            self.title = REQUESTS[self.url]
        else:
            r = requests.get(self.url)
            if r.status_code != 200:
                return
            soup = BeautifulSoup(r.content, 'lxml')
            if soup.title:
                self.title = soup.title.string
            else:
                self.title = "(no title)"
            print("Online request succeeded:", {self.url: self.title})


dd.update_field(Source, 'parent', verbose_name=_("Part of"))


class Author(Human, Born):

    class Meta:
        app_label = 'sources'
        abstract = dd.is_abstract_model(__name__, 'Author')
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    death_date = dd.IncompleteDateField(
        blank=True, verbose_name=_("Death date"))
    birth_place = dd.ForeignKey("countries.Place",
                                verbose_name=_("Birth place"),
                                blank=True, null=True, related_name="authors_born")
    death_place = dd.ForeignKey("countries.Place",
                                verbose_name=_("Death place"),
                                blank=True, null=True, related_name="authors_died")

    def __str__(self):
        s = super().__str__()
        if self.birth_date:
            if self.death_date:
                s += " ({}—{})".format(self.birth_date, self.death_date)
            else:
                s += " (*{})".format(self.birth_date)
        elif self.death_date:
            s += " (†{})".format(self.birth_date)
        return s


class License(BabelDesignated):

    class Meta:
        app_label = 'sources'
        abstract = dd.is_abstract_model(__name__, 'License')
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")


class Sources(dd.Table):
    model = 'sources.Source'
    column_names = 'id title author url *'
    order_by = ['ref']

    insert_layout = """
    url
    title
    author
    """

    detail_layout = """
    url
    ref:10 title:60 id
    author  parent
    comments.CommentsByRFC SourcesByParent
    """


class SourcesByParent(Sources):
    label = _("Parts")
    master_key = 'parent'
    column_names = 'title ref *'


class Licenses(dd.Table):
    model = 'sources.License'
    column_names = 'designation *'
    required_roles = dd.login_required(SiteAdmin)


class Authors(dd.Table):
    model = 'sources.Author'
    column_names = 'last_name first_name birth_date *'
    required_roles = dd.login_required(SiteAdmin)
    order_by = ['last_name', 'first_name', 'birth_date', 'id']
