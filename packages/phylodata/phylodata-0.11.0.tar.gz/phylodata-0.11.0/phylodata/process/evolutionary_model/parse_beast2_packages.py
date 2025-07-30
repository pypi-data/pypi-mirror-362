from abc import ABC, abstractmethod
from typing import Any, Optional
from xml.etree.ElementTree import ElementTree

from phylodata.data_types import ModelType, SampleType
from phylodata.process.utils.beast2_xml_utils import get_attribute


class Beast2PackageParser(ABC):
    """An abstract base class for parsing BEAST 2 packages."""

    def is_used(self, beast2_xml: ElementTree) -> bool:
        """Returns true if the package is detected in the given BEAST2 xml.
        Checks the top-level namespaces and the spec attribute of all elements."""
        root = beast2_xml.getroot()
        if root is None:
            return False

        # check namespaces

        namespaces = get_attribute(root, "namespace", "")
        namespaces = namespaces.split(":")

        package_namespace = self.get_namespace()

        if namespaces and any(
            namespace == package_namespace
            or namespace.startswith(f"{package_namespace}.")
            for namespace in namespaces
        ):
            return True

        # check specs

        elements_with_spec = root.findall(".//*[@spec]")
        spec_values = [get_attribute(elem, "spec") for elem in elements_with_spec]

        for spec in spec_values:
            if not spec:
                continue

            # for the following cases: assume package_namespace = "babel.distribution"

            if spec == package_namespace:
                return True

            if spec.startswith(f"{package_namespace}."):
                # e.g. spec = "babel.distribution.Normal"
                return True

            if any(
                f"{namespace}.{spec}" == package_namespace for namespace in namespaces
            ):
                # e.g. namespace = "babel" and spec = "distribution"
                return True

            if any(
                f"{namespace}.{spec}".startswith(f"{package_namespace}.")
                for namespace in namespaces
            ):
                # e.g. namespace = "babel" and spec = "distribution.Normal"
                return True

        return False

    @abstractmethod
    def get_name(self) -> str:
        """Returns a human-readable name of the BEAST 2 package."""
        raise NotImplementedError

    @abstractmethod
    def get_description(self) -> str:
        """Returns a human-readable get_description of the BEAST 2 package."""
        raise NotImplementedError

    @abstractmethod
    def get_type(self) -> ModelType:
        """Returns the type of the BEAST 2 package."""
        raise NotImplementedError

    @abstractmethod
    def get_namespace(self) -> str:
        """Returns the namespace of the BEAST 2 package."""
        raise NotImplementedError

    @abstractmethod
    def get_documentation_url(self) -> str:
        """Returns the URL to the human-readable package website."""
        raise NotImplementedError

    def get_parameters(self, beast2_xml: ElementTree) -> dict[str, Any]:
        """Extracts potential package parameters from the BEAST 2 xml configuration."""
        return {}

    def suggest_sample_type(self) -> Optional[SampleType]:
        """If the package usage suggests a specific sample type, returns it. For example,
        a model for phylogenetic language trees would return SampleType.LANGUAGE."""
        return None


class GTRParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "GTR"

    def get_description(self) -> str:
        return "General Time Reversible model of nucleotide evolution"

    def get_namespace(self) -> str:
        return "beast.evolution.substitutionmodel.GTR"

    def get_type(self) -> ModelType:
        return ModelType.SUBSTITUTION_MODEL

    def get_documentation_url(self) -> str:
        return (
            "https://www.beast2.org/xml/beast.base.evolution.substitutionmodel.GTR.html"
        )


class HKYParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "HKY"

    def get_description(self) -> str:
        return "HKY85 (Hasegawa, Kishino & Yano, 1985) substitution model of nucleotide evolution"

    def get_namespace(self) -> str:
        return "beast.evolution.substitutionmodel.HKY"

    def get_type(self) -> ModelType:
        return ModelType.SUBSTITUTION_MODEL

    def get_documentation_url(self) -> str:
        return (
            "https://www.beast2.org/xml/beast.base.evolution.substitutionmodel.HKY.html"
        )


class StrictClockParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "Strict Clock Model"

    def get_description(self) -> str:
        return "Defines a mean rate for each branch in the beast.tree."

    def get_namespace(self) -> str:
        return "beast.evolution.branchratemodel.StrictClockModel"

    def get_type(self) -> ModelType:
        return ModelType.CLOCK_MODEL

    def get_documentation_url(self) -> str:
        return "https://www.beast2.org/xml/beast.base.evolution.branchratemodel.StrictClockModel.html"


class RelaxedClockParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "Relaxed Clock Model"

    def get_description(self) -> str:
        return "Defines an uncorrelated relaxed molecular clock."

    def get_namespace(self) -> str:
        return "beast.evolution.branchratemodel.UCRelaxedClockModel"

    def get_type(self) -> ModelType:
        return ModelType.CLOCK_MODEL

    def get_documentation_url(self) -> str:
        return "https://www.beast2.org/xml/beast.base.evolution.branchratemodel.UCRelaxedClockModel.html"


class TreeLikelihoodParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "Generic TreeLikelihood"

    def get_description(self) -> str:
        return "Calculates the probability of sequence data on a tree given a site and substitution model using a variant of the 'peeling algorithm'."

    def get_namespace(self) -> str:
        return "beast.evolution.likelihood.TreeLikelihood"

    def get_type(self) -> ModelType:
        return ModelType.TREE_LIKELIHOOD

    def get_documentation_url(self) -> str:
        return "https://www.beast2.org/xml/beast.base.evolution.likelihood.TreeLikelihood.html"


class BDMMPrimeParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "BDMM-Prime"

    def get_description(self) -> str:
        return "BDMM-Prime is a BEAST 2 package for performing phylodynamic inference under a variety of linear birth-death-sampling models with/without types."

    def get_namespace(self) -> str:
        return "bdmmprime"

    def get_type(self) -> ModelType:
        return ModelType.TREE_LIKELIHOOD

    def get_documentation_url(self) -> str:
        return "https://tgvaughan.github.io/BDMM-Prime/"


class BabelParser(Beast2PackageParser):
    def get_name(self) -> str:
        return "Babel"

    def get_description(self) -> str:
        return "BABEL = BEAST analysis backing effective linguistics"

    def get_namespace(self) -> str:
        return "babel"

    def get_type(self) -> ModelType:
        return ModelType.OTHER

    def get_documentation_url(self) -> str:
        return "https://github.com/rbouckaert/Babel"

    def get_parameters(self, beast2_xml: ElementTree) -> dict[str, Any]:
        return {}

    def suggest_sample_type(self) -> Optional[SampleType]:
        return SampleType.LANGUAGE


BEAST2_PACKAGE_PARSERS: list[Beast2PackageParser] = [
    GTRParser(),
    HKYParser(),
    StrictClockParser(),
    RelaxedClockParser(),
    TreeLikelihoodParser(),
    BDMMPrimeParser(),
    BabelParser(),
]
BEAST2_PACKAGE_PARSERS_PER_NAME: dict[str, Beast2PackageParser] = {
    parser.get_name(): parser for parser in BEAST2_PACKAGE_PARSERS
}
