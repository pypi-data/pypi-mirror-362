from phylodata.data_types import ClassificationEntry, DataType, Sample, SampleType
from phylodata.errors import BlastError
from phylodata.process.samples.run_blast import (
    extract_taxon_ids,
    run_blast,
)
from phylodata.process.samples.taxon_classification import look_up_taxon_classification

MAX_SEQ_LENGTH_CONSIDERED = 160


def add_protein_metadata(samples: list[Sample]) -> list[Sample]:
    """Tries to add metadata to all samples for which we have protein
    sequences."""
    # collect all protein sequences

    protein_sequences: list[str] = []
    protein_sequence_idx: list[int] = []

    for idx, sample in enumerate(samples):
        if sample.type != SampleType.UNKNOWN:
            continue

        for data in sample.sample_data:
            if data.type == DataType.AMINO_ACIDS:
                protein_sequences.append("".join(c for c in data.data if c.isalpha()))
                protein_sequence_idx.append(idx)
                break  # we only need one sequence per sample

    # fetch the protein classifications

    classification = fetch_protein_classifications(protein_sequences)

    # decide on the tree type

    species = set(
        [
            classification[0].scientific_name
            for classification in classification
            if classification
        ]
    )
    tree_type = SampleType.SPECIES if 1 < len(species) > 1 else SampleType.CELLS

    # add the classifications to the samples

    for idx, classification in zip(protein_sequence_idx, classification):
        if classification:
            samples[idx].classification = classification
            samples[idx].scientific_name = classification[0].scientific_name
            samples[idx].common_name = classification[0].common_name
            samples[idx].type = tree_type

    return samples


def fetch_protein_classifications(
    sequences: list[str],
) -> list[list[ClassificationEntry] | None]:
    if not sequences:
        return []

    blast_params = {
        "CMD": "Put",
        "PROGRAM": "blastp",
        "DATABASE": "nr",
        "HITLIST_SIZE": 1,
    }

    try:
        blast_results = run_blast(sequences, blast_params, MAX_SEQ_LENGTH_CONSIDERED)
    except BlastError:
        return [None] * len(sequences)

    taxon_ids = extract_taxon_ids(blast_results)

    classifications: list[list[ClassificationEntry] | None] = []

    for taxon_id in taxon_ids:
        if taxon_id:
            try:
                classifications.append(look_up_taxon_classification(taxon_id))
            except Exception:
                classifications.append(None)
        else:
            classifications.append(None)

    return classifications
