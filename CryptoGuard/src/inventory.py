import pandas as pd
from pathlib import Path

from src.risk_scoring import assess_algorithm, calculate_risk_score
from src.migration import recommend_migration


REQUIRED_COLUMNS = [
    "asset_id",
    "asset_name",
    "algorithm",
    "data_sensitivity",
    "exposure",
]


def load_inventory(file_path):
    """Load and validate a cryptographic inventory CSV."""
    df = pd.read_csv(file_path)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    if df.empty:
        raise ValueError("The inventory CSV contains no assets.")

    for column in REQUIRED_COLUMNS:
        if df[column].isna().any():
            raise ValueError(
                f"Column '{column}' contains empty values."
            )

    return df


def analyze_inventory(df):
    """Assess cryptographic risks and migration guidance for each asset."""
    results = []

    for _, row in df.iterrows():
        algorithm = str(row["algorithm"])

        assessment = assess_algorithm(algorithm)

        score = calculate_risk_score(
            algorithm,
            str(row["data_sensitivity"]),
            str(row["exposure"]),
        )

        migration = recommend_migration(algorithm)

        results.append({
            "asset_id": row["asset_id"],
            "asset_name": row["asset_name"],
            "algorithm": row["algorithm"],
            "data_sensitivity": row["data_sensitivity"],
            "exposure": row["exposure"],
            "quantum_risk": assessment["quantum_risk"],
            "risk_score": score,
            "risk_reason": assessment["reason"],
            "migration_options": ", ".join(
                assessment["pqc_options"]
            ),
            "migration_category": migration["category"],
            "migration_action": migration["action"],
            "migration_recommendation": migration["recommendation"],
        })

    return pd.DataFrame(results)


def export_inventory(df, output_path):
    """Save assessment results to a CSV file."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return output