import pandas as pd
from pybiomart import Server
from time import sleep
from myvariant import MyVariantInfo
import sys
import argparse

# ----------- Argument parser ----------- #
parser = argparse.ArgumentParser(description="Annoter les SNPs significatifs avec BioMart et MyVariant.info")
parser.add_argument("input_file", help="Fichier d'entrée TSV (résumé GWAS)")
parser.add_argument("output_file", help="Fichier de sortie TSV avec annotations")
parser.add_argument("--pval-threshold", type=float, default=5e-2,
                    help="Seuil de p-value pour les SNPs significatifs (défaut: 5e-2)")
args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
pval_threshold = args.pval_threshold

# ----------- Chargement des données ----------- #
df = pd.read_csv(input_file, sep="\t")

# Filtrer les SNPs significatifs selon le seuil
signif_df = df[df["Pval"] < pval_threshold].copy()

if signif_df.empty:
    raise ValueError(f"❌ Aucun SNP significatif trouvé avec Pval < {pval_threshold}")

snp_ids = signif_df["Name"].dropna().unique().tolist()

# ----------- Annotation BioMart ----------- #
server = Server(host='http://www.ensembl.org')
dataset = server.marts['ENSEMBL_MART_SNP'].datasets['hsapiens_snp']

batch_size = 500
annotated = []

for i in range(0, len(snp_ids), batch_size):
    batch = snp_ids[i:i+batch_size]
    try:
        result = dataset.query(attributes=[
            'refsnp_id', 'chr_name', 'chrom_start',
            'ensembl_gene_stable_id', 'associated_gene', 'consequence_type_tv'
        ],
        filters={'snp_filter': batch})
        annotated.append(result)
    except Exception as e:
        print(f"⚠️ Problème avec le batch {i}-{i+batch_size}: {e}")
    sleep(1)

annotation_df = pd.concat(annotated).drop_duplicates()
annotation_df.columns = ["SNP", "Chr", "Pos", "Ensembl_ID", "Gene_Name", "Consequence"]

# ----------- Annotation MyVariant.info ----------- #
mv = MyVariantInfo()
mv_batch = mv.getvariants(snp_ids, fields="clinvar.rcv.clinical_significance,cadd.phred,dbsnp.alleles", species="human")

mv_annotations = []
for entry in mv_batch:
    rsid = entry.get("query")
    rcv_entry = entry.get("clinvar", {}).get("rcv", {})
    if isinstance(rcv_entry, list):
        clinvar = rcv_entry[0].get("clinical_significance", None) if rcv_entry else None
    elif isinstance(rcv_entry, dict):
        clinvar = rcv_entry.get("clinical_significance", None)
    else:
        clinvar = None
    cadd = entry.get("cadd", {}).get("phred", None)
    mv_annotations.append({
        "SNP": rsid,
        "ClinSig": clinvar,
        "CADD": cadd
    })

mv_df = pd.DataFrame(mv_annotations)

# ----------- Fusion et export ----------- #
final_df = signif_df.merge(annotation_df[["SNP", "Ensembl_ID", "Gene_Name", "Consequence"]],
                           how="left", left_on="Name", right_on="SNP")

final_df = final_df.merge(mv_df, how="left", on="SNP")

# Colonnes finales
final_df = final_df[["Chr", "SNP", "Pos", "Ref", "Alt", "Pval",
                     "Ensembl_ID", "Gene_Name", "Consequence", "ClinSig", "CADD"]]

# Trier par ordre croissant de la Pval
final_df = final_df.sort_values(by="Pval")

# Exporter au format TSV
final_df.to_csv(output_file, sep=",", index=False)

print(f"✅ Résultats sauvegardés dans : {output_file}")
