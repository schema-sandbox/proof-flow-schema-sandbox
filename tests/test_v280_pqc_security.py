"""
Tests for ProofFlow v28.0 (Post-Quantum Kyber & Dilithium Cryptographic Security Suite)

Covers:
    - MlKemKeyExchange (ML-KEM Keypair generation & encapsulation)
    - MlDsaDigitalSignature (ML-DSA lattice signature generation & verification)
    - CryptographicAuditLog (PQC signed audit log chain appending)
"""

from __future__ import annotations

from schemamath_api.pqc_security import (
    CryptographicAuditLog,
    MlDsaDigitalSignature,
    MlKemKeyExchange,
)


class TestPqcSecurity:
    def test_ml_kem_key_exchange(self):
        kem = MlKemKeyExchange()
        keypair = kem.generate_keypair("Kyber-768")
        assert keypair.public_key.startswith("ml_kem_pk_")

        encap = kem.encapsulate(keypair.public_key)
        assert len(encap.shared_secret) == 64

    def test_ml_dsa_signature_and_audit_log(self):
        signer = MlDsaDigitalSignature()
        kem = MlKemKeyExchange()
        kp = kem.generate_keypair("Kyber-1024")

        sig = signer.sign("admin_action_grant", kp.secret_key)
        assert signer.verify("admin_action_grant", sig, kp.public_key) is True

        audit = CryptographicAuditLog(signer, kp)
        rec = audit.append_log("log_101", "USER_GRANT")
        assert rec.signature.startswith("ml_dsa_sig_")
