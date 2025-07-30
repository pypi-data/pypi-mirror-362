import numpy as np
import onnxruntime as ort
from onnx import ModelProto
import time

def measure_inference_time(model: ModelProto, input_data: dict[str, np.ndarray], nb_warmup: int = 10, nb_iterations: int = 50) -> list[float]:
    """
    Run the provided ONNX model using ONNXRuntime.
    Performs 10 warm-up runs followed by 50 timed runs (using CPU process time).

    Args:
        model: The ONNX model (ModelProto).
        input_data: Dictionary mapping all input names to NumPy arrays.

    Returns:
        List of CPU times (in seconds) for the 50 timed runs.
    """
    sess_opt = ort.SessionOptions()
    sess_opt.intra_op_num_threads = 1
    sess = ort.InferenceSession(model.SerializeToString(), sess_opt)

    timings = []
    # Warm-up runs.
    for i in range(nb_warmup + nb_iterations):
        if i < nb_warmup:
            sess.run(None, input_data)
        else:
            start = time.process_time()
            sess.run(None, input_data)
            end = time.process_time()
            timings.append((end - start))
    return timings

def compute_output(model: ModelProto, input_data: dict[str, np.ndarray]) -> list[np.ndarray]:
    sess = ort.InferenceSession(model.SerializeToString())
    # Run the session with the provided input_data.
    outputs = sess.run(None, input_data)
    # Return all outputs.
    return np.array(outputs)