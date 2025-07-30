from io import BytesIO

from phylodata.process.evolutionary_model.parse_evolutionary_model import (
    parse_evolutionary_model,
)


def to_bytes_io(text: str):
    bytesio = BytesIO(bytes(text, "ascii"))
    bytesio.name = "Test"
    return bytesio


def test_detect_relaxed_clock_with_no_namespace():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                spec="ThreadedTreeLikelihood"
            >
                <branchRateModel clock.rate="@ucldMean.c:penguins_dna" id="RelaxedClock.c:penguins_dna" rateCategories="@rateCategories.c:penguins_dna" spec="beast.evolution.branchratemodel.UCRelaxedClockModel" tree="@Tree.t:tree">
                    <LogNormal S="@ucldStdev.c:penguins_dna" id="LogNormalDistributionModel.c:clock_dna" meanInRealSpace="true" name="distr">
                        <parameter estimate="false" id="Mrelaxed_dna" lower="0.0" name="M" upper="1.0">1.0</parameter>
                    </LogNormal>
                </branchRateModel>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "Relaxed Clock Model"
