
"""
CryptoGuard: Post-quantum cryptographic migration recommendations.

Recommendations are preliminary guidance. Final choices must be validated
against system requirements, applicable standards, and implementation support.
"""

from src.risk_scoring import normalize_algorithm


MIGRATION_GUIDANCE = {
    "RSA": {
        "category": "Public-key cryptography",
        "action": "Prioritize migration planning",
        "recommendation": (
            "Evaluate ML-KEM for key establishment and ML-DSA or SLH-DSA "
            "for digital signatures, depending on the asset's function."
        ),
    },
    "DH": {
        "category": "Key establishment",
        "action": "Prioritize migration planning",
        "recommendation": (
            "Evaluate ML-KEM as a post-quantum key-establishment alternative."
        ),
    },
    "ECDH": {
        "category": "Key establishment",
        "action": "Prioritize migration planning",
        "recommendation": (
            "Evaluate ML-KEM as a post-quantum key-establishment alternative."
        ),
    },
    "ECDSA": {
        "category": "Digital signatures",
        "action": "Prioritize migration planning",
        "recommendation": (
            "Evaluate ML-DSA or SLH-DSA for digital-signature use cases."
        ),
    },
    "DSA": {
        "category": "Digital signatures",
        "action": "Prioritize migration planning",
        "recommendation": (
            "Evaluate ML-DSA or SLH-DSA for digital-signature use cases."
        ),
    },
    "ED25519": {
        "category": "Digital signatures",
        "action": "Prioritize migration planning",
        "recommendation": (
            "Evaluate ML-DSA or SLH-DSA for digital-signature use cases."
        ),
    },
    "AES": {
        "category": "Symmetric encryption",
        "action": "Review security policy",
        "recommendation": (
            "Verify key size, mode, implementation, and security requirements. "
            "Do not automatically replace AES solely because of quantum risk."
        ),
    },
    "3DES": {
        "category": "Legacy symmetric encryption",
        "action": "Plan modernization",
        "recommendation": (
            "Review and plan replacement with an approved modern symmetric "
            "cipher, following applicable policy and compatibility requirements."
        ),
    },
    "CHACHA20": {
        "category": "Symmetric encryption",
        "action": "Review security policy",
        "recommendation": (
            "Review key size, mode, implementation, and applicable security policy."
        ),
    },
}


def recommend_migration(algorithm: str) -> dict:
    """Return preliminary migration guidance for an algorithm."""
    normalized = normalize_algorithm(algorithm)

    if normalized in {"MLKEM", "MLDSA", "SLHDSA"}:
        return {
            "category": "Post-quantum cryptography",
            "action": "Validate implementation",
            "recommendation": (
                "Verify the algorithm variant, parameters, implementation, "
                "and applicable standards before deployment."
            ),
        }

    guidance = MIGRATION_GUIDANCE.get(normalized)

    if guidance:
        return guidance.copy()

    return {
        "category": "Unclassified cryptography",
        "action": "Manual review required",
        "recommendation": (
            "Identify the algorithm, implementation, key parameters, and "
            "cryptographic purpose before selecting a migration path."
        ),
    }

