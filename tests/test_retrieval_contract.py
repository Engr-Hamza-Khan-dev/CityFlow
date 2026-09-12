def test_member2_retrieval_contract_shape():
    expected_keys = {"evidence_id", "text", "source", "metadata", "distance"}
    sample = {
        "evidence_id": "source:chunk-1",
        "text": "Government requirement text.",
        "source": "source.pdf",
        "metadata": {},
        "distance": 0.12,
    }
    assert expected_keys.issubset(sample.keys())
