from io import BytesIO

from phylodata.process.evolutionary_model.parse_evolutionary_model import (
    parse_evolutionary_model,
)


def to_bytes_io(text: str):
    bytesio = BytesIO(bytes(text, "ascii"))
    bytesio.name = "Test"
    return bytesio


def test_detect_hky_with_no_namespace():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                spec="ThreadedTreeLikelihood"
            >
                <substModel id="HKY" spec="beast.evolution.substitutionmodel.HKY" kappa="@kappa">
                    <frequencies id="Frequencies" spec="Frequencies" frequencies="@frequencies"/>
                </substModel>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "HKY"


def test_detect_hky_with_full_namespace():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core:beast.evolution.substitutionmodel" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                spec="ThreadedTreeLikelihood"
            >
                <substModel id="HKY" spec="HKY" kappa="@kappa">
                    <frequencies id="Frequencies" spec="Frequencies" frequencies="@frequencies"/>
                </substModel>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "HKY"
