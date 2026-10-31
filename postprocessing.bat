call applauncher.bat ContactreesAnnotator -threshold 50 -burnin 10 beast\hadith_motifs_only.trees beast\hadith_motifs_only_summary_tree.tree
move loanwords.log beast\hadith_motifs_only_loanwords.log
call applauncher.bat ContactreesAnnotator -threshold 50 -burnin 10 beast\hadith_mrca_priors.trees beast\hadith_mrca_priors_summary_tree.tree
move loanwords.log beast\hadith_mrca_priors_loanwords.log
call applauncher.bat ContactreesAnnotator -threshold 50 -burnin 10 beast\hadith_no_mrca_priors.trees beast\hadith_no_mrca_priors_summary_tree.tree
move loanwords.log beast\hadith_no_mrca_priors_loanwords.log
call python py\get_maximum_likelihood_tree.py beast\hadith_motifs_only.log beast\hadith_motifs_only.trees beast\hadith_motifs_only_ml_tree.tree
call python py\get_maximum_likelihood_tree.py beast\hadith_mrca_priors.log beast\hadith_mrca_priors.trees beast\hadith_mrca_priors_ml_tree.tree
call python py\get_maximum_likelihood_tree.py beast\hadith_no_mrca_priors.log beast\hadith_no_mrca_priors.trees beast\hadith_no_mrca_priors_ml_tree.tree
call python py\get_reticulations_distribution.py --burnin 0.1 beast\hadith_motifs_only.trees beast\hadith_motifs_only_reticulation_posteriors.log
call python py\get_reticulations_distribution.py --burnin 0.1 beast\hadith_mrca_priors.trees beast\hadith_mrca_priors_reticulation_posteriors.log
call python py\get_reticulations_distribution.py --burnin 0.1 beast\hadith_no_mrca_priors.trees beast\hadith_no_mrca_priors_reticulation_posteriors.log
call python py\get_ancestral_state_posteriors.py --burnin 0.1 beast\hadith_motifs_only.ancestral.log beast\hadith_motifs_only.xml beast\hadith_motifs_only_root_state_posteriors.yaml
call python py\get_ancestral_state_posteriors.py --burnin 0.1 beast\hadith_mrca_priors.ancestral.log beast\hadith_mrca_priors.xml beast\hadith_mrca_priors_root_state_posteriors.yaml
call python py\get_ancestral_state_posteriors.py --burnin 0.1 beast\hadith_no_mrca_priors.ancestral.log beast\hadith_no_mrca_priors.xml beast\hadith_no_mrca_priors_root_state_posteriors.yaml