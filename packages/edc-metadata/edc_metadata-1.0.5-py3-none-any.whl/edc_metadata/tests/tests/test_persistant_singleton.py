from copy import deepcopy
from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.models import Appointment
from edc_appointment.tests.test_case_mixins import AppointmentTestCaseMixin
from edc_consent import site_consents
from edc_consent.consent_definition import ConsentDefinition
from edc_constants.constants import FEMALE, MALE
from edc_facility import import_holidays
from edc_utils import get_utcnow
from edc_visit_schedule.constants import DAY1, MONTH1, MONTH3, MONTH6, WEEK2
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.models import SubjectVisit
from model_bakery import baker

from edc_metadata import KEYED, NOT_REQUIRED, REQUIRED
from edc_metadata.metadata import CrfMetadataGetter
from edc_metadata.metadata_handler import MetadataHandlerError
from edc_metadata.metadata_rules import (
    CrfRule,
    CrfRuleGroup,
    PersistantSingletonMixin,
    site_metadata_rules,
)
from edc_metadata.models import CrfMetadata

from ..models import CrfOne, SubjectConsent
from ..visit_schedule2 import get_visit_schedule

test_datetime = datetime(2019, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC"))


class CrfOneForm(forms.ModelForm):
    class Meta:
        model = CrfOne
        fields = "__all__"


class TestCaseMixin(AppointmentTestCaseMixin):
    @staticmethod
    def get_subject_consent():
        return baker.make_recipe(
            "edc_metadata.subjectconsentv1",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier="1234",
            initials="XX",
            gender=FEMALE,
            dob=test_datetime.date() - relativedelta(years=25),
            site=Site.objects.get(id=settings.SITE_ID),
            consent_datetime=test_datetime,
        )

    def get_subject_visit(
        self,
        visit_code=None,
        visit_code_sequence=None,
        reason=None,
        appt_datetime=None,
    ):
        reason = reason or SCHEDULED
        subject_consent = self.get_subject_consent()
        options = dict(
            subject_identifier=subject_consent.subject_identifier,
            visit_code=visit_code or DAY1,
            visit_code_sequence=(
                visit_code_sequence if visit_code_sequence is not None else 0
            ),
            reason=reason,
        )
        if appt_datetime:
            options.update(appt_datetime=appt_datetime)
        appointment = self.get_appointment(**options)
        subject_visit = SubjectVisit(
            appointment=appointment,
            subject_identifier=appointment.subject_identifier,
            report_datetime=appointment.appt_datetime,
            visit_code=appointment.visit_code,
            visit_code_sequence=appointment.visit_code_sequence,
            visit_schedule_name=appointment.visit_schedule_name,
            schedule_name=appointment.schedule_name,
            reason=SCHEDULED,
        )
        subject_visit.save()
        subject_visit.refresh_from_db()
        return subject_visit

    @staticmethod
    def get_next_subject_visit(subject_visit):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        subject_visit = SubjectVisit(
            appointment=next_appointment,
            reason=SCHEDULED,
            report_datetime=next_appointment.appt_datetime,
            visit_code=next_appointment.visit_code,
            visit_code_sequence=next_appointment.visit_code_sequence,
        )
        subject_visit.save()
        subject_visit.refresh_from_db()
        return subject_visit


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=test_datetime - relativedelta(years=3),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=test_datetime + relativedelta(years=3),
)
class TestPersistantSingleton(TestCaseMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        traveller = time_machine.travel(test_datetime)
        traveller.start()

        consent_v1 = ConsentDefinition(
            "edc_metadata.subjectconsentv1",
            version="1",
            start=get_utcnow(),
            end=get_utcnow() + relativedelta(years=3),
            age_min=18,
            age_is_adult=18,
            age_max=64,
            gender=[MALE, FEMALE],
        )
        site_consents.registry = {}
        site_consents.register(consent_v1)
        site_visit_schedules._registry = {}
        site_visit_schedules.loaded = False
        site_visit_schedules.register(get_visit_schedule(consent_v1))

        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)

        self.user = User.objects.create(username="erik")

        self.subject_identifier = "1111111"

        subject_consent = SubjectConsent.objects.create(
            subject_identifier=self.subject_identifier,
            consent_datetime=get_utcnow(),
        )
        _, self.schedule = site_visit_schedules.get_by_onschedule_model(
            "edc_metadata.onschedule"
        )
        self.schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=subject_consent.consent_datetime,
        )
        self.appointment = Appointment.objects.get(
            subject_identifier=self.subject_identifier,
            visit_code=self.schedule.visits.first.code,
        )
        self.subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment,
            report_datetime=self.appointment.appt_datetime,
            subject_identifier=self.subject_identifier,
            reason=SCHEDULED,
        )

        self.data = dict(
            subject_visit=self.subject_visit,
            report_datetime=self.subject_visit.report_datetime,
            f1="blah",
            f2="blah",
            f3="blah",
            site=Site.objects.get(id=settings.SITE_ID),
        )
        traveller.stop()

    @property
    def rule_group(self):
        class Predicates(PersistantSingletonMixin):
            app_label = "edc_metadata"

            def crfone_required(self, visit, **kwargs):  # noqa
                model = f"{self.app_label}.crfone"
                return self.persistant_singleton_required(
                    visit, model=model, exclude_visit_codes=[DAY1]
                )

        pc = Predicates()

        class RuleGroup(CrfRuleGroup):
            crfone = CrfRule(
                predicate=pc.crfone_required,
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crfone"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_visit_tracking.subjectvisit"

        return RuleGroup

    @time_machine.travel(test_datetime)
    def test_baseline_not_required(self):
        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)
        form = CrfOneForm(data=self.data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        self.assertRaises(MetadataHandlerError, form.save)

        crf_metadata_getter = CrfMetadataGetter(appointment=self.subject_visit.appointment)
        self.assertFalse(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=REQUIRED
            ).exists()
        )

    @time_machine.travel(test_datetime)
    def test_1005_required(self):
        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, WEEK2)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(model="edc_metadata.crfone").exists()
        )
        self.assertEqual(
            crf_metadata_getter.metadata_objects.get(
                model="edc_metadata.crfone", visit_code=WEEK2
            ).entry_status,
            REQUIRED,
        )

        self.assertEqual(CrfMetadata.objects.filter(model="edc_metadata.crfone").count(), 1)

        data = deepcopy(self.data)
        data.update(subject_visit=subject_visit, report_datetime=subject_visit.report_datetime)
        form = CrfOneForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=KEYED
            ).exists()
        )
        traveller.stop()

    @time_machine.travel(test_datetime)
    def test_visit_required_if_not_submitted(self):
        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, WEEK2)
        self.assertEqual(CrfMetadata.objects.filter(model="edc_metadata.crfone").count(), 1)
        self.assertEqual(
            [(WEEK2, REQUIRED)],
            [
                (obj.visit_code, obj.entry_status)
                for obj in CrfMetadata.objects.filter(model="edc_metadata.crfone").order_by(
                    "timepoint"
                )
            ],
        )
        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller.stop()
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, MONTH1)
        self.assertEqual(CrfMetadata.objects.filter(model="edc_metadata.crfone").count(), 2)
        self.assertEqual(
            [(WEEK2, NOT_REQUIRED), (MONTH1, REQUIRED)],
            [
                (obj.visit_code, obj.entry_status)
                for obj in CrfMetadata.objects.filter(model="edc_metadata.crfone").order_by(
                    "timepoint"
                )
            ],
        )

        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller.stop()
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, MONTH3)
        self.assertEqual(CrfMetadata.objects.filter(model="edc_metadata.crfone").count(), 3)
        self.assertEqual(
            [(WEEK2, NOT_REQUIRED), (MONTH1, NOT_REQUIRED), (MONTH3, REQUIRED)],
            [
                (obj.visit_code, obj.entry_status)
                for obj in CrfMetadata.objects.filter(model="edc_metadata.crfone").order_by(
                    "timepoint"
                )
            ],
        )

        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller.stop()
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, MONTH6)
        self.assertEqual(CrfMetadata.objects.filter(model="edc_metadata.crfone").count(), 4)
        self.assertEqual(
            [
                (WEEK2, NOT_REQUIRED),
                (MONTH1, NOT_REQUIRED),
                (MONTH3, NOT_REQUIRED),
                (MONTH6, REQUIRED),
            ],
            [
                (obj.visit_code, obj.entry_status)
                for obj in CrfMetadata.objects.filter(model="edc_metadata.crfone").order_by(
                    "timepoint"
                )
            ],
        )

    @time_machine.travel(test_datetime)
    def test_1010_required_if_not_submitted(self):
        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, MONTH1)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(model="edc_metadata.crfone").exists()
        )
        self.assertEqual(
            crf_metadata_getter.metadata_objects.get(
                model="edc_metadata.crfone", visit_code=MONTH1
            ).entry_status,
            REQUIRED,
        )
        data = deepcopy(self.data)
        data.update(subject_visit=subject_visit, report_datetime=subject_visit.report_datetime)
        form = CrfOneForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=KEYED
            ).exists()
        )
        traveller.stop()

    @time_machine.travel(test_datetime)
    def test_1030_required_if_not_submitted(self):
        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        traveller = time_machine.travel(subject_visit.report_datetime)
        traveller.start()
        self.assertEqual(subject_visit.visit_code, MONTH3)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(model="edc_metadata.crfone").exists()
        )
        self.assertEqual(
            crf_metadata_getter.metadata_objects.get(
                model="edc_metadata.crfone", visit_code=MONTH3
            ).entry_status,
            REQUIRED,
        )
        data = deepcopy(self.data)
        data.update(subject_visit=subject_visit, report_datetime=subject_visit.report_datetime)
        form = CrfOneForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=KEYED
            ).exists()
        )
        traveller.stop()

    @time_machine.travel(test_datetime)
    def test_1030_not_required_if_submitted(self):
        site_metadata_rules.registry = {}
        site_metadata_rules.register(self.rule_group)
        subject_visit_1005 = self.get_next_subject_visit(self.subject_visit)
        subject_visit_1010 = self.get_next_subject_visit(subject_visit_1005)
        subject_visit_1030 = self.get_next_subject_visit(subject_visit_1010)
        self.assertEqual(subject_visit_1030.visit_code, MONTH3)
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1030.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=REQUIRED
            ).exists()
        )
        data = deepcopy(self.data)
        data.update(
            subject_visit=subject_visit_1010,
            report_datetime=subject_visit_1010.report_datetime,
        )
        traveller = time_machine.travel(subject_visit_1010.report_datetime)
        traveller.start()
        form = CrfOneForm(data=data)
        form.is_valid()
        self.assertEqual({}, form._errors)
        form.save()
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1005.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=NOT_REQUIRED
            ).exists()
        )
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1010.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=KEYED
            ).exists()
        )
        crf_metadata_getter = CrfMetadataGetter(appointment=subject_visit_1030.appointment)
        self.assertTrue(
            crf_metadata_getter.metadata_objects.filter(
                model="edc_metadata.crfone", entry_status=NOT_REQUIRED
            ).exists()
        )
