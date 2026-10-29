# hadhist-pilot
Pilot BEAST 2 analyses for the HadHist ERC project proposal.

## About This Project

This project contains BEAST 2 input files, analysis outputs, and postprocessing scripts for a proof-of-concept for the HadHist ERC project proposal.
The input files are based on the hadith dataset detailed at https://github.com/yoobie-doo/JDH-Medina-Article.
The BEAST 2 analyses were run on Windows; to replicate the analysis on Mac or Linux, you will need to make slight modifications to the .bat executables (namely, removing the .bat extension from both files, changing the `ren` command in `preprocessing.bat` to `mv`, and changing back-slashes to forward-slashes in directory references).

All analyses were performed with BEAST 2.7.7.
BEAST was run with an RNG seed of 1337 and 8 threads.
The tree plots were produced using IcyTree (https://icytree.org/), and the posterior distribution plots were generated with Tracer.
To run the analysis, you must have the BEASTLabs, morphmodels, AlmostDistributions, BDSKY, EpochClockModel, and contacTrees packages installed through the BEAST package manager (accessible through BEAUti).