"""
Tests for ProofFlow v42.0 (E5 Independent Clean Rebuild Packer)

Covers:
    - E5RebuildPacker (E5 package generation & lakefile manifest packing)
"""

from __future__ import annotations

from schemamath_api.e5_rebuild_packer import E5RebuildPacker


class TestE5RebuildPacker:
    def test_pack_e5_proof(self):
        packer = E5RebuildPacker()
        pkg_ok = packer.pack_e5_proof("fermat_last", "theorem fermat_last : True := by trivial")
        assert pkg_ok.evidence_level == "E5"
        assert pkg_ok.zero_sorry_verified is False
        assert "git_commit" in pkg_ok.lakefile_manifest

        pkg_sorry = packer.pack_e5_proof("open_problem", "theorem open_problem : False := by sorry")
        assert pkg_sorry.zero_sorry_verified is False
