import typer
from .plot import generate_manhattan_qq
from .annotate import annotate_significant_snps
from .summary import summarize_gwas

app = typer.Typer(help="AudreyLab-SummaryPostQC: Visualisation et annotation de GWAS summary stats")

@app.command()
def summary(input: str, threshold: float = 5e-8):
    """Affiche un résumé de base des statistiques GWAS."""
    result = summarize_gwas(input, threshold)
    for k, v in result.items():
        typer.echo(f"{k}: {v}")

@app.command()
def plot(input: str, output: str = ".", trait: str = "Trait"):
    """Génère les plots Manhattan et QQ."""
    generate_manhattan_qq(input, output, trait)

@app.command()
def annotate(input: str, output: str, threshold: float = 5e-2):
    """Annote les SNPs significatifs via BioMart et MyVariant.info"""
    annotate_significant_snps(input, output, threshold)

if __name__ == "__main__":
    app()
