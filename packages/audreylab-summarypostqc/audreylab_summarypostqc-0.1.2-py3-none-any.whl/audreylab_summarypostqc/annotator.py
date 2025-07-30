# audreylab_summarypostqc/annotator.py

import pandas as pd
from pybiomart import Server
from time import sleep
from myvariant import MyVariantInfo

def annotate_gwas(input_file, output_file, pval_threshold=5e-2):
    df = pd.read_csv(input_file, sep="\t")
    signif_df = df[df["Pval"] < pval_threshold].copy()

    if signif_df.empty:
        raise ValueError(f"❌ Aucun SNP significatif trouvé avec Pval < {pval_threshold}")

    snp_ids = signif_df["Name"].dropna().unique().tolist()

    # BioMart annotation
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
            ], filters={'snp_filter': batch})
            annotated.append(result)
        except Exception as e:
            print(f"⚠️ Problème avec le batch {i}-{i+batch_size}: {e}")
        sleep(1)

    annotation_df = pd.concat(annotated).drop_duplicates()
    annotation_df.columns = ["SNP", "Chr", "Pos", "Ensembl_ID", "Gene_Name", "Consequence"]

    # MyVariant.info
    mv = MyVariantInfo()
    mv_batch = mv.getvariants(snp_ids, fields="clinvar.rcv.clinical_significance,cadd.phred", species="human")

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
        mv_annotations.append({"SNP": rsid, "ClinSig": clinvar, "CADD": cadd})

    mv_df = pd.DataFrame(mv_annotations)

    # Merge
    final_df = signif_df.merge(annotation_df[["SNP", "Ensembl_ID", "Gene_Name", "Consequence"]],
                               how="left", left_on="Name", right_on="SNP")

    final_df = final_df.merge(mv_df, how="left", on="SNP")
    final_df = final_df[["Chr", "SNP", "Pos", "Ref", "Alt", "Pval",
                         "Ensembl_ID", "Gene_Name", "Consequence", "ClinSig", "CADD"]]
    final_df = final_df.sort_values(by="Pval")

    final_df.to_csv(output_file, sep=",", index=False)
    print(f"✅ Résultats sauvegardés dans : {output_file}")

