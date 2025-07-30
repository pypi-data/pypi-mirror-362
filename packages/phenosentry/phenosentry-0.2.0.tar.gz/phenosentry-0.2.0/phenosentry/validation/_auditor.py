import enum
import typing

import hpotk
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket
from phenopackets.schema.v2.phenopackets_pb2 import Cohort
from stairval.notepad import Notepad

from ._api import PhenopacketAuditor, CohortAuditor
from ._checks import NoUnwantedCharactersCheck, DeprecatedTermIdCheck, UniqueIdsCheck


class AuditorLevel(enum.Enum):
    """
       Enum representing different levels of auditing.

       Attributes:
           DEFAULT (str): Represents the default auditing level.
           STRICT (str): Represents the strict auditing level.
    """
    DEFAULT = "default"
    STRICT = "strict"

    def __init__(self, level: str,):
        self.level = level

    def __str__(self):
        return f"AuditorLevel(level={self.level})"

    def __repr__(self):
        return self.__str__()


class DefaultPhenopacketAuditor(PhenopacketAuditor):
    """
      Default implementation of the `PhenopacketAuditor`.

      This auditor applies a series of checks to a `PhenopacketInfo` object and logs the results
      in a `Notepad`.

      Attributes:
          _checks (tuple): A tuple of `PhenopacketAuditor` checks to be applied.
          _id (str): The unique identifier for this auditor.
    """
    def __init__(
            self,
            checks: typing.Iterable[PhenopacketAuditor],
            id: str = "DefaultPhenopacketAuditor"
    ):
        self._checks = tuple(checks)
        self._id = id

    def audit(
            self,
            item: Phenopacket,
            notepad: Notepad,
    ):
        for check in self._checks:
            sub_notepad = notepad.add_subsection(check.id())
            check.audit(
                item=item,
                notepad=sub_notepad,
            )

    def id(self) -> str:
        return self._id

class DefaultCohortAuditor(CohortAuditor):
    """
      Default implementation of the `CohortAuditor`.

      This auditor applies a series of checks to a `Cohort` and logs the results
      in a `Notepad`.

      Attributes:
          _checks (tuple): A tuple of `CohortAuditor` or `PhenopacketAuditor` checks to be applied.
          _id (str): The unique identifier for this auditor.
    """

    def __init__(
            self,
            checks: typing.Iterable[CohortAuditor | PhenopacketAuditor],
            id: str = "DefaultCohortAuditor"
    ):
        self._checks = tuple(checks)
        self._id = id

    def audit(
            self,
            item: Cohort,
            notepad: Notepad,
    ):
        for check in self._checks:
            if isinstance(check, PhenopacketAuditor):
                sub_notepad = notepad.add_subsection(check.id())
                for phenopacket in item.members:
                    check.audit(
                        item=phenopacket,
                        notepad=sub_notepad,
                    )
            else:
                check.audit(
                    item=item,
                    notepad=notepad,
                )

    def id(self) -> str:
        return self._id

def get_phenopacket_auditor(level = AuditorLevel.DEFAULT) -> PhenopacketAuditor :
    """
     Creates and returns a `PhenopacketAuditor` with default checks.

     Args:
         level (AuditorLevel): The auditing level. Defaults to `AuditorLevel.DEFAULT`.

     Returns:
         PhenopacketAuditor: An instance of `DefaultPhenopacketAuditor` configured with default checks.
     """
    store = hpotk.configure_ontology_store()
    hpo = store.load_hpo()
    checks = (NoUnwantedCharactersCheck.no_whitespace(),)
    if level == AuditorLevel.STRICT:
        checks += (DeprecatedTermIdCheck(hpo),)
        return DefaultPhenopacketAuditor(id="StrictPhenopacketAuditor", checks=checks)
    return DefaultPhenopacketAuditor(checks=checks)

def get_cohort_auditor() -> CohortAuditor:
    """
    Creates and returns a `CohortAuditor` with default checks.

    Returns:
        CohortAuditor: An instance of `DefaultCohortAuditor` configured with default checks.
    """
    checks = (get_phenopacket_auditor(), UniqueIdsCheck())
    return DefaultCohortAuditor(checks=checks)