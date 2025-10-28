from src.ai_resume_analyzer.embeddings.encoder import Encoder
def test_encode_small():
    enc = Encoder()
    texts = ["hello world", "machine learning engineer with python and sql"]
    embs = enc.encode(texts)
    assert embs.shape[0] == 2
