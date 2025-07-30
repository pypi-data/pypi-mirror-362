# AudreyLab-SummaryPostQC

[![PyPI version](https://badge.fury.io/py/audreylab-summarypostqc.svg)](https://pypi.org/project/audreylab-summarypostqc/)
[![License](https://img.shields.io/github/license/EtienneNtumba/audreylab-summarypostqc)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)

**AudreyLab-SummaryPostQC** is a robust and lightweight Python command-line utility for visualizing genome-wide association study (GWAS) summary statistics. It provides clear, publication-ready **QQ plots** and **Manhattan plots**, and computes the **genomic inflation factor** (λGC) as a key quality control metric.

> Developed by **Etienne Kabongo**, member of the [Audrey Grant Lab](https://www.mcgill.ca/genepi/), McGill University.  
> Source code: [github.com/EtienneNtumba/audreylab-summarypostqc](https://github.com/EtienneNtumba/audreylab-summarypostqc)

---

## 🧬 Use Case

This tool is particularly useful for:
- Post-QC visualization of GWAS results (e.g., after using REGENIE or PLINK)
- Checking for population stratification or inflation via λGC
- Generating Manhattan plots for initial signal discovery

---

## 🔧 Features

- ✅ Parses post-QC GWAS summary files (TSV/CSV)
- ✅ Filters out invalid or missing P-values
- ✅ Calculates the genomic inflation factor λGC
- ✅ Generates high-resolution QQ plots
- ✅ Generates Manhattan plots with chromosome separation
- ✅ Supports custom output filenames and minimal dependencies

---

## 📦 Installation

Install via [PyPI](https://pypi.org/project/audreylab-summarypostqc/):

```bash
pip install audreylab-summarypostqc
```
## 🚀 Usage

After installation, you can call the tool from the command line using:

```bash
audreylab-summarypostqc --input <your_file.txt> --out <prefix>
```
This generates the following files:

- `<prefix>_qqplot.png`
- `<prefix>_manhattan.png`

### Example 1: Basic usage

```bash
audreylab-summarypostqc --input results/gwas_summary.txt --out results/plots
```
## 📈 Input File Format

Your input file should be a **tab-separated** (`.tsv` or `.txt`) file with the following required columns:

| Column | Description                          |
|--------|--------------------------------------|
| Chr    | Chromosome number (1–22)             |
| Pos    | Base pair position                   |
| Pval   | P-value of association               |

⚠️ **Missing or invalid values** will be excluded from the plots.

---

## 🧪 Output

- 📊 **QQ Plot**: Observed vs. expected -log10(P) values, includes calculated **λGC**
- 🗺️ **Manhattan Plot**: P-values across all chromosomes, with genome-wide significance threshold line

# audreylab-summarypostqc

