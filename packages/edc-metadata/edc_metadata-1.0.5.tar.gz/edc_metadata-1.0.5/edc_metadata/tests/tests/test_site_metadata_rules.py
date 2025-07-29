from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django.test import TestCase, override_settings
from edc_consent import site_consents
from edc_consent.consent_definition import ConsentDefinition
from edc_constants.constants import FEMALE, MALE
from edc_facility.import_holidays import import_holidays

from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata.metadata_rules import (
    CrfRule,
    CrfRuleGroup,
    P,
    RegisterRuleGroupError,
    SiteMetadataNoRulesError,
    SiteMetadataRulesAlreadyRegistered,
    register,
    site_metadata_rules,
)

test_datetime = datetime(2019, 6, 11, 8, 00, tzinfo=ZoneInfo("UTC"))


class RuleGroupWithoutRules(CrfRuleGroup):
    class Meta:
        app_label = "edc_metadata"
        source_model = "edc_visit_tracking.subjectvisit"


class RuleGroupWithRules(CrfRuleGroup):
    rule1 = CrfRule(
        predicate=P("gender", "eq", MALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crfone", "crftwo"],
    )

    class Meta:
        app_label = "edc_metadata"
        source_model = "edc_visit_tracking.subjectvisit"


class RuleGroupWithRules2(CrfRuleGroup):
    rule1 = CrfRule(
        predicate=P("gender", "eq", MALE),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=["crfone", "crftwo"],
    )

    class Meta:
        app_label = "edc_metadata"
        source_model = "edc_visit_tracking.subjectvisit"


@override_settings(
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=test_datetime - relativedelta(years=3),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=test_datetime + relativedelta(years=3),
)
class TestSiteMetadataRules(TestCase):
    @classmethod
    def setUpTestData(cls):
        import_holidays()

    def setUp(self):
        site_metadata_rules.registry = {}
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

    def test_register_rule_group_no_rules_raises_on_register(self):
        self.assertRaises(
            SiteMetadataNoRulesError,
            site_metadata_rules.register,
            RuleGroupWithoutRules,
        )

    def test_register_rule_group_with_rule(self):
        try:
            site_metadata_rules.register(RuleGroupWithRules)
        except SiteMetadataNoRulesError:
            self.fail("SiteMetadataNoRulesError unexpectedly raised.")

    def test_register_rule_group_get_rule_groups_for_app_label(self):
        site_metadata_rules.register(RuleGroupWithRules)
        rule_groups = site_metadata_rules.rule_groups.get("edc_metadata")
        self.assertEqual(rule_groups, [RuleGroupWithRules])

    def test_register_rule_group_register_more_than_one_rule_group(self):
        site_metadata_rules.register(RuleGroupWithRules)
        site_metadata_rules.register(RuleGroupWithRules2)
        rule_groups = site_metadata_rules.rule_groups.get("edc_metadata")
        self.assertEqual(rule_groups, [RuleGroupWithRules, RuleGroupWithRules2])

    def test_register_twice_raises(self):
        site_metadata_rules.register(rule_group_cls=RuleGroupWithRules)
        self.assertRaises(
            SiteMetadataRulesAlreadyRegistered,
            site_metadata_rules.register,
            RuleGroupWithRules,
        )

    def test_rule_group_repr(self):
        repr(RuleGroupWithRules())
        str(RuleGroupWithRules())

    def test_register_decorator(self):
        @register()
        class RuleGroupWithRules(CrfRuleGroup):
            rule1 = CrfRule(
                predicate=P("gender", "eq", MALE),
                consequence=REQUIRED,
                alternative=NOT_REQUIRED,
                target_models=["crfone", "crftwo"],
            )

            class Meta:
                app_label = "edc_metadata"
                source_model = "edc_visit_tracking.subjectvisit"

        self.assertIn("edc_metadata", site_metadata_rules.registry)

    def test_register_decorator_raises(self):
        try:

            @register()
            class RuleGroupWithRules:
                class Meta:
                    app_label = "edc_metadata"
                    source_model = "edc_visit_tracking.subjectvisit"

        except RegisterRuleGroupError:
            pass
        else:
            self.fail("RegisterRuleGroupError unexpectedly not raised.")
