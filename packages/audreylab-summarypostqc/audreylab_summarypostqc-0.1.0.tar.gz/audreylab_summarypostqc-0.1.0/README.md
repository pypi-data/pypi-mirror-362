# README.md
# AudreyLab-SummaryPostQC

Un outil en ligne de commande pour :
- Générer des graphiques Manhattan et QQ
- Annoter les SNPs significatifs avec Ensembl BioMart et MyVariant.info
- Filtrer et résumer les statistiques de GWAS

## Installation
```bash
pip install AudreyLab-SummaryPostQC
```

## Usage
```bash
audreylab-summarypostqc summary --input results.tsv

# Plots

audreylab-summarypostqc plot --input results.tsv --output figs/

# Annotation

audreylab-summarypostqc annotate --input results.tsv --output annotated.tsv --threshold 5e-5
```

## Auteur
Etienne Kabongo (AudreyLab)

# LICENSE
MIT License

Copyright (c) 2025 Etienne Kabongo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
