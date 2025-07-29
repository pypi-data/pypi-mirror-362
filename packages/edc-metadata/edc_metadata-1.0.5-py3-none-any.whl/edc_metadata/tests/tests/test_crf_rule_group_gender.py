from datetime import datetime
from zoneinfo import ZoneInfo

import time_machine
from dateutil.relativedelta import relativedelta
from django.test import TestCase, override_settings
from edc_appointment.models import Appointment
from edc_consent import site_consents
from edc_consent.consent_definition import ConsentDefinition
from edc_constants.constants import FEMALE, MALE
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_tracking.models import SubjectVisit
from faker import Faker

from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import (
    PF,
    CrfRule,
    CrfRuleGroup,
    CrfRuleModelConflict,
    P,
    PredicateError,
    RuleEvaluatorRegisterSubjectError,
    RuleGroupMetaError,
    TargetModelConflict,
    site_metadata_rules,
)
from edc_metadata.models import CrfMetadata

from ..models import CrfOne, SubjectConsentV1
from ..visit_schedule import get_visit_schedule

fake = Faker()


test_datetime = datetime(2019, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC"))


class CrfRuleGroupWithSourceModel(CrfRuleGroup):
    """Specifies source model."""

    crfs_male = CrfRule(
        predicate=P("f1", "eq", "car"),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crffive", "crffour"],
    )

    crfs_female = CrfRule(
        predicate=P("f1", "eq", "bicycle"),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crfthree", "crftwo"],
    )

    class Meta:
        app_label = "edc_metadata"
        source_model = "edc_metadata.crfone"
        related_visit_model = "edc_visit_tracking.subjectvisit"


class CrfRuleGroupWithoutSourceModel(CrfRuleGroup):
    crfs_male = CrfRule(
        predicate=P("gender", "eq", MALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crffive", "crffour"],
    )

    crfs_female = CrfRule(
        predicate=P("gender", "eq", FEMALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crfthree", "crftwo"],
    )

    class Meta:
        app_label = "edc_metadata"
        related_visit_model = "edc_visit_tracking.subjectvisit"


class CrfRuleGroupWithoutExplicitReferenceModel(CrfRuleGroup):
    crfs_male = CrfRule(
        predicate=P("gender", "eq", MALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crffive", "crffour"],
    )

    crfs_female = CrfRule(
        predicate=P("gender", "eq", FEMALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crfthree", "crftwo"],
    )

    class Meta:
        app_label = "edc_metadata"
        source_model = "edc_metadata.crfone"
        related_visit_model = "edc_visit_tracking.subjectvisit"


class CrfRuleGroupGender(CrfRuleGroup):
    crfs_male = CrfRule(
        predicate=P("gender", "eq", MALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crffour", "crffive"],
    )

    crfs_female = CrfRule(
        predicate=P("gender", "eq", FEMALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crftwo", "crfthree"],
    )

    class Meta:
        app_label = "edc_metadata"
        related_visit_model = "edc_visit_tracking.subjectvisit"


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=test_datetime - relativedelta(years=3),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=test_datetime + relativedelta(years=3),
)
class TestMetadataRulesWithGender(TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        consent_v1 = ConsentDefinition(
            "edc_metadata.subjectconsentv1",
            version="1",
            start=test_datetime,
            end=test_datetime + relativedelta(years=3),
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
        # note crfs in visit schedule are all set to REQUIRED by default.
        _, self.schedule = site_visit_schedules.get_by_onschedule_model(
            "edc_metadata.onschedule"
        )

        site_metadata_rules.registry = {}
        site_metadata_rules.register(rule_group_cls=CrfRuleGroupGender)

    def enroll(self, gender=None):
        traveller = time_machine.travel(test_datetime)
        traveller.start()
        subject_identifier = fake.credit_card_number()
        subject_consent = SubjectConsentV1.objects.create(
            subject_identifier=subject_identifier,
            consent_datetime=get_utcnow(),
            gender=gender,
        )
        self.schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=subject_consent.consent_datetime,
        )
        self.appointment = Appointment.objects.get(
            subject_identifier=subject_identifier,
            visit_code=self.schedule.visits.first.code,
        )
        subject_visit = SubjectVisit.objects.create(
            appointment=self.appointment,
            subject_identifier=subject_identifier,
            report_datetime=self.appointment.appt_datetime,
            visit_code=self.appointment.visit_code,
            visit_code_sequence=self.appointment.visit_code_sequence,
            visit_schedule_name=self.appointment.visit_schedule_name,
            schedule_name=self.appointment.schedule_name,
            reason=SCHEDULED,
        )
        traveller.stop()
        return subject_visit

    def test_rules_with_source_model(self):
        for rule in CrfRuleGroupWithSourceModel._meta.options.get("rules"):
            self.assertEqual(rule.source_model, "edc_metadata.crfone")

    def test_rules_without_source_model(self):
        for rule in CrfRuleGroupWithoutSourceModel._meta.options.get("rules"):
            self.assertIsNone(rule.source_model)

    def test_rules_source_and_reference_model_is_none(self):
        subject_visit = self.enroll(MALE)
        for rule in CrfRuleGroupWithoutSourceModel._meta.options.get("rules"):
            with self.subTest(rule=rule):
                result = rule.run(subject_visit)
                if rule.name == "crfs_male":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crffive": REQUIRED,
                            "edc_metadata.crffour": REQUIRED,
                        },
                    )
                elif rule.name == "crfs_female":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crfthree": NOT_REQUIRED,
                            "edc_metadata.crftwo": NOT_REQUIRED,
                        },
                    )

    def test_rules_with_source_but_no_explicit_reference_model(self):
        subject_visit = self.enroll(MALE)
        for rule in CrfRuleGroupWithoutExplicitReferenceModel._meta.options.get("rules"):
            with self.subTest(rule=rule):
                self.assertIsNotNone(rule.source_model)
                result = rule.run(subject_visit)
                if rule.name == "crfs_male":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crffive": REQUIRED,
                            "edc_metadata.crffour": REQUIRED,
                        },
                    )
                elif rule.name == "crfs_female":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crfthree": NOT_REQUIRED,
                            "edc_metadata.crftwo": NOT_REQUIRED,
                        },
                    )

    def test_rules_if_no_source_model_instance(self):
        subject_visit = self.enroll(MALE)
        for rule in CrfRuleGroupWithSourceModel._meta.options.get("rules"):
            with self.subTest(rule=rule):
                result = rule.run(subject_visit)
                if rule.name == "crfs_male":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crffive": NOT_REQUIRED,
                            "edc_metadata.crffour": NOT_REQUIRED,
                        },
                    )
                elif rule.name == "crfs_female":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crfthree": NOT_REQUIRED,
                            "edc_metadata.crftwo": NOT_REQUIRED,
                        },
                    )

    def test_rules_run_if_source_f1_equals_car(self):
        subject_visit = self.enroll(MALE)
        CrfOne.objects.create(subject_visit=subject_visit, f1="car")
        for rule in CrfRuleGroupWithSourceModel._meta.options.get("rules"):
            with self.subTest(rule=rule):
                result = rule.run(subject_visit)
                if rule.name == "crfs_male":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crffive": REQUIRED,
                            "edc_metadata.crffour": REQUIRED,
                        },
                    )
                elif rule.name == "crfs_female":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crfthree": NOT_REQUIRED,
                            "edc_metadata.crftwo": NOT_REQUIRED,
                        },
                    )

    def test_rules_run_if_source_f1_equals_bicycle(self):
        subject_visit = self.enroll(MALE)
        CrfOne.objects.create(subject_visit=subject_visit, f1="bicycle")
        for rule in CrfRuleGroupWithSourceModel._meta.options.get("rules"):
            with self.subTest(rule=rule):
                result = rule.run(subject_visit)
                if rule.name == "crfs_male":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crffive": NOT_REQUIRED,
                            "edc_metadata.crffour": NOT_REQUIRED,
                        },
                    )
                elif rule.name == "crfs_female":
                    self.assertEqual(
                        result,
                        {
                            "edc_metadata.crfthree": REQUIRED,
                            "edc_metadata.crftwo": REQUIRED,
                        },
                    )

    def test_rules_run_requires_registered_subject(self):
        subject_visit = self.enroll(MALE)
        RegisteredSubject.objects.all().delete()
        for rule in CrfRuleGroupWithSourceModel._meta.options.get("rules"):
            self.assertRaises(RuleEvaluatorRegisterSubjectError, rule.run, subject_visit)

    def test_metadata_rules_run_male_required(self):
        subject_visit = self.enroll(gender=MALE)
        for target_model in [
            "edc_metadata.crffour",
            "edc_metadata.crffive",
        ]:
            with self.subTest(target_model=target_model):
                obj = CrfMetadata.objects.get(
                    model=target_model,
                    subject_identifier=subject_visit.subject_identifier,
                    visit_code=subject_visit.visit_code,
                )
                self.assertEqual(obj.entry_status, REQUIRED)

    def test_metadata_rules_run_female_required(self):
        subject_visit = self.enroll(gender=FEMALE)
        for target_model in [
            "edc_metadata.crftwo",
            "edc_metadata.crfthree",
        ]:
            with self.subTest(target_model=target_model):
                obj = CrfMetadata.objects.get(
                    model=target_model,
                    subject_identifier=subject_visit.subject_identifier,
                    visit_code=subject_visit.visit_code,
                )
                self.assertEqual(obj.entry_status, REQUIRED)

    def test_metadata_rules_run_female_not_required(self):
        subject_visit = self.enroll(gender=FEMALE)
        for target_model in [
            "edc_metadata.crffour",
            "edc_metadata.crffive",
        ]:
            with self.subTest(target_model=target_model):
                obj = CrfMetadata.objects.get(
                    model=target_model,
                    subject_identifier=subject_visit.subject_identifier,
                    visit_code=subject_visit.visit_code,
                )
                self.assertEqual(obj.entry_status, NOT_REQUIRED)

    def test_metadata_rules_run_male_not_required(self):
        subject_visit = self.enroll(gender=MALE)
        for target_model in [
            "edc_metadata.crftwo",
            "edc_metadata.crfthree",
        ]:
            with self.subTest(target_model=target_model):
                obj = CrfMetadata.objects.get(
                    model=target_model,
                    subject_identifier=subject_visit.subject_identifier,
                    visit_code=subject_visit.visit_code,
                )
                self.assertEqual(obj.entry_status, NOT_REQUIRED)

    def test_rule_group_metadata_objects(self):
        subject_visit = self.enroll(gender=MALE)
        _, metadata_objects = CrfRuleGroupGender().evaluate_rules(related_visit=subject_visit)
        self.assertEqual(metadata_objects.get("edc_metadata.crffour").entry_status, REQUIRED)
        self.assertEqual(metadata_objects.get("edc_metadata.crffive").entry_status, REQUIRED)
        self.assertEqual(
            metadata_objects.get("edc_metadata.crftwo").entry_status, NOT_REQUIRED
        )
        self.assertEqual(
            metadata_objects.get("edc_metadata.crfthree").entry_status,
            NOT_REQUIRED,
        )

    def test_rule_group_rule_results(self):
        subject_visit = self.enroll(gender=MALE)
        rule_results, _ = CrfRuleGroupGender().evaluate_rules(related_visit=subject_visit)
        self.assertEqual(
            rule_results["CrfRuleGroupGender.crfs_male"].get("edc_metadata.crffour"),
            REQUIRED,
        )
        self.assertEqual(
            rule_results["CrfRuleGroupGender.crfs_male"].get("edc_metadata.crffive"),
            REQUIRED,
        )
        self.assertEqual(
            rule_results["CrfRuleGroupGender.crfs_female"].get("edc_metadata.crftwo"),
            NOT_REQUIRED,
        )
        self.assertEqual(
            rule_results["CrfRuleGroupGender.crfs_female"].get("edc_metadata.crfthree"),
            NOT_REQUIRED,
        )

    def test_bad_rule_group_target_model_cannot_also_be_source_model(self):
        site_metadata_rules.registry = {}
        subject_visit = self.enroll(gender=MALE)

        class BadCrfRuleGroup(CrfRuleGroup):
            crfs_male = CrfRule(
                predicate=P("f1", "eq", "car"),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crfone"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfone"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        self.assertRaises(
            CrfRuleModelConflict, BadCrfRuleGroup().evaluate_rules, related_visit=subject_visit
        )

    def test_rule_group_target_model_cannot_be_visit_model(self):
        site_metadata_rules.registry = {}

        subject_visit = self.enroll(gender=MALE)

        class BadCrfRuleGroup(CrfRuleGroup):
            rule = CrfRule(
                predicate=P("f1", "eq", "car"),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["subjectvisit"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfone"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        self.assertRaises(
            TargetModelConflict, BadCrfRuleGroup().evaluate_rules, related_visit=subject_visit
        )

    def test_bad_predicate_blah_is_not_an_operator(self):
        try:

            class BadCrfRuleGroup(CrfRuleGroup):
                rule = CrfRule(
                    predicate=P("f1", "blah", "car"),
                    consequence=REQUIRED,
                    alternative=NOT_REQUIRED,
                    target_models=["crftwo"],
                )

                class Meta:
                    app_label = "edc_metadata"
                    source_model = "edc_metadata.crfone"
                    related_visit_model = "edc_visit_tracking.subjectvisit"

        except PredicateError:
            pass
        else:
            self.fail("PredicateError not raised.")

    def test_predicate_pf(self):
        def func(f1, f2):
            return True if f1 == "f1" and f2 == "f2" else False

        class MyCrfRuleGroup(CrfRuleGroup):
            rule = CrfRule(
                predicate=PF("f1", "f2", func=func),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crftwo"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfone"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        site_metadata_rules.registry = {}
        site_metadata_rules.register(MyCrfRuleGroup)
        subject_visit = self.enroll(gender=MALE)

        MyCrfRuleGroup().evaluate_rules(related_visit=subject_visit)

        obj = CrfMetadata.objects.get(
            model="edc_metadata.crftwo",
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
        )
        self.assertEqual(obj.entry_status, NOT_REQUIRED)

    @override_settings(DEBUG=True)
    def test_predicate_pf2(self):
        """Asserts entry status set to alternative if source model
        exists but does not meet criteria.
        """

        def func(f1, f2):
            return f1 == "f1_value" and f2 == "f2_value"

        class MyCrfRuleGroup(CrfRuleGroup):
            rule = CrfRule(
                predicate=PF("f1", "f2", func=func),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crftwo"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfone"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        site_metadata_rules.registry = {}
        site_metadata_rules.register(MyCrfRuleGroup)
        subject_visit = self.enroll(gender=MALE)
        obj = CrfMetadata.objects.get(
            model="edc_metadata.crftwo",
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
        )
        self.assertEqual(obj.entry_status, NOT_REQUIRED)
        CrfOne.objects.create(subject_visit=subject_visit, f1="blah", f2="f2_value")
        self.assertFalse(func("blah", "f2_value"))
        # MyCrfRuleGroup().evaluate_rules(related_visit=subject_visit)
        obj = CrfMetadata.objects.get(
            model="edc_metadata.crftwo",
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
        )

        self.assertEqual(obj.entry_status, NOT_REQUIRED)

    def test_predicate_pf3(self):
        """Asserts entry status set to consequence if source model
        exists and meets criteria.
        """

        def func(f1, f2):
            return True if f1 == "f1" and f2 == "f2" else False

        class MyCrfRuleGroup(CrfRuleGroup):
            rule = CrfRule(
                predicate=PF("f1", "f2", func=func),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crftwo"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfone"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        site_metadata_rules.registry = {}
        subject_visit = self.enroll(gender=MALE)
        CrfOne.objects.create(subject_visit=subject_visit, f1="f1", f2="f2")
        MyCrfRuleGroup().evaluate_rules(related_visit=subject_visit)

        obj = CrfMetadata.objects.get(
            model="edc_metadata.crftwo",
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
        )
        self.assertEqual(obj.entry_status, REQUIRED)

    def test_p_repr(self):
        p = P("blah", "eq", "car")
        self.assertTrue(repr(p))

    def test_pf_repr(self):
        def func(f1, f2):
            return True if f1 == "f1" and f2 == "f2" else False

        pf = PF("blah", "f2", func=func)
        self.assertTrue(repr(pf))

    def test_rule_repr(self):
        rule = CrfRule(
            predicate=P("f1", "eq", "car"),
            consequence=REQUIRED,
            alternative=NOT_REQUIRED,
            target_models=["crftwo"],
        )
        self.assertTrue(repr(rule))

    def test_rule_group_meta_repr(self):
        class MyCrfRuleGroup(CrfRuleGroup):
            rule = CrfRule(
                predicate=P("f1", "eq", "car"),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crftwo"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfmissingmanager"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        self.assertTrue(repr(MyCrfRuleGroup()._meta))

    def test_sub_class_rule_group(self):
        class MyCrfRuleGroup(CrfRuleGroup):
            rule1 = CrfRule(
                predicate=P("f1", "eq", "car"),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crftwo"],
            )

            class Meta:
                abstract = True

        class NewCrfRuleGroup(CrfRuleGroup):
            rule2 = CrfRule(
                predicate=P("f1", "eq", "car"),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crfthree"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_metadata.crfmissingmanager"
                related_visit_model = "edc_visit_tracking.subjectvisit"

        self.assertTrue(len(NewCrfRuleGroup()._meta.options.get("rules")), 2)

    def test_rule_group_missing_meta(self):
        try:

            class MyCrfRuleGroup(CrfRuleGroup):
                rule1 = CrfRule(
                    predicate=P("f1", "eq", "car"),
                    consequence=REQUIRED,
                    alternative=NOT_REQUIRED,
                    target_models=["crftwo"],
                )

        except AttributeError:
            pass
        else:
            self.fail("AttributeError not raised.")

    def test_rule_group_invalid_meta_option(self):
        try:

            class MyCrfRuleGroup(CrfRuleGroup):
                rule1 = CrfRule(
                    predicate=P("f1", "eq", "car"),
                    consequence=REQUIRED,
                    alternative=NOT_REQUIRED,
                    target_models=["crftwo"],
                )

                class Meta:
                    app_label = "edc_metadata"
                    source_model = "edc_metadata.crfmissingmanager"
                    related_visit_model = "edc_visit_tracking.subjectvisit"
                    blah = "blah"

        except RuleGroupMetaError:
            pass
        else:
            self.fail("AttributeError not raised.")
