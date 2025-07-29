# biofoldutils/__init__.py
from .core import (
           get_min_max_residueIDs_from_reference_residue,
           PDB2dataFrame,
           calculate_distance_from_ref_point,
           find_max_tuple,
           find_min_tuple,
           download_alphafold_pdb_from_uniprot_id,
	   make_input_data,
	   find_motif_positions,
	   find_residue_position,
	   calculte_conservation_scores_per_residue,
	   run_interproscan,
	   run_clustal,
	   parse_fasta_sequences,
	   convert_aln2fasta,
	   make_fasta_file,
	   make_dictionary_seqs,
	   make_interproscan_annotaiton,
	   get_domain_part,
	   get_Cys_sasa_per_protein,
	   calculate_SASA_from_alphafold_pdb,
	   replace_scores_in_aligned_values

                                    # Add more as needed
                                    )


from .digest import (
get_num_ibaq_peptides_per_protein,
make_iBaq_mapping_df,
get_digested_peptides,
get_peptide_to_protein_map,
get_ibaq_peptide_to_protein_map

)
