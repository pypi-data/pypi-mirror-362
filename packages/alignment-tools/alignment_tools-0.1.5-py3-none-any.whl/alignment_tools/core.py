import warnings
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy
import os

from Bio import AlignIO,SeqIO,Phylo
from Bio.Align import AlignInfo
from Bio.PDB import PDBParser

import freesasa
# this is the path to interproscan binaries at BayBioMS
dir_interpro = ""


def batch_find_sequence_start_end(fullsequence:str ,subsequence_grouped:str) -> str:
    """
    Find the start and end positions of multiple peptide subsequences within a full sequence.

    Splits the `subsequence_grouped` string (which contains semicolon-separated peptide subsequences),
    then uses `find_peptide_positions_within_full_sequence` to compute the start and end position
    of each peptide in the `fullsequence`.

    Parameters
    ----------
    fullsequence : str
        The full protein or nucleotide sequence in which to search for subsequences.
    subsequence_grouped : str
        A semicolon-separated string of peptide subsequences (e.g., "ABC;DEF;GHI").

    Returns
    -------
    str
        A semicolon-separated string of start and end positions for each peptide, in the format
        'start_end;start_end;...'.

    Notes
    -----
    The function assumes each peptide appears exactly once in the full sequence.
    If a peptide is not found, `find_peptide_positions_within_full_sequence` may raise an error
    or return an invalid result depending on its internal logic.
    """
    return (';').join([find_peptide_positions_within_full_sequence(fullsequence,x) for x in subsequence_grouped.split(';') ])



def find_peptide_positions_within_full_sequence(fullsequence:str,peptide:str) -> str:
    """
    Find the start and end positions of a peptide within a full sequence.

    Uses `alignment_functions.find_motif_positions` to locate the starting index
    of the peptide motif in the full sequence, then calculates the end position
    based on the peptide length.

    Parameters
    ----------
    fullsequence : str
        The full protein or nucleotide sequence in which to search.
    peptide : str
        The peptide sequence (motif) to find within the full sequence.

    Returns
    -------
    str
        A string formatted as 'start_end' representing the 1-based inclusive
        positions of the peptide within the full sequence.

    Notes
    -----
    The function assumes that `alignment_functions.find_motif_positions` returns
    the starting index (0-based) of the peptide in the full sequence.
    """
    startpoint = find_motif_positions(fullsequence,peptide)
    return f'{startpoint}_{startpoint+len(peptide)-1 }'



def get_min_max_residueIDs_from_reference_residue(uniprot_id, ref_residue_id:int,neighbor_distance:int= 6, atom_name="CA"):
    """
    Identifies the minimum and maximum residue IDs within a specified distance 
    from a reference residue in a protein structure.

    Parameters
    ----------
    uniprot_id : str
        The UniProt ID of the protein. Used to construct the PDB file name (expected format: 'AF-{uniprot_id}-F1.pdb').
    
    ref_residue_id : int
        The residue ID to use as the reference point.
    
    neighbor_distance : int, optional
        The distance threshold (in Ångströms) to define neighboring residues (default is 6 Å).
    
    atom_name : str, optional
        The atom name in the reference residue to calculate distance from (default is 'CA' for alpha carbon).

    Returns
    -------
    tuple
        A tuple containing:
        - minimum residue ID within the distance threshold
        - maximum residue ID within the distance threshold

    Notes
    -----
    - Requires the corresponding PDB file to be named 'AF-{uniprot_id}-F1.pdb' and located in the working directory.
    - Uses Euclidean distance from the specified atom in the reference residue.
    - Assumes the structure only contains one model.
    
    Raises
    ------
    ValueError
        If the reference atom is not found in the structure.
    """
 
    try:
        df = PDB2dataFrame(uniprot_id,f'AF-{uniprot_id}-F1.pdb')
        df = calculate_distance_from_ref_point(df, ref_residue_id,atom_name=atom_name)
        return df['residue_id'][df.distance <= neighbor_distance].min(), df['residue_id'][df.distance <= neighbor_distance].max()
    except:
        return None,None



def PDB2dataFrame(id:str,pdb_file:str) -> pd.DataFrame:
    """
    Parses a PDB file and extracts atomic-level information into a pandas DataFrame.

    Parameters
    ----------
    id : str
        An identifier for the structure (e.g., PDB ID or custom name).
    
    pdb_file : str
        Path to the PDB file to be parsed.

    Returns
    -------
    pd.DataFrame
        A DataFrame where each row corresponds to an atom in the structure.
        Columns include:
            - 'atom_name': Name of the atom (e.g., 'CA', 'N').
            - 'residue_name': 3-letter residue name (e.g., 'ALA').
            - 'chain_id': Chain identifier (e.g., 'A').
            - 'residue_id': Residue number.
            - 'x', 'y', 'z': Cartesian coordinates of the atom.
            - 'bfactor': B-factor (temperature factor).
            - 'occupancy': Occupancy value of the atom.
            - 'element': Chemical element symbol.
            - 'id': The structure ID passed to the function.

    Notes
    -----
    - Uses Biopython's PDBParser to extract atomic data.
    - Only includes atoms from the first model (if multiple models exist).
    - Skips hydrogen atoms only if they are not present in the file (no filtering is done).
    """
    parser = PDBParser()
    structure = parser.get_structure(id, pdb_file)

    atom_data = []

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    atom_info = {
                        "atom_name": atom.get_name(),
                        "residue_name": residue.get_resname(),
                        "chain_id": chain.id,
                        "residue_id": residue.get_id()[1],
                        "x": atom.coord[0],
                        "y": atom.coord[1],
                        "z": atom.coord[2],
                        "bfactor": atom.get_bfactor(),
                        "occupancy": atom.get_occupancy(),
                        "element": atom.element
                    }
                    atom_data.append(atom_info)
    final_df = pd.DataFrame(atom_data)
    final_df['id'] = id
    # Convert to DataFrame
    return final_df


def _get_reference_point(df:pd.DataFrame,resid:int,atom_name:str='CA'):
    """
    Extracts the 3D coordinates (x, y, z) of a specific atom from a given residue in a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing atomic coordinates and residue information.
        Expected columns: ['residue_id', 'atom_name', 'x', 'y', 'z'].
    
    resid : int
        The residue ID from which to extract the reference atom.
    
    atom_name : str, optional
        The name of the atom to extract (default is 'CA' for alpha carbon).
    
    Returns
    -------
    np.ndarray
        A NumPy array of shape (1, 3) representing the (x, y, z) coordinates of the specified atom.

    Raises
    ------
    ValueError
        If the specified atom is not found in the DataFrame.
    """
    return np.array(df[(df.residue_id == resid) & (df.atom_name == atom_name) ][['x','y','z']])




def calculate_distance_from_ref_point(df:pd.DataFrame,resid:int,atom_name:str='CA'):
    """
    Calculates the Euclidean distance from a reference atom in a specified residue
    to all other atoms in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame containing atomic coordinates and residue information.
        Expected columns: ['residue_id', 'atom_name', 'x', 'y', 'z'].
    
    resid : int
        The residue ID containing the reference atom.
    
    atom_name : str, optional
        The name of the reference atom within the residue (default is 'CA').

    Returns
    -------
    pd.DataFrame
        The input DataFrame with an additional column `'distance'` representing
        the Euclidean distance of each atom to the reference point.

    Raises
    ------
    ValueError
        If the specified reference atom is not found in the DataFrame.
    """
    ref_point = _get_reference_point(df,resid,atom_name)
    df['distance'] = np.sqrt(
    (df['x'] - ref_point[0,0])**2 +
    (df['y'] - ref_point[0,1])**2 +
    (df['z'] - ref_point[0,2])**2 )
    return df




def find_min_tuple(tuples):
    """
    Returns the minimum tuple from a list of tuples, ignoring any tuples containing None.

    Parameters
    ----------
    tuples : list of tuple
        A list of tuples to evaluate.

    Returns
    -------
    tuple or None
        The tuple with the smallest value, or None if no valid tuples exist.
    """
    clean_tuples = [t for t in tuples if None not in t]
    
    if not clean_tuples:
        return None
    try:
        return min(min(clean_tuples))
    except:
        return None
    


def find_max_tuple(tuples):
    """
    Returns the maximum tuple from a list of tuples, ignoring any tuples containing None.

    Parameters
    ----------
    tuples : list of tuple
        A list of tuples to evaluate.

    Returns
    -------
    tuple or None
        The tuple with the largest value, or None if no valid tuples exist.
    """
    clean_tuples = [t for t in tuples if None not in t]
    
    if not clean_tuples:
        return None
    try:
        return max(max(clean_tuples))
    except:
        return None



def download_alphafold_pdb_from_uniprot_id(uniprot_id: str, database_version: str = 'v4') -> None:
    """
    Downloads the AlphaFold PDB structure file for a given UniProt ID.

    Parameters
    ----------
    uniprot_id : str
        The UniProt identifier of the protein to download (e.g., 'P12345').

    database_version : str, optional
        The AlphaFold database version to use (default is 'v4').

    Returns
    -------
    None
        The function saves the downloaded PDB file in the current working directory
        with the filename format: 'AF-{uniprot_id}-F1.pdb'.

    Notes
    -----
    - The function uses `curl` via `os.system()`, so it requires `curl` to be installed and available in the system's PATH.
    - The file is fetched from: https://alphafold.ebi.ac.uk/files/
    - The downloaded file corresponds to: 'AF-{uniprot_id}-F1-model_{database_version}.pdb'
      but it is saved locally as: 'AF-{uniprot_id}-F1.pdb'
    """
    alphafold_ID = f'AF-{uniprot_id}-F1'
    print(alphafold_ID)
    model_url = f'https://alphafold.ebi.ac.uk/files/{alphafold_ID}-model_{database_version}.pdb'
    os.system(f'curl {model_url} -o {alphafold_ID}.pdb')




def find_motif_positions(sequence:str, motif:str) -> int :
    """
    Finds the 1-based index of the first occurrence of a motif in a given sequence.

    This function searches for the first exact occurrence of the specified motif (substring)
    within a larger sequence (e.g., a protein or nucleotide sequence). It returns the index
    of the first character of that match using 1-based indexing, which is standard in
    bioinformatics.

    Parameters
    ----------
    sequence : str
        The full sequence in which to search for the motif.
    motif : str
        The motif (substring) to locate within the sequence.

    Returns
    -------
    int
        The 1-based position of the first occurrence of the motif in the sequence.
        Returns None if the motif is not found or an error occurs.

    Examples
    --------
    find_motif_positions("ACDEFGHIK", "EFG")
    4

    find_motif_positions("ACDEFGHIK", "XYZ")
    None
    """
    try:
        positions = []
        for i in range(len(sequence) - len(motif) + 1):
            if sequence[i:i+len(motif)] == motif:
                positions.append(i + 1)  # +1 for 1-based indexing (common in bioinformatics)
        return int(positions[0])
    except:
        return None



def find_residue_position(sequence:str,start_pos:int= 1, residue:str = 'C') -> str:
    """
    Finds all positions of a specific residue in a given sequence and returns them as a semicolon-separated string.

    This function scans the input sequence for occurrences of a specified residue (e.g., 'C' for cysteine)
    and returns their positions, adjusted by the given start position (useful when the sequence is a subregion
    of a longer protein).

    Parameters
    ----------
    sequence : str
        The amino acid sequence in which to search.
    start_pos : int, optional
        The starting position of the sequence relative to a global context (default is 1).
        This is added to the zero-based index to get the correct biological position.
    residue : str, optional
        The single-letter code of the amino acid to search for (default is 'C').

    Returns
    -------
    str
        A semicolon-separated string of 1-based positions where the residue is found.
        Returns an empty string if the residue is not found.

    Examples
    --------
    find_residue_position("ACKCDEFGC", start_pos=1, residue='C')
    '2;4;9'

    find_residue_position("MQDRVKRPMNAFIVWSRDQRRKMALEN", start_pos=10, residue='R')
    '17;20;21;23'
    """
    return (';').join(list(map(str,[i+ start_pos for i, c in enumerate(sequence) if c ==residue])))



def _tokenize(x, residue='C'):
    """
    Converts a sequence string into a binary list indicating presence of a specified residue.

    For each character in the input sequence, returns 1 if it matches the residue, otherwise 0.
    Example: For residue 'C', input 'CCRTG_JHLKSDG' returns [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0].

    Parameters
    ----------
    x : str
        Input sequence string.
    residue : str, optional
        Single character representing the residue of interest (default is 'C').

    Returns
    -------
    list of int
        List of 1s and 0s indicating presence of the residue at each position.

    Examples
    --------
    _tokenize('CCRTG_JHLKSDG', residue='C')
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    """
    return [int(char) for char in''.join(list(map(str,[1 if x==residue else 0 for x in x])))]



def calculte_conservation_scores_per_residue(fasta_df:pd.DataFrame,residue= 'C'):
    """
    Calculates conservation scores per residue type across aligned sequences.

    This function computes a conservation score for a specified residue type (e.g., 'C') 
    based on the average frequency of that residue appearing in each position across 
    a multiple sequence alignment. The input DataFrame is expected to have aligned sequences.

    Parameters
    ----------
    fasta_df : pandas.DataFrame
        DataFrame containing aligned sequences with columns:
        - 'Proteins': identifiers of sequences
        - 'sequence': aligned sequences (strings) containing gaps if any
    residue : str, optional
        The amino acid residue to calculate conservation for (default is 'C').

    Returns
    -------
    fasta_df : pandas.DataFrame
        The original DataFrame augmented with a new column 
        `conserved_<residue>` containing conservation scores per sequence position as
        semicolon-separated strings.
    conserved_df : pandas.DataFrame
        A numeric matrix (DataFrame) of the conservation scores per residue per position,
        indexed by 'Proteins'.

    Notes
    -----
    - The function filters out sequences with the exact value '..:.' in the 'sequence' column.
    - Uses a helper function `_tokenize` (not provided here) to transform sequences into numeric vectors 
      indicating the presence of the specified residue.
    - Conservation score per position is computed as the product of the residue presence matrix 
      and the mean frequency across sequences.
    - The returned `conserved_df` can be used for further analysis or visualization.

    Examples
    --------
    fasta_df, conserved_df = calculate_conservation_scores_per_residue(fasta_df, residue='C')
    fasta_df.columns
    Index(['Proteins', 'sequence', 'tokens', 'conserved_C'], dtype='object')
    """
    fasta_df = fasta_df[fasta_df['sequence'] !='..:.']
    fasta_df['tokens'] = fasta_df['sequence'].apply(lambda x:_tokenize(x,residue=residue))
    matrix = np.array(fasta_df.tokens.tolist())
    conserved_mat =  matrix * matrix.mean(axis=0) # this calculates the average count of that residue after alignment
    nonzero_per_row = [row[row != 0] for row in conserved_mat]
    list_scores = []
    for row in nonzero_per_row:
        sting_row = list(map(str,row))
        list_scores.append(';'.join(sting_row))
    fasta_df[f'conserved_{residue}'] = list_scores
    conserved_df = pd.DataFrame(conserved_mat)
    conserved_df.index = fasta_df.Proteins
    #conserved_df[conserved_df==0] = None
    return fasta_df, conserved_df





def run_interproscan(input_file:str,interpro_command = "/media/LIMS/Src/fasta_annotation/interproscan-5.73-104.0/interproscan.sh" ) -> None:
    """
    Runs InterProScan to annotate protein sequences with domain and family information.

    This function executes the InterProScan command-line tool on a given FASTA file
    to generate protein domain annotations (e.g., Pfam, TIGRFAM, etc.) in TSV format.

    Parameters
    ----------
    input_file : str
        Path to the input FASTA file containing protein sequences to annotate.
    interpro_command : str, optional
        Full path to the InterProScan executable script (default is a specific local path).

    Returns
    -------
    None
        The function does not return a value but generates an output TSV file in the
        same directory as the input file, with annotations from InterProScan.

    Raises
    ------
    subprocess.CalledProcessError
        If the InterProScan command fails.

    Notes
    -----
    - Ensure InterProScan is installed and the path provided in `interpro_command` is correct.
    - The output TSV file will have the same base name as the input but with an `.tsv` extension.
    - Additional command-line options (e.g., output directory, formats) can be added by modifying the `command` list.

    Examples
    --------
    run_interproscan("proteins.fasta")
    """

    command = [
        interpro_command,
        "-i " + input_file,
        "-f tsv " 
    ]
    subprocess.run(
        command, check=True, text=True, capture_output=True
    )
    return None



def run_clustal(input_file:str,draw_tree=False ):
    """
    Runs ClustalW on a FASTA file to generate a multiple sequence alignment (MSA) and optionally draws a dendrogram.

    This function runs the external ClustalW program on the given FASTA file,
    producing an alignment file (.aln) and a dendrogram file (.dnd).
    It reads the alignment and computes a consensus sequence.
    Optionally, it draws and displays the phylogenetic tree.

    Parameters
    ----------
    input_file : str
        Path to the input FASTA file containing sequences to be aligned.
    draw_tree : bool, optional
        If True, displays a dendrogram of the phylogenetic tree (default is False).

    Returns
    -------
    alignment : Bio.Align.MultipleSeqAlignment
        The multiple sequence alignment object read from the ClustalW output.
    aln_output_file : str
        Path to the generated alignment file (.aln).

    Raises
    ------
    subprocess.CalledProcessError
        If the ClustalW command fails.

    Notes
    -----
    - Requires ClustalW installed and available in the system PATH.
    - Uses Biopython modules: AlignIO, AlignInfo, Phylo.
    - Uses matplotlib.pyplot for drawing the tree.

    Examples
    --------
    alignment, aln_file = run_clustal("sequences.fasta", draw_tree=True)
    print(alignment)
    """
    aln_output_file = input_file.split(".")[0] + ".aln"
    dnd_file = input_file.split(".")[0] + ".dnd"
    clustalw_command = [
        "clustalw",
        "-INFILE=" + input_file,
        "-OUTFILE=" + aln_output_file,
    ]
    subprocess.run(
        clustalw_command, check=True, text=True, capture_output=True
    )
    alignment = AlignIO.read(aln_output_file, "clustal")
    summary_align = AlignInfo.SummaryInfo(alignment)
    consensus = summary_align.dumb_consensus()
    print(consensus)
    tree = Phylo.read(dnd_file, "newick")
    if draw_tree:
        Phylo.draw(tree)
        plt.show()
    return alignment, aln_output_file



def parse_fasta_sequences(input_file, from_site=0, to_site=None):
    """
    Parses a FASTA file and returns a dictionary of sequence IDs and their (optionally sliced) sequences.

    This function reads a FASTA file and returns a dictionary where each key is a sequence ID
    (from the FASTA header) and the value is the corresponding nucleotide or amino acid sequence.
    Optionally, you can extract a slice of the sequence using `from_site` and `to_site`.

    Parameters
    ----------
    input_file : str
        Path to the FASTA file to be parsed.
    from_site : int, optional
        Start index for slicing the sequence (default is 0, inclusive).
    to_site : int or None, optional
        End index for slicing the sequence (default is None, meaning slice until the end).

    Returns
    -------
    dict
        A dictionary where keys are sequence IDs and values are sequences (or sliced subsequences).

    Notes
    -----
    - Slicing follows Python's 0-based indexing and is inclusive of `from_site`, exclusive of `to_site`.
    - Sequences are returned as plain strings.

    Examples
    --------
    parse_fasta_sequences("example.fasta")
    {'seq1': 'MKTLLILTCLVAVALARPKH', 'seq2': 'GAVRQKLIED'}

    parse_fasta_sequences("example.fasta", from_site=5, to_site=10)
    {'seq1': 'LILTC', 'seq2': 'QKLIE'}
    """
    fasta_ids_dic = {}
    for record in SeqIO.parse(input_file, "fasta"):
        seq = str(record.seq)
        if to_site is not None:
            seq = seq[from_site:to_site]
        fasta_ids_dic[str(record.id)] = seq

    return fasta_ids_dic






def convert_aln2fasta(input_file, output_file):
    """
    Converts a CLUSTAL .aln alignment file to FASTA format.

    This function reads a CLUSTAL-formatted alignment file (commonly with `.aln` extension),
    parses the sequence blocks, reconstructs full sequences per identifier, and writes
    them in standard FASTA format to the output file.

    Parameters
    ----------
    input_file : str
        Path to the input `.aln` file in CLUSTAL format.
    output_file : str
        Path to the output `.fasta` file to be created.

    Returns
    -------
    None
        Writes output to the specified FASTA file.

    Notes
    -----
    - Skips CLUSTAL headers, empty lines, and consensus lines (lines containing '*').
    - Handles multiple alignment blocks and concatenates sequences by ID.
    - Assumes alignment lines are whitespace-separated: `<ID> <SEQ>`.

    Examples
    --------
    convert_aln2fasta("alignment.aln", "alignment.fasta")
    Converted alignment.aln to alignment.fasta
    """
    def _parse_aln(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

        sequences = {}
        for line in lines:
            if not line.strip() or line.startswith("CLUSTAL") or line.__contains__("*"):
                continue

            parts = line.strip().split()
            if len(parts) < 2:
                continue

            name, seq = parts[0], parts[1]
            if name in sequences:
                sequences[name] += seq
            else:
                sequences[name] = seq

        return sequences

    def _write_fasta(sequences, output_path):
        with open(output_path, "w") as file:
            for name, seq in sequences.items():
                file.write(f">{name}\n")
                file.write(f"{seq}\n")

    sequences = _parse_aln(input_file)
    _write_fasta(sequences, output_file)
    print(f"Converted {input_file} to {output_file}")



def make_fasta_file(sub_df, file_name="final.fasta"):
    """
    Writes protein sequences from a DataFrame to a FASTA-format file.

    Each row in the DataFrame should contain a protein sequence and a corresponding protein name.
    The function creates a FASTA file where each sequence is preceded by a header line with the protein name.

    Parameters
    ----------
    sub_df : pandas.DataFrame
        A DataFrame containing at least two columns:
        - 'sequence': the protein sequence as a string
        - 'Proteins': the identifier or name of the protein
    file_name : str, optional
        The name of the output FASTA file (default is "final.fasta").

    Returns
    -------
    None
        The function writes to a file and returns nothing.

    Raises
    ------
    KeyError
        If the 'sequence' or 'Proteins' column is not present in `sub_df`.
    """

    with open(file_name, "w") as f:
        for i in range(len(sub_df)):
            sequence = sub_df.sequence.tolist()[i]
            protein_name = sub_df.Proteins.tolist()[i]
            f.write(f">{protein_name}\n")
            f.write(sequence + "\n")



def make_dictionary_seqs(fasta: str,splitter = '|') -> dict:
    """
    Parses a FASTA file and returns a dictionary and DataFrame of sequences.

    This function reads a FASTA file and constructs:
    1. A dictionary where keys are parsed from the FASTA header using a delimiter
       and values are the corresponding sequences.
    2. A pandas DataFrame containing the same data with columns: 'Proteins' and 'sequence'.

    Parameters
    ----------
    fasta : str
        Path to the input FASTA file.
    splitter : str, optional
        A character used to split the FASTA header (default is '|').
        The second part after the split (index 1) is used as the dictionary key.
        If splitter is None or an empty string, the full header is used.

    Returns
    -------
    tuple
        fasta_ids_dic : dict
            Dictionary mapping parsed identifiers to sequences.
        fasta_df : pandas.DataFrame
            DataFrame with columns:
                - 'Proteins': parsed identifiers
                - 'sequence': full sequence strings

    Raises
    ------
    IndexError
        If the FASTA header does not contain at least two parts when using a splitter.
    FileNotFoundError
        If the FASTA file path is invalid.

    Examples
    --------
    dic, df = make_dictionary_seqs("example.fasta")
    dic["P12345"]
    'MKTLLILTCLVAVALARPKH'
    df.head()
      Proteins            sequence
    0   P12345  MKTLLILTCLVAVALARPKH
    """
    fasta_ids_dic = {}
    for record in SeqIO.parse(fasta, "fasta"):
        if splitter:
            id = str(record.id).split("|")[1]
        else:
            id = str(record.id)
        fasta_ids_dic[id] = str(record.seq)
    fasta_df = pd.DataFrame(list(zip(list(fasta_ids_dic.keys()),list(fasta_ids_dic.values()))))
    fasta_df.columns  = ['Proteins','sequence']
    return fasta_ids_dic,fasta_df



def make_interproscan_annotaiton(annotation_file:str):
    """
    Parses an InterProScan annotation file and extracts entries with ATP-related domains.

    This function reads an InterProScan annotation TSV file (without a header), assigns
    meaningful column names, and filters for entries where the domain description contains
    the substring "ATP" (e.g., ATP-binding, ATPase, etc.).

    Parameters
    ----------
    annotation_file : str
        Path to the InterProScan annotation file (TSV format, no header expected).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing only the rows where the domain name includes "ATP".
        The DataFrame includes the following columns:
            - uniprot : str
            - hash : str
            - length : int
            - db : str
            - pfam : str
            - domain : str
            - start_position : int
            - end_position : int

    Notes
    -----
    - Assumes the file has at least 8 tab-separated columns.
    - No validation is performed on the structure or content of the file beyond column count.
    - Filtering is case-sensitive (i.e., only matches "ATP", not "atp").
    """
    annotation_df = pd.read_csv(annotation_file,header=None,sep='\t')
    annotation_df = annotation_df.iloc[:,range(8)]
    annotation_df.columns = [
    'uniprot',
    'hash',
    'length',
    'db',
    'pfam',
    'domain',
    'start_position',
    'end_position'
    ]
    return annotation_df[annotation_df['domain'].str.contains('ATP')]



def get_domain_part(x,start,end,tolerance=20) -> str:
    """
    Extracts a substring from a protein sequence with extended boundaries.

    This function extracts a region of a protein sequence around a specified
    start and end position, extending the region by a specified tolerance (in
    amino acids) on both sides. The function ensures that the extended range
    does not exceed the sequence boundaries.

    Parameters
    ----------
    x : str
        The full protein sequence.
    start : int
        The starting index of the domain (1-based, inclusive).
    end : int
        The ending index of the domain (1-based, inclusive).
    tolerance : int, optional
        Number of residues to extend on both sides of the domain (default is 20).

    Returns
    -------
    str
        The extracted domain region from the protein sequence, including the
        tolerance extension, if within bounds.

    Notes
    -----
    - Indexing is adjusted for 0-based Python slicing.
    - If the start or end with tolerance goes beyond the sequence, it is clipped
      to valid indices.
    - Prints the start and end indices used for slicing (for debugging).

    Examples
    --------
    get_domain_part("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 5, 12,tolerance=2)
    'CDEFGHIJKLMN'
    """
    start = int(start)
    end = int(end)
    protlength = len(x)
    if (start - tolerance) > 0:
        start = (start - tolerance) - 1
    else:
        start = 0

    if not (end  +  tolerance) > protlength:
        end = end + tolerance
    else:
        end = protlength  
    return x[start  :end]



def get_Cys_sasa_per_protein(uniprot_id,resids):
    """
    Retrieves the solvent accessible surface area (SASA) values for the sulfur atom (SG) 
    of cysteine residues specified by residue IDs from an AlphaFold SASA-annotated PDB file.

    Parameters
    ----------
    uniprot_id : str
        The UniProt identifier of the protein. The function expects a corresponding
        AlphaFold SASA PDB file named 'AF-{uniprot_id}-F1.sasa.pdb' in the working directory.

    resids : str
        A semicolon-separated string of residue IDs (integers) corresponding to cysteine residues.
        Example: "45;78;102"

    Returns
    -------
    str
        A semicolon-separated string of SASA values (as strings) for the sulfur atom (SG) of
        each cysteine residue in the input list. If SASA cannot be found or an error occurs
        for a residue, 'n.d.' (not determined) is returned for that residue.

    Notes
    -----
    - Internally uses a helper function `_get_CYS_sasa_for_residue_id` that attempts to extract
      the 'bfactor' value (used here to store SASA) for the SG atom of the specified residue.
    - The function handles exceptions gracefully, returning 'n.d.' for missing or problematic residues,
      and returns None silently if the entire process fails.

    Example
    -------
    get_Cys_sasa_per_protein("P12345", "45;78;102")
    '23.45;15.67;n.d.'
    """

    try:
        def _get_CYS_sasa_for_residue_id(uniprot_id,residue_id):
            try:
                pdb_df = PDB2dataFrame(uniprot_id,f'AF-{uniprot_id}-F1.sasa.pdb')
                return str(float(pdb_df[(pdb_df.residue_id==int(residue_id)) & (pdb_df.atom_name == 'SG')]['bfactor']))
            except:
                return 'n.d.'
        
        return (';').join([_get_CYS_sasa_for_residue_id(uniprot_id,x) for x in resids.split(';')])
    except:
        None



def calculate_SASA_from_alphafold_pdb(uniprot_id:str) -> None:
    """
    Calculates the solvent accessible surface area (SASA) of a protein structure
    from an AlphaFold PDB file and writes the SASA data to a new PDB file.

    Parameters
    ----------
    uniprot_id : str
        The UniProt identifier corresponding to the AlphaFold structure file 
        named 'AF-{uniprot_id}-F1.pdb' which must be present in the working directory.

    Returns
    -------
    None
        The function writes a new PDB file named 'AF-{uniprot_id}-F1.sasa.pdb' 
        with SASA values included.

    Notes
    -----
    - Uses the freesasa Python library to calculate SASA.
    - The AlphaFold PDB file must exist in the current directory before calling this function.
    - Any exceptions during calculation or file handling are caught, and a failure message is printed.
      This prevents the program from crashing but suppresses detailed error information.
    
    Example
    -------
    calculate_SASA_from_alphafold_pdb("P12345")
    This will read 'AF-P12345-F1.pdb' and write 'AF-P12345-F1.sasa.pdb'.
    """
    try:
        alphafold_ID = f'AF-{uniprot_id}-F1'
        structure = freesasa.Structure(f'{alphafold_ID}.pdb')
        result = freesasa.calc(structure)
        result.write_pdb(f'{alphafold_ID}.sasa.pdb')
    except:
        print(f'{uniprot_id} failed')


def replace_scores_in_aligned_values(list1, list2):
    """
    Replaces non-zero values in a list with new values from another list.

    This function takes two inputs:
    - `list1`: a string representation of a Python list containing numerical values,
      possibly with zeros indicating positions to keep unchanged.
    - `list2`: a list (or iterable) of values that will replace the non-zero elements
      in `list1` in the order they appear.

    The function returns a NumPy array where each non-zero element in the parsed `list1`
    is replaced by the corresponding value from `list2`.

    Parameters
    ----------
    list1 : str
        String representation of a list of floats, e.g. '[0.0, 1.5, 0.0, 2.3]'.
        Zero values indicate positions to be preserved.
    list2 : list or iterable of float-compatible
        List of replacement values for non-zero positions in `list1`.

    Returns
    -------
    numpy.ndarray
        Array with non-zero positions replaced by values from `list2`.

    Raises
    ------
    ValueError
        If the number of non-zero elements in `list1` does not match the length of `list2`.

    Examples
    --------
    replace_scores_in_aligned_values('[0, 2.0, 0, 3.5]', [10, 20])
    array([ 0., 10.,  0., 20.])
    """
    import ast
    import numpy as np
    try:
        list1 = ast.literal_eval(list1)
        list2 = list(map(float, list2))
        original = np.array(list1, dtype=float)
        replacement = np.array(list2, dtype=float)

        nonzero_indices = np.nonzero(original)[0]

        if len(nonzero_indices) != len(replacement):
            raise ValueError(f"Number of non-zero elements ({len(nonzero_indices)}) in list1 "
                            f"does not match length of list2 ({len(replacement)}).")

        result = original.copy()
        result[nonzero_indices] = replacement

        return result
    except:
        return None
    


def make_input_data(df, column):
    """
    Converts a DataFrame column containing array-like objects into a clean 2D DataFrame.

    This function stacks the values in the specified column (which should contain array-like entries, such as lists or arrays)
    into a 2D NumPy array, constructs a new DataFrame from it, and sets its index to the original `uniprot_id` column.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing a `column` of array-like values and a `uniprot_id` column.
    column : str
        The name of the column in `df` that contains the array-like values to be stacked.

    Returns
    -------
    df_clean : pandas.DataFrame
        A new DataFrame where each row corresponds to one entry in the original column, and the index is set to `uniprot_id`.

    Raises
    ------
    KeyError
        If `column` or `uniprot_id` does not exist in the input DataFrame.
    ValueError
        If the entries in the specified column are not array-like or are inconsistent in length.
    """
    df_clean = pd.DataFrame(np.vstack(df[column].values))
    df_clean.index = df.uniprot_id
    return df_clean


def get_matching_peptides_index(sites:str,digested_peptidess_intervals:str) -> str:
    """
    Find indexes of digested peptide intervals that contain any of the given sites.

    Parses a semicolon-separated list of numeric sites and a semicolon-separated list of
    interval strings (in 'start_end' format), then identifies which intervals contain
    at least one of the sites.

    Parameters
    ----------
    sites : str
        A semicolon-separated string of integers representing site positions (e.g., "71;87;129").
    digested_peptidess_intervals : str
        A semicolon-separated string of peptide intervals in 'start_end' format
        (e.g., "70_80;81_103;127_140").

    Returns
    -------
    str
        A semicolon-separated string of indexes (0-based) corresponding to intervals that contain
        at least one of the given sites.

    Example
    -------
    >>> get_matching_peptides_indexes("71;87;129", "70_80;81_103;127_140")
    '0;1;2'
    """

    numbers = list(map(int,sites.split(';')))
    intervals = [(int(start), int(end)) for start, end in (pair.split('_') for pair in digested_peptidess_intervals.split(';'))]

    def _interval_contains_any(interval, nums):
        start, end = interval
        return any(start <= num <= end for num in nums)
    return (';').join([str(i) for i, interval in enumerate(intervals) if _interval_contains_any(interval, numbers)])


def get_peptides_list_by_index(inds:str,list_peptides:str) -> str:
    """
    Select peptides by index from a semicolon-separated peptide list.

    Parses `inds` as a semicolon-separated list of integer indexes, and uses them
    to extract peptides from the `list_peptides` string.

    Parameters
    ----------
    inds : str
        A semicolon-separated string of integers representing the indexes of the peptides to select.
        Example: "0;2;4"
    
    list_peptides : str
        A semicolon-separated string of peptide sequences.
        Example: "PEP1;PEP2;PEP3;PEP4;PEP5"

    Returns
    -------
    str or None
        A semicolon-separated string of selected peptides, or None if an error occurs (e.g., index out of range or invalid input).

    Example
    -------
    >>> get_final_peptides("0;2", "A;B;C")
    'A;C'
    """
    try:
        selected_inds = list(map(int,inds.split(';')))
        list_peptides = list_peptides.split(';')
        return (';').join([list_peptides[i] for i in selected_inds])
    except:
        return None