from src.inventory import (
    load_inventory,
    analyze_inventory,
    export_inventory,
)


def main():
    input_file = "data/raw/crypto_inventory.csv"
    output_file = "data/processed/risk_assessment.csv"

    try:
        inventory = load_inventory(input_file)
        results = analyze_inventory(inventory)
        export_inventory(results, output_file)

        print("\nCRYPTOGUARD - INVENTORY ANALYSIS")
        print("=" * 50)

        print(results[
            ["asset_id", "algorithm", "quantum_risk", "risk_score"]
        ].to_string(index=False))

        print(f"\nAnalyzed assets: {len(results)}")
        print(f"Results saved to: {output_file}")

    except (ValueError, FileNotFoundError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()