import numpy as np
from src.ai_resume_analyzer.embeddings.faiss_index import build_index, load_index, search
def test_index_build_search(tmp_path):
    emb = np.eye(4, dtype="float32")
    ids = ["a","b","c","d"]
    out = str(tmp_path / "test.index")
    build_index(emb, ids, out)
    idx = load_index(out)
    # query first vector
    res = search(idx, emb[0], k=2)
    assert len(res) >= 1
