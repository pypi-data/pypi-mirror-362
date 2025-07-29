from audreylab_summarypostqc.summary import summarize_gwas

def test_summary():
    result = summarize_gwas("tests/test_data.tsv", pval_threshold=0.05)
    assert isinstance(result, dict)
