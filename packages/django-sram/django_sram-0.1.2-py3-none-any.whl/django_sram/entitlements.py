import re
from typing import AnyStr
from re import Pattern

from django.conf import settings

DEFAULT_ENTITLEMENT_RE = r"^urn:mace:surf\.nl:sram:group:(?P<organisation>[^:\s]+)(?P<collaboration>:[^:\s]+)?(?P<group>:[\S]+)?$"
ENTITLEMENT_RE = re.compile(
    getattr(settings, "SRAM_ENTITLEMENT_REGEX", DEFAULT_ENTITLEMENT_RE)
)


def get_collaborations(
    entitlements: list[str], entitlement_regex_pattern: Pattern[AnyStr] = ENTITLEMENT_RE
) -> list[str]:
    """Convert entitlements into a list of unique collaboration names.
    :param entitlements: List of entitlement URNs from SRAM.
    :param entitlement_regex_pattern: Optional regex pattern to extract the collaborations.
                                      Defaults to SRAM_ENTITLEMENT_REGEX from settings if it is set, otherwise:
                                      `'urn:mace:surf.nl:sram:group:<organisation>:<collaboration>:<group>'`
                                      `r"^urn:mace:surf\\.nl:sram:group:(?P<organisation>[^:\\s]+)(?P<collaboration>:[^:\\s]+)?(?P<group>:[\\S]+)?$"`
    :return: A deduplicated list of collaboration names, stripped of their leading colon.
    """
    collaborations = []
    for entitlement in entitlements:
        if match := entitlement_regex_pattern.match(entitlement):
            if collaboration := match.group("collaboration"):
                collaborations.append(collaboration[1:])
    return list(set(collaborations))


def get_groups_in_collaboration(
    collaboration: str,
    entitlements: list[str],
    entitlement_regex_pattern: Pattern[AnyStr] = ENTITLEMENT_RE,
) -> list[str]:
    """Get all groups for a given collaboration
    :param entitlement_regex_pattern: Optional regex pattern to extract the collaborations. Defaults to ENTITLEMENT_RE
    :param collaboration: Collaboration name
    :param entitlements: List of entitlement URNs from SRAM.
    """
    groups = []
    for entitlement in entitlements:
        if re_match := entitlement_regex_pattern.match(entitlement):
            if collab := re_match.group("collaboration"):
                if collab.endswith(collaboration):
                    if group := re_match.group("group"):
                        groups.append(group[1:])
    return groups
