from typing import Optional, Tuple

import numpy as np
from numba import njit

from finter.backtest.config.config import AVAILABLE_REBALANCING_METHODS
from finter.backtest.core.constraint import (
    apply_target_volume_constraint,
    apply_turnover_volume_constraint,
)


@njit(cache=True)
def update_target_volume(
    weight: np.ndarray,
    prev_aum: float,
    weight_before: np.ndarray,
    target_volume_before: np.ndarray,
    is_first_day: bool,
    rebalancing_method: AVAILABLE_REBALANCING_METHODS,
    rebalancing_mask: int,
    target_volume_limit: Optional[np.ndarray],
    redistribute_max_iter: int,
    adjustment_ratio: np.ndarray,
    prev_adj_price: np.ndarray,
) -> np.ndarray:
    if is_first_day or rebalancing_method == "auto":
        target_volume = np.nan_to_num(weight * prev_aum / prev_adj_price)

    elif rebalancing_method == "by_position":
        # ISSUE
        if (np.abs(weight_before - weight) > 1e-10).any():
            target_volume = np.nan_to_num(weight * prev_aum / prev_adj_price)
        else:
            target_volume = target_volume_before

    elif rebalancing_method in ["W", "M", "Q"]:
        if rebalancing_mask:
            target_volume = np.nan_to_num(weight * prev_aum / prev_adj_price)
        else:
            target_volume = target_volume_before
    else:
        raise ValueError(f"Invalid rebalancing method: {rebalancing_method}")
    return (
        apply_target_volume_constraint(
            prev_adj_price,
            target_volume,
            target_volume_limit,
            weight,
            redistribute_max_iter,
        )
        * adjustment_ratio
    )


@njit(cache=True)
def calculate_target_buy_sell_volume(
    target_volume: np.ndarray,
    prev_actual_holding_volume: np.ndarray,
    weight: np.ndarray,
    volume_capacity: Optional[np.ndarray],
    volume_adjustment_ratio: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    target_buy_volume = np.maximum(
        target_volume - prev_actual_holding_volume * volume_adjustment_ratio, 0
    )
    target_sell_volume = np.maximum(
        prev_actual_holding_volume * volume_adjustment_ratio - target_volume, 0
    )

    if volume_capacity is not None:
        target_buy_volume = apply_turnover_volume_constraint(
            target_buy_volume, volume_capacity, weight
        )
        target_sell_volume = apply_turnover_volume_constraint(
            target_sell_volume, volume_capacity, weight
        )

    return target_buy_volume, target_sell_volume
