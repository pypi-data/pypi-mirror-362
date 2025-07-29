# retrieved from picked-group-fdr  with some modifications
from __future__ import print_function, annotations
from pathlib import Path
import sys
import csv
import itertools
import collections
from typing import Dict, Iterator, List, Optional
from argparse import Namespace
from typing import List
import pandas as pd

import numpy as np


ENZYME_DEFAULT = "trypsin"
CLEAVAGES_DEFAULT = 2
MIN_PEPLEN_DEFAULT = 7
MAX_PEPLEN_DEFAULT = 60
SPECIAL_AAS_DEFAULT = "KR"
DIGESTION_DEFAULT = "full"


class DigestionParams:
    enzyme: str
    digestion: str
    min_length: int
    max_length: int
    cleavages: int
    special_aas: str
    methionine_cleavage: bool
    db: str
    use_hash_key: bool

    def __init__(
        self,
        enzyme = ENZYME_DEFAULT,
        digestion = DIGESTION_DEFAULT,
        min_length = MIN_PEPLEN_DEFAULT,
        max_length = MAX_PEPLEN_DEFAULT,
        cleavages = CLEAVAGES_DEFAULT,
        special_aas = SPECIAL_AAS_DEFAULT,
        fasta_contains_decoys = False,
    ):
        self.enzyme = enzyme

        self.digestion = digestion
        if self.enzyme == "no_enzyme":
            self.digestion = "none"

        self.min_length = min_length
        self.max_length = max_length
        self.cleavages = cleavages

        self.special_aas = list()
        if special_aas != "none":
            self.special_aas = list(special_aas)

        self.methionine_cleavage = True
        self.db = "target" if fasta_contains_decoys else "concat"

        self.use_hash_key = self.digestion == "none"


def digestion_params_list_to_arg_list(
    digestion_params_list: List[DigestionParams],
) -> List[str]:
    return (
        ["--min-length"]
        + [str(p.min_length) for p in digestion_params_list]
        + ["--max-length"]
        + [str(p.max_length) for p in digestion_params_list]
        + ["--cleavages"]
        + [str(p.cleavages) for p in digestion_params_list]
        + ["--enzyme"]
        + [p.enzyme for p in digestion_params_list]
        + ["--digestion"]
        + [p.digestion for p in digestion_params_list]
        + ["--special-aas"]
        + ["".join(p.special_aas) for p in digestion_params_list]
    )


def get_digestion_params_list(args: Namespace) -> List[DigestionParams]:
    """Takes the parsed arguments from argparse and returns a list of DigestionParams.

    Args:
        args (Namespace): arguments from argparse.ArgumentParser.

    Raises:
        ValueError: if digestion parameters of length > 1 are of unequal length.

    Returns:
        List[DigestionParams]: list of DigestionParams with length of longest digestion parameter argument.
    """
    params_list = [
        args.enzyme,
        args.digestion,
        args.min_length,
        args.max_length,
        args.cleavages,
        args.special_aas,
        [args.fasta_contains_decoys],
    ]
    param_lengths = [len(p) for p in params_list if len(p) != 1]
    if len(set(param_lengths)) > 1:
        raise ValueError("Received digestion parameters of unequal length.")

    max_params = max(param_lengths) if len(param_lengths) > 0 else 1
    params_list_updated = []
    for param in params_list:
        if len(param) == 1:
            param = param * max_params
        params_list_updated.append(param)

    return [DigestionParams(*p) for p in zip(*params_list_updated)]


def add_digestion_arguments(apars):
    apars.add_argument(
        "-e",
        "--enzyme",
        default=[ENZYME_DEFAULT],
        metavar="E",
        nargs="+",
        help="""Enzyme used for digestion. Available enzymes are
                "trypsin","trypsinp","no_enzyme","elastase","pepsin",
                "proteinasek","thermolysin","chymotrypsin","chymotrypsin+",
                "lys-n","lys-c","lys-cp","arg-c","asp-n","glu-c".""",
    )

    apars.add_argument(
        "-c",
        "--cleavages",
        default=[CLEAVAGES_DEFAULT],
        metavar="C",
        type=int,
        nargs="+",
        help="""Number of allowed miss cleavages used in the search engine.""",
    )

    apars.add_argument(
        "-l",
        "--min-length",
        default=[MIN_PEPLEN_DEFAULT],
        metavar="L",
        type=int,
        nargs="+",
        help="""Minimum peptide length allowed used in the search engine.""",
    )

    apars.add_argument(
        "-t",
        "--max-length",
        default=[MAX_PEPLEN_DEFAULT],
        metavar="L",
        type=int,
        nargs="+",
        help="""Maximum peptide length allowed used in the search engine.""",
    )

    apars.add_argument(
        "--special-aas",
        default=[SPECIAL_AAS_DEFAULT],
        metavar="S",
        nargs="+",
        help="""Special AAs that MaxQuant uses for decoy generation.
                Amino acids are written as a single string with all
                amino acids, e.g. "RK". To specify no amino acids,
                supply the string "none".""",
    )

    apars.add_argument(
        "--digestion",
        default=[DIGESTION_DEFAULT],
        metavar="D",
        nargs="+",
        help="""Digestion mode ('full', 'semi' or 'none').
                                                    """,
    )

    apars.add_argument(
        "--fasta_contains_decoys",
        help="Set this flag if your fasta file already contains decoy protein sequences.",
        action="store_true",
    )

ENZYME_CLEAVAGE_RULES = {
    "trypsin": {"pre": ["K", "R"], "not_post": ["P"], "post": []},
    "trypsinp": {"pre": ["K", "R"], "not_post": [], "post": []},
    "no_enzyme": {"pre": [], "not_post": [], "post": []},
    "chymotrypsin": {"pre": ["F", "W", "Y", "L"], "not_post": ["P"], "post": []},
    "chymotrypsin+": {"pre": ["F", "W", "Y", "L", "M"], "not_post": [], "post": []},
    "proteinasek": {
        "pre": ["A", "E", "F", "I", "L", "T", "V", "W", "Y"],
        "not_post": [],
        "post": [],
    },
    "elastase": {"pre": ["L", "V", "A", "G"], "not_post": ["P"], "post": []},
    "clostripain": {"pre": ["R"], "not_post": [], "post": []},
    "cyanogen-bromide": {"pre": ["M"], "not_post": [], "post": []},
    "iodosobenzoate": {"pre": ["W"], "not_post": [], "post": []},
    "proline-endopeptidase": {"pre": ["P"], "not_post": [], "post": []},
    "staph-protease": {"pre": ["E"], "not_post": [], "post": []},
    "asp-n": {"pre": [], "not_post": [], "post": ["D"]},
    "lys-c": {"pre": ["K"], "not_post": ["P"], "post": []},
    "lys-cp": {"pre": ["K"], "not_post": [], "post": []},
    "lys-n": {"pre": [], "not_post": [], "post": ["K"]},
    "arg-c": {"pre": ["R"], "not_post": ["P"], "post": []},
    "glu-c": {"pre": ["E"], "not_post": ["P"], "post": []},
    "pepsin-a": {"pre": ["F", "L"], "not_post": ["P"], "post": []},
    "elastase-trypsin-chymotrypsin": {
        "pre": ["A", "L", "I", "V", "F", "K", "R", "W", "F", "Y"],
        "not_post": ["P"],
        "post": [],
    },
    "lysarginase": {"pre": [], "not_post": [], "post": ["K", "R"]},
    "v8-de": {"pre": ["N", "D", "E", "Q"], "not_post": ["P"], "post": []},
}

PeptideToProteinMap = Dict[str, List[str]]


def make_iBaq_mapping_df(fasta_file:str) -> pd.DataFrame:
    """
    Generates a DataFrame mapping UniProt IDs to the number of peptides per protein 
    for intensity-based absolute quantification (iBAQ) analysis.

    This function digests the protein sequences from a given FASTA file, maps peptides 
    back to their corresponding proteins, and computes the number of peptides per protein. 
    It extracts the UniProt ID from the protein identifier and filters out reversed entries 
    (e.g., "REV__"). The output includes the maximum number of peptides per UniProt ID, 
    which is useful for downstream iBAQ calculations.

    Parameters:
    -----------
    fasta_file : str
        Path to the FASTA file containing protein sequences.

    Returns:
    --------
    pd.DataFrame
        A DataFrame with the following columns:
        - 'protein_identifier': Original protein identifier from the FASTA file.
        - 'num': Number of peptides mapped to the protein.
        - 'uniprot_id': Extracted UniProt identifier.
        - 'max_num_peptide': Maximum number of peptides observed for each UniProt ID.
    """
    digest_res = get_peptide_to_protein_map(
    fasta_file,
    min_len = 6,
    max_len = 32,
    miscleavages = 0,
    methionine_cleavage = False
    )
    mapping_dic = dict(get_num_peptides_per_protein(digest_res))
    protein2peptide_df = pd.DataFrame(list(mapping_dic.items()),columns=['protein_identifier','num'])
    try:
        protein2peptide_df['uniprot_id'] = protein2peptide_df['protein_identifier'].apply(lambda x:x.split('|')[1])
    except:
        protein2peptide_df['uniprot_id'] = protein2peptide_df['protein_identifier'].apply(lambda x:x.split('|')[0])
        
    protein2peptide_df = protein2peptide_df[~protein2peptide_df.protein_identifier.str.contains('REV__')]
    protein2peptide_df['max_num_peptide'] = protein2peptide_df.groupby('uniprot_id')['num'].transform('max')
    return protein2peptide_df




def main(argv):  # pragma: no cover
    args = parse_args()

    digestion_params_list = get_digestion_params_list(args)

    if args.prosit_input:
        writer = get_tsv_writer(args.prosit_input, delimiter=",")
        writer.writerow(
            "modified_sequence,collision_energy,precursor_charge".split(",")
        )

        prosit_input_file_with_proteins = args.prosit_input.replace(
            ".csv", "_with_proteins.csv"
        )
        writer_with_proteins = get_tsv_writer(
            prosit_input_file_with_proteins, delimiter=","
        )
        writer_with_proteins.writerow(
            "modified_sequence,collision_energy,precursor_charge,protein".split(",")
        )

        for peptide, proteins in get_peptide_to_protein_map_from_params(
            args.fasta, digestion_params_list
        ).items():
            if not is_valid_prosit_peptide(peptide):
                continue

            for charge in [2, 3, 4]:
                writer.writerow([peptide, 30, charge])
                writer_with_proteins.writerow([peptide, 30, charge, proteins[0]])

    if args.peptide_protein_map:
        with open(args.peptide_protein_map + ".params.txt", "w") as f:
            f.write(" ".join(sys.argv))

        writer = get_tsv_writer(args.peptide_protein_map, delimiter="\t")
        for peptide, proteins in get_peptide_to_protein_map_from_params(
            args.fasta, digestion_params_list
        ).items():
            writer.writerow([peptide, ";".join(proteins)])

    if args.ibaq_map:
        writer = get_tsv_writer(args.ibaq_map, delimiter="\t")

        num_peptides_per_protein = get_num_ibaq_peptides_per_protein(
            args.fasta, digestion_params_list
        )
        for protein, num_peptides in num_peptides_per_protein.items():
            writer.writerow([protein, num_peptides])


def parse_args():  # pragma: no cover
    import argparse

    apars = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    apars.add_argument(
        "--fasta",
        default=None,
        metavar="F",
        required=True,
        nargs="+",
        help="""Fasta file used as input.""",
    )

    apars.add_argument(
        "--prosit_input",
        default=None,
        metavar="M",
        required=False,
        help="""Path to file where to write the prosit input file.""",
    )

    apars.add_argument(
        "--peptide_protein_map",
        default=None,
        metavar="M",
        required=False,
        help="""Write mapping from peptides to all its proteins to
                the specified file.""",
    )

    apars.add_argument(
        "--ibaq_map",
        default=None,
        metavar="M",
        required=False,
        help="""Write number of peptides per protein to the specified file that meet
                the iBAQ criteria (6 <= pepLen <= 30, no miscleavages).""",
    )

    add_digestion_arguments(apars)

    # ------------------------------------------------
    args = apars.parse_args()

    return args


def is_valid_prosit_peptide(peptide):
    return len(peptide) <= 30 and "U" not in peptide and "X" not in peptide


def parse_until_first_space(fasta_id: str) -> str:
    return fasta_id.split(" ")[0]


def read_fasta_tide(
    file_path: str, db: str = "target", parse_id=parse_until_first_space
):
    read_fasta_maxquant(file_path, db, parse_id, special_aas=[], decoy_prefix="decoy_")


def read_fasta_maxquant(
    file_path: str,
    db: str = "target",
    parse_id=parse_until_first_space,
    special_aas: Optional[List[str]] = None,
    decoy_prefix: str = "REV__",
):
    if special_aas is None:
        special_aas = ["K", "R"]

    if db not in ["target", "decoy", "concat"]:
        raise ValueError("unknown db mode: %s" % db)

    has_special_aas = len(special_aas) > 0
    name, seq = None, []
    with open(file_path, "r") as fp:
        for line in itertools.chain(fp, [">"]):
            line = line.rstrip()
            if line.startswith(">"):
                if name:
                    seq = "".join(seq)
                    if db in ["target", "concat"]:
                        yield (name, seq)

                    if db in ["decoy", "concat"]:
                        rev_seq = seq[::-1]
                        if has_special_aas:
                            rev_seq = swap_special_aas(rev_seq, special_aas)
                        yield (decoy_prefix + name, rev_seq)

                if len(line) > 1:
                    name, seq = parse_id(line[1:]), []
            else:
                seq.append(line)


# from . import digestfast
# read_fasta = digestfast.readFastaMaxQuant
read_fasta = read_fasta_maxquant


def swap_special_aas(seq: str, special_aas: List[str]):
    """Swaps the special AAs with its preceding amino acid, as is done in MaxQuant.

    e.g. special_aas = ['R', 'K'] transforms ABCKDEFRK into ABKCDERKF
    """
    seq = list(seq)
    for i in range(1, len(seq)):
        if seq[i] in special_aas:
            swap_positions(seq, i, i - 1)
    seq = "".join(seq)
    return seq


def swap_positions(seq: str, pos1: int, pos2: int):
    seq[pos1], seq[pos2] = seq[pos2], seq[pos1]


def get_protein_sequences(file_paths: Optional[List[str]], **kwargs):
    if file_paths is None:
        return dict()

    protein_sequences = dict()
    for file_path in file_paths:
        for protein_id, protein_sequence in read_fasta(file_path, **kwargs):
            if (
                protein_id not in protein_sequences
            ):  # keep only first sequence per identifier
                protein_sequences[protein_id] = protein_sequence
    return protein_sequences


def filter_fasta_file(
    fasta_file: str, filtered_fasta_file: str, proteins: List[str], **kwargs
):
    with open(filtered_fasta_file, "w") as f:
        for prot, seq in read_fasta(fasta_file, **kwargs):
            if prot in proteins:
                f.write(">" + prot + "\n" + seq + "\n")
                # f.write('>decoy_' + prot + '\n' + seq[::-1] + '\n')


# @profile
def get_digested_peptides(
    seq: str,
    min_len: int = 6,
    max_len: int = 50,
    pre: List[str] = ["K", "R"],
    not_post: List[str] = ["P"],
    post: List[str] = [],
    digestion: str = "full",
    miscleavages: int = 0,
    methionine_cleavage: bool = True,
):
    """
    Yields digested peptide sequences from a protein sequence based on the specified digestion strategy.

    Supports full, semi-specific, and non-specific digestion modes, and includes options for 
    controlling cleavage rules, peptide length, missed cleavages, and initial methionine removal.

    Parameters:
    -----------
    seq : str
        Protein sequence to be digested.

    min_len : int, default=6
        Minimum peptide length to include.

    max_len : int, default=50
        Maximum peptide length to include.

    pre : List[str], default=["K", "R"]
        Amino acids before which cleavage is allowed (i.e., cleavage sites).

    not_post : List[str], default=["P"]
        Amino acids that prevent cleavage if they appear immediately after the cleavage site.

    post : List[str], default=[]
        Amino acids after which cleavage is allowed (used in more specialized rules).

    digestion : str, default="full"
        Type of digestion to perform:
        - "full": Enforces cleavage at both peptide ends.
        - "semi": Allows cleavage at only one end.
        - "none": Non-specific cleavage (random subsequences).

    miscleavages : int, default=0
        Number of allowed missed cleavage sites.

    methionine_cleavage : bool, default=True
        Whether to consider removal of the initial methionine residue (if present).

    Yields:
    -------
    str
        Digested peptide sequences that meet the specified criteria.
    """
    if digestion == "none":
        yield from non_specific_digest(seq, min_len, max_len)
    elif digestion == "semi":
        yield from semi_specific_digest(
            seq,
            min_len,
            max_len,
            pre,
            not_post,
            post,
            miscleavages,
            methionine_cleavage,
        )
    else:
        yield from full_digest(
            seq,
            min_len,
            max_len,
            pre,
            not_post,
            post,
            miscleavages,
            methionine_cleavage,
        )


def non_specific_digest(seq, min_len, max_len):
    seq_len = len(seq)
    for i in range(seq_len + 1):
        for j in range(i + min_len, min(seq_len + 1, i + max_len + 1)):
            if j <= seq_len:
                yield seq[i:j]


def semi_specific_digest(
    seq: str,
    min_len: int,
    max_len: int,
    pre: List[str],
    not_post: List[str],
    post: List[str],
    miscleavages: int,
    methionine_cleavage: bool,
):
    seq_len, starts = len(seq), [0]
    methionine_cleavage = methionine_cleavage and seq[0] == "M"
    length_accepted = lambda x: x >= min_len and x <= max_len

    for i in range(seq_len + 1):
        is_cleavage_site = is_enzymatic(
            seq[min([seq_len - 1, i])],
            seq[min([seq_len - 1, i + 1])],
            pre,
            not_post,
            post,
        )
        is_methionine_cleavage_site = i == 0 and methionine_cleavage
        if i == seq_len or is_cleavage_site or is_methionine_cleavage_site:
            # peptides with enzymatic C-terminal (both enzymatic and non-enzymatic N-terminal)
            start = starts[0]
            for j in range(start, min([i + 1, seq_len])):
                pep_len = min([i, seq_len - 1]) - j + 1
                if length_accepted(pep_len):
                    yield (seq[j : i + 1])
            starts.append(i + 1)
            methionine_cleaved = int(starts[0] == 0 and methionine_cleavage)
            if len(starts) > miscleavages + 1 + methionine_cleaved or i == seq_len:
                starts = starts[1 + methionine_cleaved :]
        else:  # peptides with non enzymatic C-terminal
            for start in starts:
                pep_len = i - start + 1
                if length_accepted(pep_len) and i + 1 not in starts:
                    yield (seq[start : i + 1])


def full_digest(
    seq: str,
    min_len: int,
    max_len: int,
    pre: List[str],
    not_post: List[str],
    post: List[str],
    miscleavages: int,
    methionine_cleavage: bool,
):
    seq_len, starts = len(seq), [0]
    methionine_cleavage = methionine_cleavage and seq[0] == "M"

    check_pre = len(pre) > 0
    check_post = len(post) > 0

    cleavage_sites = [0] if methionine_cleavage else []
    # HACK: inline if statement instead of using is_enzymatic because it is ~20% faster
    cleavage_sites.extend(
        [
            i
            for i in range(seq_len)
            if (
                check_pre
                and seq[i] in pre
                and not seq[min([seq_len - 1, i + 1])] in not_post
            )
            or (check_post and seq[min([seq_len - 1, i + 1])] in post)
        ]
    )
    cleavage_sites.append(seq_len)
    for i in cleavage_sites:
        for start in starts:
            pep_len = i - start + 1
            if min_len <= pep_len <= max_len:
                yield (seq[start : i + 1])
        starts.append(i + 1)
        methionine_cleaved = int(starts[0] == 0 and methionine_cleavage)
        if len(starts) > miscleavages + 1 + methionine_cleaved:
            starts = starts[1 + methionine_cleaved :]


def get_peptide_to_protein_map_from_params(
    fasta_files: List[str], digestion_params_list: List[DigestionParams], **kwargs
):
    """
    Generates a peptide-to-protein mapping from multiple FASTA files and digestion parameter sets.

    This function performs in silico digestion for each combination of FASTA file and digestion 
    parameters, and aggregates the resulting peptide-to-protein maps. If available, it also returns 
    a map of protein identifiers to sequences.

    Notes:
    - Each peptide may map to multiple proteins.
    - The function supports returning a tuple of (peptide_to_protein_map, protein_to_seq_map) 
      if the underlying call to `get_peptide_to_protein_map_from_params_single` provides both.


    Parameters:
    -----------
    fasta_files : List[str]
        List of file paths to FASTA files containing protein sequences.

    digestion_params_list : List[DigestionParams]
        List of digestion parameter sets (e.g., enzyme rules, miscleavages).

    **kwargs : dict
        Additional keyword arguments passed to the underlying single-file digestion function.

    Returns:
    --------
    Union[Dict[str, List[str]], Tuple[Dict[str, List[str]], Dict[str, str]]]
        - If only peptide-to-protein map is computed:
            A dictionary mapping peptides (str) to lists of protein identifiers (List[str]).
        - If protein sequences are also available:
            A tuple containing:
            - peptide_to_protein_map: Dict[str, List[str]]
            - protein_to_seq_map: Dict[str, str]
    """
    peptide_to_protein_map = collections.defaultdict(list)
    protein_to_seq_map = dict()
    for fasta_file in fasta_files:
        for params in digestion_params_list:
            # TODO: make sure we do not combine use_hash_key=True with use_hash_key=False
            peptide_to_protein_map_tmp = get_peptide_to_protein_map_from_params_single(
                fasta_file, params, **kwargs
            )

            # TODO: refactor peptide_to_protein_map as a class to get rid of this check
            if len(peptide_to_protein_map_tmp) == 2:
                (
                    peptide_to_protein_map_tmp,
                    protein_to_seq_map_tmp,
                ) = peptide_to_protein_map_tmp
                protein_to_seq_map |= protein_to_seq_map_tmp

            if len(peptide_to_protein_map) == 0:
                peptide_to_protein_map = peptide_to_protein_map_tmp
            else:
                for peptide, proteins in peptide_to_protein_map_tmp.items():
                    peptide_to_protein_map[peptide].extend(proteins)

    if len(protein_to_seq_map) > 0:
        return peptide_to_protein_map, protein_to_seq_map

    return peptide_to_protein_map


def get_peptide_to_protein_map_from_params_single(
    fasta_file: str, params: DigestionParams, **kwargs
):
    pre, not_post, post = get_cleavage_sites(params.enzyme)
    return get_peptide_to_protein_map(
        fasta_file,
        params.db,
        digestion=params.digestion,
        min_len=params.min_length,
        max_len=params.max_length,
        pre=pre,
        not_post=not_post,
        post=post,
        miscleavages=params.cleavages,
        methionine_cleavage=params.methionine_cleavage,
        use_hash_key=params.use_hash_key,
        special_aas=params.special_aas,
        **kwargs,
    )


def get_peptide_to_protein_map(
    fasta_file: str,
    db: str = "concat",
    min_len: int = 6,
    max_len: int = 52,
    pre: List[str] = ["K", "R"],
    not_post: List[str] = ["P"],
    post: List[str] = [],
    digestion: str = "full",
    miscleavages: int = 2,
    methionine_cleavage: bool = True,
    use_hash_key: bool = False,
    special_aas: List[str] = ["K", "R"],
    parse_id=parse_until_first_space,
):
    peptide_to_protein_map = collections.defaultdict(list)
    protein_to_seq_map = dict()

    print(f"Parsing fasta file: {Path(fasta_file).name}")
    for protein_idx, (protein, seq) in enumerate(
        read_fasta(fasta_file, db, parse_id, special_aas=special_aas)
    ):
        if protein_idx % 10000 == 0:
            print(f"Digesting protein {protein_idx}")
        seen_peptides = set()
        protein_to_seq_map[protein] = seq
        for peptide in get_digested_peptides(
            seq,
            min_len,
            max_len,
            pre,
            not_post,
            post,
            digestion,
            miscleavages,
            methionine_cleavage,
        ):
            peptide = peptide
            if use_hash_key:
                hash_key = peptide[:6]
            else:
                hash_key = peptide
            if hash_key not in seen_peptides:
                seen_peptides.add(hash_key)
                peptide_to_protein_map[hash_key].append(protein)

    if use_hash_key:
        return (peptide_to_protein_map, protein_to_seq_map)
    else:
        return peptide_to_protein_map


def merge_peptide_to_protein_maps(peptide_protein_maps: Iterator[PeptideToProteinMap]):
    peptide_to_protein_map = collections.defaultdict(list)
    for peptide_protein_map in peptide_protein_maps:
        for peptide, proteins in peptide_protein_map.items():
            peptide_to_protein_map[peptide].extend(proteins)
    return peptide_to_protein_map


def get_peptide_to_protein_map_from_file(
    peptide_to_protein_map_file, use_hash_key=False
):
    if use_hash_key:
        print("Hash key not supported yet, continuing without hash key...")
        use_hash_key = False
    peptide_to_protein_map = collections.defaultdict(list)
    reader = get_tsv_reader(peptide_to_protein_map_file)
    for i, row in enumerate(reader):
        if (i + 1) % 1000000 == 0:
            print(f"Processing peptide {i+1}")

        peptide, proteins = row[0], row[1].split(";")
        if use_hash_key:
            raise NotImplementedError("Hash key not supported yet...")
            hash_key = peptide[:6]
        else:
            hash_key = peptide
        for protein in proteins:
            peptide_to_protein_map[hash_key].append(protein)
    return peptide_to_protein_map


def get_proteins(peptide_to_protein_map, peptide: str):
    if len(peptide_to_protein_map) == 2:
        hash_key = peptide[:6]
        proteins = list()
        if hash_key in peptide_to_protein_map[0]:
            for protein in peptide_to_protein_map[0][hash_key]:
                # TODO: This does not work correctly for full or partial digestion,
                # since we might find the peptide with the wrong number of enzymatic terminals
                if peptide in peptide_to_protein_map[1][protein]:
                    proteins.append(protein)
            proteins = sorted(proteins)
        # else:
        #    print("Could not find peptide " + peptide + " in fasta database")
        return proteins
    else:
        return peptide_to_protein_map.get(peptide, [])


def get_all_proteins(peptide_to_protein_map):
    seen_proteins = set()
    if len(peptide_to_protein_map) == 2:
        peptide_to_protein_map = peptide_to_protein_map[0]
    for _, proteins in peptide_to_protein_map.items():
        for protein in proteins:
            if protein not in seen_proteins:
                seen_proteins.append(protein)
    return list(seen_proteins)


def get_ibaq_peptide_to_protein_map(
    fasta_files: List[str], digestion_params_list: List[DigestionParams], **kwargs
):
    """
    Generates a peptide-to-protein mapping specifically configured for iBAQ quantification.

    This function modifies the provided digestion parameters to conform to iBAQ standards:
    - Peptide lengths are constrained to a minimum of 6 and a maximum of 30 amino acids.
    - Missed cleavages are disabled (`cleavages = 0`).
    - Initial methionine cleavage is disabled.

    The adjusted digestion parameters are then used to perform in silico digestion and build
    a peptide-to-protein map using the underlying `get_peptide_to_protein_map_from_params` function.

    Parameters:
    -----------
    fasta_files : List[str]
        List of paths to FASTA files containing protein sequences.

    digestion_params_list : List[DigestionParams]
        List of digestion parameter objects, which will be adjusted for iBAQ use.

    **kwargs : dict
        Additional keyword arguments passed to `get_peptide_to_protein_map_from_params`.

    Returns:
    --------
    Union[Dict[str, List[str]], Tuple[Dict[str, List[str]], Dict[str, str]]]
        - A dictionary mapping peptides to lists of protein identifiers.
        - If available, also returns a dictionary mapping protein IDs to sequences.
    """
    digestion_params_list_ibaq = []
    for digestion_params in digestion_params_list:
        digestion_params.min_length = max([6, digestion_params.min_length])
        digestion_params.max_length = min([30, digestion_params.max_length])
        digestion_params.cleavages = 0
        digestion_params.methionine_cleavage = False
        digestion_params_list_ibaq.append(digestion_params)
    return get_peptide_to_protein_map_from_params(
        fasta_files, digestion_params_list_ibaq, **kwargs
    )


def get_num_ibaq_peptides_per_protein_from_args(args, peptide_to_protein_maps, **kwargs):
    """
    Determines the number of iBAQ peptides per protein based on input arguments.

    This function computes the number of peptides per protein required for iBAQ 
    quantification, using either a FASTA file (in silico digestion) or a provided 
    peptide-to-protein mapping.

    - If a FASTA file is provided via `args.fasta`, proteins are digested in silico 
      using digestion parameters, and peptide counts are calculated accordingly.
    - If a peptide-to-protein map is provided via `args.peptide_protein_map`, 
      peptide counts are derived directly from the mapping (no sequence-based digestion).
    - Raises an error if neither input is available.

    Parameters:
    -----------
    args : argparse.Namespace
        Command-line arguments containing either `fasta` or `peptide_protein_map`.
    
    peptide_to_protein_maps : List[Dict[str, List[str]]]
        List of peptide-to-protein mappings, used if no FASTA file is provided.
    
    **kwargs : dict
        Additional keyword arguments passed to the digestion function.

    Returns:
    --------
    dict
        A dictionary mapping protein identifiers to the number of associated peptides.

    Raises:
    -------
    ValueError
        If neither a FASTA file nor a peptide-to-protein map is provided.
    """

    digestion_params_list = get_digestion_params_list(args)
    if args.fasta:
        print("In silico protein digest for iBAQ")
        num_ibaq_peptides_per_protein = get_num_ibaq_peptides_per_protein(
            args.fasta, digestion_params_list, **kwargs
        )
    elif args.peptide_protein_map:
        print("Found peptide_protein_map (instead of fasta input): ")
        print(
            "- calculating iBAQ values using all peptides in peptide_protein_map."
        )
        print("- cannot compute sequence coverage.")
        num_ibaq_peptides_per_protein = get_num_peptides_per_protein(
            merge_peptide_to_protein_maps(peptide_to_protein_maps)
        )
    else:
        raise ValueError(
            "No fasta or peptide to protein mapping file detected, please specify either the --fasta or --peptide_protein_map flags"
        )
    return num_ibaq_peptides_per_protein



def get_num_ibaq_peptides_per_protein(
    fasta_files: List[str], digestion_params_list: List[DigestionParams], **kwargs
) -> Dict[str, int]:
    """
    Computes the number of iBAQ-eligible peptides per protein from given FASTA files.

    This function performs an in silico digestion of protein sequences using the provided 
    digestion parameters. It then maps the resulting peptides to their corresponding proteins 
    and counts the number of peptides per protein, which is essential for iBAQ quantification.

    Parameters:
    -----------
    fasta_files : List[str]
        A list of paths to FASTA files containing protein sequences.
    
    digestion_params_list : List[DigestionParams]
        A list of digestion parameter objects specifying enzyme rules, missed cleavages, 
        and other digestion settings.

    **kwargs : dict
        Additional arguments forwarded to the underlying peptide-to-protein mapping function.

    Returns:
    --------
    Dict[str, int]
        A dictionary mapping protein identifiers to the number of iBAQ peptides.
    """

    peptide_to_protein_map_ibaq = get_ibaq_peptide_to_protein_map(
        fasta_files, digestion_params_list, **kwargs
    )
    return get_num_peptides_per_protein(peptide_to_protein_map_ibaq)


def get_num_peptides_per_protein(peptide_to_protein_map) -> Dict[str, int]:
    num_peptides_per_protein = collections.defaultdict(int)
    for _, proteins in peptide_to_protein_map.items():
        for protein in proteins:
            num_peptides_per_protein[protein] += 1

    return num_peptides_per_protein


def get_cleavage_sites(enzyme):
    if enzyme not in ENZYME_CLEAVAGE_RULES:
        print.error("Enzyme", enzyme, "not implemented yet")

    pre = ENZYME_CLEAVAGE_RULES[enzyme]["pre"]
    not_post = ENZYME_CLEAVAGE_RULES[enzyme]["not_post"]
    post = ENZYME_CLEAVAGE_RULES[enzyme]["post"]
    return pre, not_post, post


def is_enzymatic_advanced(
    aa1: str,
    aa2: str,
    pre: List[str] = ["K", "R"],
    not_post: List[str] = ["P"],
    post: List[str] = [],
    methionine_cleavage: bool = True,
):
    return (
        aa1 == "-"
        or aa2 == "-"
        or is_enzymatic(aa1, aa2, pre, not_post, post)
        or (methionine_cleavage and aa1 == "M")
    )


def is_enzymatic(aa1, aa2, pre, not_post, post):
    return (aa1 in pre and aa2 not in not_post) or (aa2 in post)


def has_miscleavage(seq, pre=["K", "R"], not_post=["P"], post=[]):
    for i in range(len(seq) - 1):
        if is_enzymatic_advanced(seq[i], seq[i + 1], pre, not_post, post):
            return True
    return False


def get_tsv_reader(filename, delimiter="\t"):
    # Python 3
    if sys.version_info[0] >= 3:
        return csv.reader(open(filename, "r", newline=""), delimiter=delimiter)
    # Python 2
    else:
        return csv.reader(open(filename, "rb"), delimiter=delimiter)


def get_tsv_writer(filename, delimiter="\t"):
    # Python 3
    if sys.version_info[0] >= 3:
        return csv.writer(open(filename, "w", newline=""), delimiter=delimiter)
    # Python 2
    else:
        return csv.writer(open(filename, "wb"), delimiter=delimiter)



def _get_the_number_peptides_from_protein_group(x,mapping_df):
    try:
        if len(mapping_df[mapping_df.proteins.isin(x.split(';'))]):
            return(mapping_df[mapping_df.proteins.isin(x.split(';'))]['num'].max())
        else:
            return 0
    except:
        return 0


def unnest_proteingroups(df:pd.DataFrame) -> pd.DataFrame:
    """
    Unnest the protein_groups A;B as two separate rows with the same values
    the protein groups are the index of the the pandas dataframe df
    """
    temp_df = df
    temp_df['index'] = temp_df.index.str.split(';')
    temp_df = temp_df.explode('index')
    temp_df = temp_df.set_index('index')
    return temp_df



