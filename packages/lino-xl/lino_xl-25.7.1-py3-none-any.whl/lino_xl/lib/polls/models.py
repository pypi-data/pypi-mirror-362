# -*- coding: UTF-8 -*-
# Copyright 2013-2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.contrib.contenttypes.models import ContentType

from lino.api import dd, rt
from lino import mixins
from lino.mixins import Referrable
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.gfks.fields import GenericForeignKey, GenericForeignKeyIdField

from .utils import ResponseStates, PollStates
from .ui import *


class ChoiceSet(mixins.BabelNamed):

    class Meta(object):
        app_label = 'polls'
        verbose_name = _("Choice Set")
        verbose_name_plural = _("Choice Sets")

    choice_type = dd.ForeignKey(
        ContentType,
        editable=True,
        # related_name="%(app_label)s_%(class)s_set",
        verbose_name=_("Database model"),
        blank=True, null=True
    )


class Choice(mixins.BabelNamed, mixins.Sequenced):

    class Meta(object):
        app_label = 'polls'
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    choiceset = dd.ForeignKey('polls.ChoiceSet', related_name='choices')

    def get_siblings(self):
        return self.choiceset.choices.all()

    @dd.action()
    def select_by_response(self, ar):
        mi = ar.master_instance
        dd.logger.info("20140929 %s", mi)
        if isinstance(mi, Response):
            AnswerChoice(response=mi, choice=self).save()


class Poll(UserAuthored, mixins.CreatedModified, Referrable):

    class Meta(object):
        app_label = 'polls'
        abstract = dd.is_abstract_model(__name__, 'Poll')
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")
        ordering = ['ref']

    title = models.CharField(_("Heading"), max_length=200)

    details = models.TextField(_("Details"), blank=True)

    default_choiceset = dd.ForeignKey('polls.ChoiceSet',
                                      null=True,
                                      blank=True,
                                      related_name='polls',
                                      verbose_name=_("Default Choiceset"))

    default_multiple_choices = models.BooleanField(_("Allow multiple choices"),
                                                   default=False)

    questions_to_add = models.TextField(
        _("Questions to add"),
        help_text=_("Paste text for questions to add. "
                    "Every non-empty line will create one question."),
        blank=True)

    state = PollStates.field(default='draft')

    workflow_state_field = 'state'

    def __str__(self):
        return self.ref or self.title

    def after_ui_save(self, ar, cw):
        if self.questions_to_add:
            # print "20150203 self.questions_to_add", self,
            # self.questions_to_add
            q = None
            qkw = dict()
            number = 1
            for ln in self.questions_to_add.splitlines():
                ln = ln.strip()
                if ln:
                    if ln.startswith('#'):
                        q.details = ln[1:]
                        q.save()
                        continue
                    elif ln.startswith('='):
                        q = Question(poll=self,
                                     title=ln[1:],
                                     is_heading=True,
                                     **qkw)
                        number = 1
                    else:
                        q = Question(poll=self,
                                     title=ln,
                                     number=str(number),
                                     **qkw)
                        number += 1
                    q.full_clean()
                    q.save()
                    qkw.update(seqno=q.seqno + 1)
            self.questions_to_add = ''
            self.save()  # save again because we modified afterwards

        super(Poll, self).after_ui_save(ar, cw)


class Question(mixins.Sequenced):

    class Meta(object):
        app_label = 'polls'
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['seqno']

    allow_cascaded_delete = ['poll']

    poll = dd.ForeignKey('polls.Poll', related_name='questions')
    number = models.CharField(_("No."), max_length=20, blank=True)
    title = models.CharField(pgettext("polls", "Title"), max_length=200)
    details = models.TextField(_("Details"), blank=True)

    choiceset = dd.ForeignKey('polls.ChoiceSet', blank=True, null=True)
    multiple_choices = models.BooleanField(_("Allow multiple choices"),
                                           blank=True,
                                           default=False)
    is_heading = models.BooleanField(_("Heading"), default=False)

    NUMBERED_TITLE_FORMAT = "%s) %s"

    def __str__(self):
        # ~ return self.text[:40].strip() + ' ...'
        if self.number:
            return self.NUMBERED_TITLE_FORMAT % (self.number, self.title)
        return self.title

    def get_siblings(self):
        # ~ return self.choiceset.choices.order_by('seqno')
        return self.poll.questions.all()

    def get_choiceset(self):
        if self.is_heading:
            return None
        if self.choiceset is None:
            return self.poll.default_choiceset
        return self.choiceset

    def full_clean(self, *args, **kw):
        if self.multiple_choices is None:
            self.multiple_choices = self.poll.default_multiple_choices
        # ~ if self.choiceset_id is None:
        # ~ self.choiceset = self.poll.default_choiceset
        super(Question, self).full_clean()


Question.set_widget_options('number', width=5)


class ToggleChoice(dd.Action):
    readonly = False
    show_in_toolbar = False
    parameters = dict(
        question=dd.ForeignKey("polls.Question"),
        choice_type=dd.ForeignKey(ContentType),
        choice_id=dd.PositiveIntegerField(),
    )
    no_params_window = True
    params_layout = 'question\nchoice_type choice_id'

    # We specify params_layout although no_params_window is True because
    # otherwise e.g. lino.api.doctest.get_fields() would display them in
    # arbitrary order

    def run_from_ui(self, ar, **kw):
        response = ar.selected_rows[0]
        if response is None:
            return
        pv = ar.action_param_values
        qs = AnswerChoice.objects.filter(response=response, **pv)
        if qs.count() == 1:
            qs[0].delete()
        elif qs.count() == 0:
            if not pv.question.multiple_choices:
                # delete any other choice which might exist
                qs = AnswerChoice.objects.filter(response=response,
                                                 question=pv.question)
                qs.delete()
            obj = AnswerChoice(response=response, **pv)
            obj.full_clean()
            obj.save()
        else:
            raise Exception("Oops, %s returned %d rows." %
                            (qs.query, qs.count()))
        ar.success(refresh=True, refresh_delayed_value=True)
        # dd.logger.info("20140930 %s", obj)


class Response(UserAuthored, mixins.Registrable):

    class Meta(object):
        app_label = 'polls'
        verbose_name = _("Response")
        verbose_name_plural = _("Responses")
        ordering = ['date']

    poll = dd.ForeignKey('polls.Poll', related_name='responses')
    date = models.DateField(_("Date"), default=dd.today)
    state = ResponseStates.field(default='draft')
    remark = models.TextField(verbose_name=_("My general remark"), blank=True)
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)

    toggle_choice = ToggleChoice()

    @dd.chooser()
    def poll_choices(cls):
        return Poll.objects.filter(state=PollStates.active)

    def __str__(self):
        if self.partner is None:
            return _("%(user)s's response to %(poll)s") % dict(user=self.user,
                                                               poll=self.poll)
        return _("{poll} {partner} {date}").format(
            user=self.user.initials,
            date=dd.fds(self.date),
            partner=self.partner.get_full_name(salutation=False),
            poll=self.poll)

    @classmethod
    def get_registrable_fields(model, site):
        for f in super().get_registrable_fields(site):
            yield f
        yield 'user'
        yield 'poll'
        yield 'date'
        yield 'partner'


class AnswerChoice(dd.Model):

    class Meta(object):
        app_label = 'polls'
        verbose_name = _("Answer Choice")
        verbose_name_plural = _("Answer Choices")
        # ordering = ['question__seqno']

        # ordering removed 20160721 because it probably caused random
        # results when serializing.

    allow_cascaded_delete = ['response']

    response = dd.ForeignKey('polls.Response')
    question = dd.ForeignKey('polls.Question')

    # choice = dd.ForeignKey('polls.Choice',
    #                        related_name='answers',
    #                        verbose_name=_("My answer"),
    #                        blank=True,
    #                        null=True)

    choice_type = dd.ForeignKey(
        ContentType,
        editable=False,
        blank=True,
        null=True,
        # related_name="%(app_label)s_%(class)s_set",
        verbose_name=_("Database model"),
    )

    choice_id = GenericForeignKeyIdField(
        choice_type,
        editable=True,
        blank=True,
        null=True,
        verbose_name=_("Database row"),
    )

    choice = GenericForeignKey("choice_type", "choice_id",
                               verbose_name=_("My answer"))

    # TODO: update to new gfk API
    @dd.chooser()
    def choice_choices(cls, question):
        return question.get_choiceset().choices.all()

    def save(self, *args, **kwargs):
        if self.question.choiceset:
            self.choice_type = self.question.choiceset.choice_type
        else:
            self.choice_type = ContentType.objects.get_for_model(rt.models.polls.Choice)
        super().save(*args, **kwargs)


class AnswerRemark(dd.Model):

    class Meta(object):
        app_label = 'polls'
        verbose_name = _("Answer Remark")
        verbose_name_plural = _("Answer Remarks")
        ordering = ['question__seqno']

    allow_cascaded_delete = ['response']

    response = dd.ForeignKey('polls.Response')
    question = dd.ForeignKey('polls.Question')
    remark = models.TextField(_("My remark"), blank=True)

    # def full_clean(self, *args, **kwargs):
    #     if self.remark:
    #         self.remark = truncate_comment(self.remark, max_p_len=-1)
    #     super().full_clean(*args, **kwargs)

    def __str__(self):
        # return _("Remark for {0}").format(self.question)
        return str(self.question)
