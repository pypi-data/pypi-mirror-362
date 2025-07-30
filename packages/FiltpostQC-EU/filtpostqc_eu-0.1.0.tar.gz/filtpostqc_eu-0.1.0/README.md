# FiltpostQC-EU

**FiltpostQC-EU** is a command-line tool designed to apply post-GWAS quality control (QC) filtering to merged summary statistics files (e.g., from REGENIE) using an external variant filter file. It supports filtered output, FUMA-compatible output, or both.

Developed by **Etienne Kabongo**, research assistant at the Audrey Grant Lab.

---

## 🚀 Features

- Filters merged `.regenie` output files using a QC reference file (e.g., from European ancestry filtering)
- Automatically extracts `Beta` and `SE` from REGENIE-style `Info` fields
- Outputs:
  - Filtered GWAS summary statistics
  - FUMA-compatible format (Chromosome, Position, SNP, Alleles, Beta, SE, P-value, etc.)
- Fast and lightweight
- Compatible with Slurm clusters and large datasets (millions of variants)

---

## 📦 Installation

Install directly from PyPI:

```bash
pip install FiltpostQC-EU
```
