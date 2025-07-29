from datetime import datetime
from unittest.mock import MagicMock
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.views.generic.base import ContextMixin, View
from edc_appointment.constants import INCOMPLETE_APPT
from edc_appointment.creators import UnscheduledAppointmentCreator
from edc_appointment.models import Appointment
from edc_consent import site_consents
from edc_consent.consent_definition import ConsentDefinition
from edc_constants.constants import FEMALE, MALE
from edc_facility.import_holidays import import_holidays
from edc_lab.models.panel import Panel
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.models import SubjectVisit

from ...models import CrfMetadata, RequisitionMetadata
from ...view_mixins import MetadataViewMixin
from ..models import CrfOne, CrfThree, SubjectConsent
from ..visit_schedule import get_visit_schedule

test_datetime = datetime(2019, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC"))


class DummyCrfModelWrapper:
    def __init__(self, **kwargs):
        self.model_obj = kwargs.get("model_obj")
        self.model = kwargs.get("model")


class DummyRequisitionModelWrapper:
    def __init__(self, **kwargs):
        self.model_obj = kwargs.get("model_obj")
        self.model = kwargs.get("model")


class MyView(MetadataViewMixin, ContextMixin, View):
    crf_model_wrapper_cls = DummyCrfModelWrapper
    requisition_model_wrapper_cls = DummyRequisitionModelWrapper

    def __init__(self, appointment: Appointment = None, **kwargs):
        self._appointment = appointment
        super().__init__(**kwargs)

    @property
    def appointment(self) -> Appointment:
        return self._appointment


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=test_datetime - relativedelta(years=3),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=test_datetime + relativedelta(years=3),
)
class TestViewMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()
        return super().setUpTestData()

    def setUp(self):
        self.user = User.objects.create(username="erik")

        for name in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
            Panel.objects.create(name=name)

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
        self.subject_identifier = "1111111"
        self.assertEqual(CrfMetadata.objects.all().count(), 0)
        self.assertEqual(RequisitionMetadata.objects.all().count(), 0)

        subject_consent = SubjectConsent.objects.create(
            subject_identifier=self.subject_identifier, consent_datetime=get_utcnow()
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
            subject_identifier=self.subject_identifier,
            report_datetime=self.appointment.appt_datetime,
            visit_code=self.appointment.visit_code,
            visit_code_sequence=self.appointment.visit_code_sequence,
            visit_schedule_name=self.appointment.visit_schedule_name,
            schedule_name=self.appointment.schedule_name,
            reason=SCHEDULED,
        )

    def test_view_mixin(self):
        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user
        view = MyView(request=request, appointment=self.appointment)
        view.subject_identifier = self.subject_identifier
        view.kwargs = {}
        view.get_context_data()

    def test_view_mixin_context_data_crfs(self):
        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user
        view = MyView(request=request, appointment=self.appointment)
        view.subject_identifier = self.subject_identifier
        view.kwargs = {}
        context_data = view.get_context_data()
        self.assertEqual(len(context_data.get("crfs")), 5)

    def test_view_mixin_context_data_crfs_exists(self):
        CrfOne.objects.create(subject_visit=self.subject_visit)
        CrfThree.objects.create(subject_visit=self.subject_visit)
        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user
        view = MyView(request=request, appointment=self.appointment)
        view.subject_identifier = self.subject_identifier
        view.kwargs = {}
        context_data = view.get_context_data()
        for metadata in context_data.get("crfs"):
            if metadata.model in ["edc_metadata.crfone", "edc_metadata.crfthree"]:
                self.assertIsNotNone(metadata.model_instance)
            else:
                self.assertIsNone(metadata.model_instance)

    def test_view_mixin_context_data_requisitions(self):
        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user
        view = MyView(request=request, appointment=self.appointment)
        view.subject_identifier = self.subject_identifier
        context_data = view.get_context_data()
        self.assertEqual(len(context_data.get("requisitions")), 2)

    def test_view_mixin_context_data_crfs_unscheduled(self):
        self.appointment.appt_status = INCOMPLETE_APPT
        self.appointment.save()
        creator = UnscheduledAppointmentCreator(
            subject_identifier=self.subject_identifier,
            visit_schedule_name=self.appointment.visit_schedule_name,
            schedule_name=self.appointment.schedule_name,
            visit_code=self.appointment.visit_code,
            suggested_visit_code_sequence=self.appointment.visit_code_sequence + 1,
            facility=self.appointment.facility,
        )

        SubjectVisit.objects.create(
            appointment=creator.appointment,
            subject_identifier=self.subject_identifier,
            reason=SCHEDULED,
        )

        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user
        view = MyView(request=request, appointment=creator.appointment)
        view.subject_identifier = self.subject_identifier
        view.kwargs = {}
        context_data = view.get_context_data()
        self.assertEqual(len(context_data.get("crfs")), 3)
        self.assertEqual(len(context_data.get("requisitions")), 4)

        request = RequestFactory().get("/?f=f&e=e&o=o&q=q")
        request.user = self.user

        view = MyView(request=request, appointment=self.appointment)
        view.subject_identifier = self.subject_identifier
        view.kwargs = {}
        view.request = HttpRequest()
        view.message_user = MagicMock(return_value=None)
        # view.message_user.assert_called_with(3, 4, 5, key='value')
        context_data = view.get_context_data()
        self.assertEqual(len(context_data.get("crfs")), 5)
        self.assertEqual(len(context_data.get("requisitions")), 2)
