applauncher.bat ContactreesAnnotator -threshold 50 -burnin 10 beast\hadith_motifs_only.trees beast\hadith_motifs_only_summary.tree
ren beast\loanwords.txt beast\hadith_motifs_only_loanwords.txt
applauncher.bat ContactreesAnnotator -threshold 50 -burnin 10 beast\hadith_mrca_priors.trees beast\hadith_mrca_priors_summary.tree
ren beast\loanwords.txt beast\hadith_mrca_priors_loanwords.txt
applauncher.bat ContactreesAnnotator -threshold 50 -burnin 10 beast\hadith_no_mrca_priors.trees beast\hadith_no_mrca_priors_summary.tree
ren beast\loanwords.txt beast\hadith_no_mrca_priors_loanwords.txt
python py\get_maximum_likelihood_tree.py beast\hadith_motifs_only.log beast\hadith_motifs_only.trees beast\hadith_motifs_only_ml_tree.tree
python py\get_maximum_likelihood_tree.py beast\hadith_mrca_priors.log beast\hadith_mrca_priors.trees beast\hadith_mrca_priors_ml_tree.tree
python py\get_maximum_likelihood_tree.py beast\hadith_no_mrca_priors.log beast\hadith_no_mrca_priors.trees beast\hadith_no_mrca_priors_ml_tree.tree
python py\get_reticulations_distribution.py --burnin 0.1 beast\hadith_motifs_only.trees beast\hadith_motifs_only_reticulation_posteriors.txt
python py\get_reticulations_distribution.py --burnin 0.1 beast\hadith_mrca_priors.trees beast\hadith_mrca_priors_reticulation_posteriors.txt
python py\get_reticulations_distribution.py --burnin 0.1 beast\hadith_no_mrca_priors.trees beast\hadith_no_mrca_priors_reticulation_posteriors.txt
python py\get_ancestral_state_posteriors.py --burnin 0.1 beast\hadith_motifs_only.ancestral.log beast\hadith_motifs_only.xml beast\hadith_motifs_only_root_state_posteriors.yaml
python py\get_ancestral_state_posteriors.py --burnin 0.1 beast\hadith_mrca_priors.ancestral.log beast\hadith_mrca_priors.xml beast\hadith_mrca_priors_root_state_posteriors.yaml
python py\get_ancestral_state_posteriors.py --burnin 0.1 beast\hadith_no_mrca_priors.ancestral.log beast\hadith_no_mrca_priors.xml beast\hadith_no_mrca_priors_root_state_posteriors.yaml