import torch, os

from ...core.interfaces import AuditOps
from ...plugins.registry import register
from ...utils.mtsq_utils import MTSQConfig, apply_mtsq_to_model, quantize_model_weights
from ...utils.onnx_utils import export_mtsq_to_onnx, create_optimized_session, benchmark_onnx_model, validate_onnx_accuracy, InputQuantizer



@register('audit_ops', 'mtsq_quantization')
class MTSQ_Quantizer(AuditOps):
    """MTSQ Quantizer"""

    def __init__(self, bits, symmetric, per_channel, power_of_two_clipping, learning_rate, max_iteration, patience, save_path, **kwargs):
        self.bits = bits
        self.symmetric = symmetric
        self.per_channel = per_channel
        self.power_of_two_clipping = power_of_two_clipping
        self.learning_rate = learning_rate
        self.max_iteration = max_iteration
        self.patience = patience
        self.save_path = save_path
        
    def quantize(self, model, device, dummy_audio=torch.randn((12,64000))):
        fp32_model = model.eval()
        test_input = dummy_audio.to(device)
        
        config = MTSQConfig(bits=self.bits,
                            symmetric=self.symmetric,
                            per_channel=self.per_channel,
                            power_of_two_clipping=self.power_of_two_clipping,
                            learning_rate=self.learning_rate,
                            max_iterations=self.max_iteration,
                            patience=self.patience)

        quant_model = apply_mtsq_to_model(fp32_model, config)

        first_params = quantize_model_weights(quant_model)
        input_quantizer = None
    
        if first_params is not None:
            input_quantizer = InputQuantizer(first_params[0], first_params[1], qmin=config.qmin, qmax=config.qmax)

        onnx_path = os.path.join(self.save_path, 'wavlm_mtsq.onnx')
        export_success = export_mtsq_to_onnx(quant_model, test_input[:1], onnx_path, input_quantizer)

        if not export_success:
            print("ONNX export failed – aborting")
            return
        else:
            print("ONNX export Successfull")

        
    def evaluate(self):
        self.quantize()
        
        
    def get_config(self):
        """Return configuration."""
        return {'config': self.config}
