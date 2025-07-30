from minivectordb.embedding_model import EmbeddingModel

def test_load_onnx_model():
    quant_model = EmbeddingModel(use_quantized_onnx_model=True)
    assert quant_model.model is not None, "Onnx model should be loaded"

    embedding = quant_model.extract_embeddings("This is a sample text")
    assert embedding is not None, "Embedding should be extracted from onnx model"

    embedding = quant_model.extract_embeddings("This is a sample text")

    # Should be 512
    assert len(embedding) == 512, "Embedding should have 512 dimensions from onnx model"
