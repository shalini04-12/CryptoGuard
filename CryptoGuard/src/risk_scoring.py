"""
CryptoGuard: Preliminary cryptographic risk assessment.

Scores are illustrative prototype triage scores, not official NIST
or Qiskit Fall Fest scoring formulas.
"""

from typing import Any


ALGORITHM_INFO = {
    "RSA": {
        "quantum_risk": "High",
        "reason": (
            "A sufficiently capable quantum computer could threaten RSA."
        ),
        "pqc_options": ["ML-KEM for key establishment", "ML-DSA for signatures"],
    },
    "DH": {
        "quantum_risk": "High",
        "reason": (
            "Finite-field Diffie-Hellman is vulnerable to a sufficiently "
            "capable quantum attack."
        ),
        "pqc_options": ["ML-KEM for key establishment"],
    },
    "ECDH": {
        "quantum_risk": "High",
        "reason": (
            "Elliptic-curve Diffie-Hellman is vulnerable to a sufficiently "
            "capable quantum attack."
        ),
        "pqc_options": ["ML-KEM for key establishment"],
    },
    "ECDSA": {
        "quantum_risk": "High",
        "reason": (
            "Elliptic-curve digital signatures are vulnerable to a "
            "sufficiently capable quantum attack."
        ),
        "pqc_options": ["ML-DSA", "SLH-DSA"],
    },
    "DSA": {
        "quantum_risk": "High",
        "reason": (
            "Classical discrete-logarithm signatures are vulnerable to "
            "a sufficiently capable quantum attack."
        ),
        "pqc_options": ["ML-DSA", "SLH-DSA"],
    },
    "ED25519": {
        "quantum_risk": "High",
        "reason": (
            "Ed25519 is an elliptic-curve digital signature scheme."
        ),
        "pqc_options": ["ML-DSA", "SLH-DSA"],
    },
    "AES": {
        "quantum_risk": "Moderate",
        "reason": (
            "Symmetric encryption requires a key-size and security-margin "
            "review under quantum threat models."
        ),
        "pqc_options": ["Review key size and cryptographic policy"],
    },
    "3DES": {
        "quantum_risk": "Review",
        "reason": (
            "Legacy cipher with significant classical security and "
            "lifecycle concerns."
        ),
        "pqc_options": [
            "Plan replacement with an approved modern symmetric cipher"
        ],
    },
    "CHACHA20": {
        "quantum_risk": "Moderate",
        "reason": (
            "Symmetric cryptography requires a security-margin review, "
            "not automatic post-quantum replacement."
        ),
        "pqc_options": ["Review key size and cryptographic policy"],
    },
}


def normalize_algorithm(algorithm: str) -> str:
    """Normalize common algorithm names and aliases."""
    normalized = str(algorithm).strip().upper()
    normalized = normalized.replace("-", "").replace("_", "")
    normalized = normalized.replace(" ", "")

    aliases = {
        "DIFFIEHELLMAN": "DH",
        "ECDIFFIEHELLMAN": "ECDH",
        "TRIPLEDES": "3DES",
        "DES3": "3DES",
        "CHACHA20POLY1305": "CHACHA20",
        "ED25519": "ED25519",
        "MLKEM": "MLKEM",
        "MLDSA": "MLDSA",
        "SLHDSA": "SLHDSA",
        "AES128": "AES",
        "AES192": "AES",
        "AES256": "AES",
    }

    return aliases.get(normalized, normalized)


def assess_algorithm(algorithm: str) -> dict[str, Any]:
    """Return a preliminary classification for a known algorithm."""
    normalized = normalize_algorithm(algorithm)

    # Recognized post-quantum algorithm families.
    if normalized in {"MLKEM", "MLDSA", "SLHDSA"}:
        return {
            "quantum_risk": "PQC",
            "reason": (
                "Recognized post-quantum algorithm family. "
                "Implementation, parameters, and configuration still need review."
            ),
            "pqc_options": [
                "Verify implementation, parameters, and applicable standards"
            ],
        }

    if normalized in ALGORITHM_INFO:
        return ALGORITHM_INFO[normalized].copy()

    return {
        "quantum_risk": "Unknown",
        "reason": (
            "Algorithm not recognized; manual cryptographic review is required."
        ),
        "pqc_options": [
            "Identify the algorithm and implementation before planning migration"
        ],
    }


def calculate_risk_score(
    algorithm: str,
    data_sensitivity: str,
    exposure: str,
) -> int:
    """
    Calculate an illustrative 0-100 prioritization score.

    This is a prototype triage score, not an official standard.
    """
    assessment = assess_algorithm(algorithm)
    risk_level = assessment["quantum_risk"]

    algorithm_points = {
        "High": 70,
        "Moderate": 35,
        "Review": 45,
        "PQC": 10,
        "Unknown": 50,
    }.get(risk_level, 50)

    sensitivity = str(data_sensitivity).strip().title()
    exposure_level = str(exposure).strip().casefold()

    sensitivity_points = {
        "High": 20,
        "Medium": 12,
        "Low": 5,
    }.get(sensitivity, 12)

    exposure_points = {
        "internet-facing": 10,
        "internal": 5,
        "isolated": 0,
    }.get(exposure_level, 5)

    score = algorithm_points + sensitivity_points + exposure_points

    return min(100, max(0, score))