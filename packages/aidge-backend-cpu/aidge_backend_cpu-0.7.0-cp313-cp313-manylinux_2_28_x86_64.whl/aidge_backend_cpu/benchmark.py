import time

import numpy as np

import aidge_core

def prepare_model_scheduler_inputs(model: aidge_core.GraphView, input_data: list[str, np.ndarray]) -> tuple[aidge_core.GraphView, aidge_core.SequentialScheduler]:
    # update model and inputs backend
    model.set_backend("cpu")
    ordered_inputs = [aidge_core.Tensor(i[1]) for i in input_data]
    for ordered_input in ordered_inputs:
        ordered_input.set_backend("cpu")

    scheduler = aidge_core.SequentialScheduler(model)
    scheduler.generate_scheduling()

    return model, scheduler, ordered_inputs


def measure_inference_time(model: aidge_core.GraphView, input_data: list[str, np.ndarray], nb_warmup: int = 10, nb_iterations: int = 50) -> list[float]:
    model, scheduler, ordered_inputs = prepare_model_scheduler_inputs(model, input_data)

    timings = []
    # Warm-up runs.
    for i in range(nb_warmup + nb_iterations):
        if i < nb_warmup:
            scheduler.forward(forward_dims=False, data=ordered_inputs)
        else:
            start = time.process_time()
            scheduler.forward(forward_dims=False, data=ordered_inputs)
            end = time.process_time()
            timings.append((end - start))
    return timings

def compute_output(model: aidge_core.GraphView, input_data: list[str, np.ndarray]) -> list[np.ndarray]:
    model, scheduler, ordered_inputs = prepare_model_scheduler_inputs(model, input_data)

    scheduler.forward(forward_dims=False, data=ordered_inputs)

    return [np.array(t[0].get_operator().get_output(t[1])) for t in model.get_ordered_outputs()]