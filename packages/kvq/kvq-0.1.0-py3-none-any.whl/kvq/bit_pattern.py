from __future__ import annotations

import json
import warnings
from typing import Dict, List, Sequence

import importlib.resources as pkg_resources

from kvq.const import model_dict, supported_models, _SUPPORTED_BITS


RD_EXP: int = 2  # 2^(−RD_EXP·b)
TOL: float = 1e-6
ASSETS_PATH = "kvq.assets"


def _build_next_bit_dict(bits: Sequence[float]) -> Dict[float, float]:

    bits = sorted(bits)  # sorted if user passes unsorted bits
    return {bits[i]: bits[i + 1] for i in range(len(bits) - 1)}


def bit_pattern(
    model: str,
    budget=4,
    layers="all",
    bit_range=_SUPPORTED_BITS,
    score: int = 0,  # will be removed
):
    """
    Allocate bit-widths for every (W_k, W_v) matrix in *model*.

    Parameters
    ----------
    model : str
        HuggingFace repo name (must exist in kvq.const.model_dict).
    budget : int | float, default 4
        Average bits per matrix (total budget = 2 * layers * budget).
    layers : "all" | int, default "all"
        Currently only "all" layers are supported.
    bit_range : sequence of float, default _SUPPORTED_BITS
        Allowed quantisation bit-widths (need not be integers).
    score : {0, 1}, default 0 will be removed
        0: Frobenius norm file, 1: spectral norm file.

    Returns
    dict with keys
        "nbits_k": list[float] – per-layer bits for W_k
        "nbits_v": list[float] – per-layer bits for W_v
    """

    if model not in supported_models:
        raise ValueError(
            f"Model {model!r} is not supported. "
            f"Supported models: {', '.join(supported_models)}"
        )

    # TODO: more specific
    if budget > 8:
        raise ValueError("Budget should be less than or equal to 8 bits.")

    if layers != "all":
        raise NotImplementedError("Only layers='all' is currently supported.")

    model_name = model_dict.get(model)

    if model_name is None:
        raise ValueError(f"Model {model} not found in mapping. Please open an issue.")

    norm_type = "frobenius_norm" if score == 0 else "spectral_norm"
    score_file = f"{norm_type}/{model_name}.json"

    with pkg_resources.files(ASSETS_PATH).joinpath(score_file).open() as f:
        kv_norms = json.load(f)

    num_layers = len(kv_norms["w_k"])

    total_budget = 2 * budget * num_layers
    n_matrices = 2 * num_layers

    sens = []
    for k, v in zip(kv_norms["w_k"], kv_norms["w_v"]):
        sens.extend([k, v])

    c = [s**RD_EXP for s in sens]

    supported_bits = sorted(bit_range)
    next_bit_dict = _build_next_bit_dict(supported_bits)

    min_bits = supported_bits[0]
    current_bits = [min_bits] * n_matrices
    bits_used = n_matrices * min_bits

    while bits_used + TOL < total_budget:
        best_gain = -1.0
        cand_idx = None
        cand_next = None
        cand_delta = None

        for idx, (c_i, b_i) in enumerate(zip(c, current_bits)):
            # Is there a higher precision we can jump to?
            next_b = next_bit_dict.get(b_i)
            if next_b is None:
                continue

            delta_b = next_b - b_i
            if bits_used + delta_b - total_budget > TOL:
                continue

            cur_err = c_i * 2 ** (-RD_EXP * b_i)
            next_err = c_i * 2 ** (-RD_EXP * next_b)
            gain = (cur_err - next_err) / delta_b

            if gain > best_gain + TOL:
                best_gain, cand_idx = gain, idx
                cand_next, cand_delta = next_b, delta_b

        if cand_idx is None:
            break

        current_bits[cand_idx] = cand_next
        bits_used += cand_delta

    w_k_bits = current_bits[0::2]
    w_v_bits = current_bits[1::2]

    used = sum(w_k_bits) + sum(w_v_bits)
    if abs(used - total_budget) > TOL:
        warnings.warn(
            f"Total bits used = {used:.6f} differs from budget "
            f"{total_budget} by > {TOL}."
        )

    print(f"Total bits used: {used}, (Budget: {total_budget})")

    return {"nbits_k": w_k_bits, "nbits_v": w_v_bits}


if __name__ == "__main__":

    kv_bits = bit_pattern(
        model="meta-llama/Llama-3.2-1B-Instruct",
        budget=4,
        bit_range=(8, 6, 5, 4, 3, 2, 1.58, 1),
        score=1,
    )

    print("w_k bits:", kv_bits["nbits_k"])
    print("w_v bits:", kv_bits["nbits_v"])
