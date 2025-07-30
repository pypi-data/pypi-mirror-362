from io import BytesIO

from phylodata.process.evolutionary_model.parse_evolutionary_model import (
    parse_evolutionary_model,
)


def to_bytes_io(text: str):
    bytesio = BytesIO(bytes(text, "ascii"))
    bytesio.name = "Test"
    return bytesio


def test_detect_babel_in_specs_with_attributes():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                    id="treeLikelihood.ringe"
                    spec="babel.evolution.likelihood.ALSTreeLikelihood"
                    tree="@Tree.t:ringe"
                    useAmbiguities="true"
                >
                <observationprocess
                        id="AnyTipObservationProcess.0"
                        spec="babel.evolution.likelihood.AnyTipObservationProcess"
                        integrateGainRate="true"
                        mu="@deathRate.SDollo"
                        tree="@Tree.t:ringe"
                    >
                </observationprocess>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "Babel"


def test_detect_babel_in_specs_with_tags():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                    id="treeLikelihood.ringe"
                    tree="@Tree.t:ringe"
                    useAmbiguities="true"
                >
                <spec>babel.evolution.likelihood.ALSTreeLikelihood</spec>
                <observationprocess
                        id="AnyTipObservationProcess.0"
                        spec="babel.evolution.likelihood.AnyTipObservationProcess"
                        integrateGainRate="true"
                        mu="@deathRate.SDollo"
                        tree="@Tree.t:ringe"
                    >
                </observationprocess>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "Babel"


def test_detect_babel_in_specs_with_input_tag():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                    id="treeLikelihood.ringe"
                    tree="@Tree.t:ringe"
                    useAmbiguities="true"
                >
                <input name="spec">babel.evolution.likelihood.ALSTreeLikelihood</input>
                <observationprocess
                        id="AnyTipObservationProcess.0"
                        spec="babel.evolution.likelihood.AnyTipObservationProcess"
                        integrateGainRate="true"
                        mu="@deathRate.SDollo"
                        tree="@Tree.t:ringe"
                    >
                </observationprocess>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "Babel"


def test_detect_babel_in_namespace():
    file = to_bytes_io("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <beast namespace="beast.core:babel.evolution.likelihood" required="BEAST.base v2.7.7" version="2.7">
        <data></data>
        <run>
            <distribution
                    id="treeLikelihood.ringe"
                    spec="ALSTreeLikelihood"
                    tree="@Tree.t:ringe"
                    useAmbiguities="true"
                >
                <observationprocess
                        id="AnyTipObservationProcess.0"
                        spec="AnyTipObservationProcess"
                        integrateGainRate="true"
                        mu="@deathRate.SDollo"
                        tree="@Tree.t:ringe"
                    >
                </observationprocess>
            </distribution>
        </run>
    </beast>""")
    model = parse_evolutionary_model(file)

    assert model
    assert len(model) == 1
    assert model[0].name == "Babel"
