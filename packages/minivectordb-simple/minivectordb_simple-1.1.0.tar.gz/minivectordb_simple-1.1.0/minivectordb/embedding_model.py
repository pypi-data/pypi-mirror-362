from onnxruntime_extensions import get_library_path
import onnxruntime as ort
from os import cpu_count
import pkg_resources

class EmbeddingModel:
   
    def __init__(self, use_quantized_onnx_model = True, onnx_model_cpu_core_count=None):
        self.onnx_model_path = pkg_resources.resource_filename('minivectordb', 'resources/embedding_model_quantized.onnx')
        self.use_quantized_onnx_model = use_quantized_onnx_model
        self.onnx_model_cpu_core_count = onnx_model_cpu_core_count

        assert isinstance(self.onnx_model_cpu_core_count, int) or self.onnx_model_cpu_core_count is None
        
        if self.use_quantized_onnx_model:
            self.load_onnx_model()
        else:
            self.load_alternative_model()

    def load_onnx_model(self):
        cpu_core_count = cpu_count() if self.onnx_model_cpu_core_count is None else self.onnx_model_cpu_core_count
        _options = ort.SessionOptions()
        _options.inter_op_num_threads, _options.intra_op_num_threads = cpu_core_count, cpu_core_count
        _options.register_custom_ops_library(get_library_path())
        _providers = ["CPUExecutionProvider"]

        self.model = ort.InferenceSession(
            path_or_bytes = self.onnx_model_path,
            sess_options=_options,
            providers=_providers
        )

    def extract_embeddings_quant_onnx(self, text):
        return self.model.run(output_names=["outputs"], input_feed={"inputs": [text]})[0][0]
    
    def extract_embeddings(self, text):
        return self.extract_embeddings_quant_onnx(text)
