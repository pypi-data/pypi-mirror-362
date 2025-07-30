import typing

from collections import Counter, defaultdict

from stairval.notepad import Notepad
from hpotk import MinimalOntology
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket, Cohort

from ._api import PhenopacketAuditor, CohortAuditor


# Cohort Level Checks
class UniqueIdsCheck(CohortAuditor):
    """
    A check to ensure that all phenopacket IDs within a cohort are unique.

    Methods:
        id() -> str: Returns the unique identifier for this check.
        audit(item: CohortInfo, notepad: Notepad): Performs the uniqueness check on the cohort.
    """

    def id(self) -> str:
        return "unique_ids_check"

    def audit(
        self,
        item: Cohort,
        notepad: Notepad,
    ):
        id_counter = Counter()
        pp_id2cohort = defaultdict(set)
        for pp in item.members:
            pp_id2cohort[pp.id].add(item.id)
            id_counter[pp.id] += 1

        repeated = {pp_id: count for pp_id, count in id_counter.items() if count > 1}

        for pp_id, count in repeated.items():
            msg = f"`{pp_id}` is not unique in cohort `{next(iter(pp_id2cohort[pp_id]))}`"
            notepad.add_error(msg)

# Phenopacket Level Checks
class NoUnwantedCharactersCheck(PhenopacketAuditor):
    """
     A check to ensure that phenopacket elements do not include unwanted characters (e.g., whitespace).

     Methods:
         no_whitespace(whitespaces: typing.Iterable[str]) -> NoUnwantedCharactersCheck:
             Creates an instance of the check with specified unwanted characters.
         id() -> str: Returns the unique identifier for this check.
         audit(item: PhenopacketInfo, notepad: Notepad): Performs the unwanted character check on the phenopacket.
     """

    @staticmethod
    def no_whitespace(
        whitespaces: typing.Iterable['str'] = ("\t", "\n", "\r\n"),
    ) -> "NoUnwantedCharactersCheck":
        return NoUnwantedCharactersCheck(whitespaces)

    def __init__(
        self,
        unwanted: typing.Iterable[str],
    ):
        self._unwanted = set(unwanted)

    def id(self) -> str:
        return "unwanted_characters_check"

    def audit(
        self,
        item: Phenopacket,
        notepad: Notepad,
    ):
            pp_pad = notepad.add_subsection(self.id())
            self._check_unwanted_characters(item.id, pp_pad.add_subsection("id"))
            _, subject_id_pad = pp_pad.add_subsections("subject", "id")
            self._check_unwanted_characters(item.subject.id, subject_id_pad)

            # Disease name in diseases and variant interpretations
            disease_pad = pp_pad.add_subsection("disease")
            for i, disease in enumerate(item.diseases):
                _, _, label_pad = disease_pad.add_subsections(f"#{i}", "term", "label")
                self._check_unwanted_characters(disease.term.label, label_pad)

            interpretation_pad = pp_pad.add_subsection("interpretations")
            for i, interpretation in enumerate(item.interpretations):
                id_pad = interpretation_pad.add_subsection("id")
                self._check_unwanted_characters(interpretation.id, id_pad)
                _, _, label_pad = interpretation_pad.add_subsections("diagnosis", "disease", "label")
                self._check_unwanted_characters(
                    interpretation.diagnosis.disease.label, label_pad
                )

            # PubMed title
            _, ers_pad = pp_pad.add_subsections("meta_data", "external_references")
            for i, er in enumerate(item.meta_data.external_references):
                _, er_pad = ers_pad.add_subsections(f"#{i}", "description")
                self._check_unwanted_characters(er.description, er_pad)


    def _check_unwanted_characters(
        self,
        value: str,
        notepad: Notepad,
    ):
        for ch in value:
            if ch in self._unwanted:
                notepad.add_error(f"`{value}` includes a forbidden character `{ch}`")


class DeprecatedTermIdCheck(PhenopacketAuditor):
    """
    A check to ensure that all term IDs in the phenopackets do not use deprecated identifiers.

    Methods:
        id() -> str: Returns the unique identifier for this check.
        audit(item: PhenopacketInfo, notepad: Notepad): Performs the deprecated term ID check on the phenopacket.
    """

    def __init__(self, ontology: MinimalOntology):
        self.ontology = ontology

    def id(self) -> str:
        return "deprecated_term_id_check"

    def audit(
        self,
        item: Phenopacket,
        notepad: Notepad,
    ):
        pp_pad = notepad.add_subsection(self.id())
        for phenotype in item.phenotypic_features:
            term = self.ontology.get_term(phenotype.type.id)
            if term is not None and (term.is_obsolete or term.identifier.value != phenotype.type.id):
                msg = f"`{item.id}` has a deprecated term ID `{phenotype.type.id}`"
                pp_pad.add_error(msg)


