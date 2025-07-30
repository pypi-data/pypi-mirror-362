import torch
import numpy as np
from onnx import ModelProto
from onnx2torch import convert
import time

def measure_inference_time(model_onnx: ModelProto, input_data: dict[str, np.ndarray], nb_warmup: int = 10, nb_iterations: int = 50) -> list[float]:
    """
    Run the provided PyTorch model.
    Performs 10 warm-up runs followed by 50 timed runs (using CPU process time).

    Args:
        model_onnx: The ONNX model.
        input_data: Dictionary mapping all input names to NumPy arrays.

    Returns:
        List of CPU times (in seconds) for the 50 timed runs.
    """
    model = convert(model_onnx)

    device = torch.device("cpu")
    model.to(device)
    model.eval()

    torch.set_num_threads(1)

    inputs = [torch.tensor(v, device=device) for _, v in input_data.items()]
    timings = []
    with torch.no_grad():
        # Warm-up runs
        for i in range(nb_warmup + nb_iterations):
            if i < nb_warmup:
                model(*inputs)
            else:
                start = time.process_time()
                model(*inputs)
                end = time.process_time()
                timings.append(end - start)
    return timings

def compute_output(model_onnx: ModelProto, input_data: dict[str, np.ndarray]) -> list[np.ndarray]:
    """
    Run the PyTorch model inference.

    Args:
        model: The PyTorch model.
        input_data: Dictionary mapping all input names to NumPy arrays.

    Returns:
        The first output tensor if there is only one, else a list of output tensors.
    """
    model = convert(model_onnx)

    device = torch.device("cpu")
    model.to(device)
    model.eval()

    inputs = [torch.tensor(v, device=device) for _, v in input_data.items()]

    with torch.no_grad():
        # Warning: not tested for multiple outputs case
        output = model(*inputs)

    return output.numpy()
