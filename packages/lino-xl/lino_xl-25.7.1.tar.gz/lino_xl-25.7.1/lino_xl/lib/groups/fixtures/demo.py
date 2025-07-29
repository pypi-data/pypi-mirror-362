# -*- coding: UTF-8 -*-
# Copyright 2017-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils.mldbc import babel_named as named


def objects():
    Group = rt.models.groups.Group
    User = rt.models.users.User
    UserTypes = rt.models.users.UserTypes

    yield named(Group, _("Hitchhiker's Guide to the Galaxy"))
    yield named(Group, _("Star Trek"))
    yield named(Group, _("Harry Potter"))

    def user(username, **kwargs):
        kwargs.update(user_type=UserTypes.user, username=username)
        if not dd.plugins.users.with_nickname:
            kwargs.pop('nickname', None)
        return User(**kwargs)

    yield user("andy", first_name="Andreas", last_name="Anderson", nickname="Andy", email="andy@example.com")
    yield user("bert", first_name="Albert", last_name="Bernstein", nickname="Bert", email="bert@example.com")
    yield user("chloe", first_name="Chloe", last_name="Cleoment", email="chloe@example.com")
