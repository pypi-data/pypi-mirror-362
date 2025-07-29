from datetime import datetime
from functools import reduce
from typing import Dict, Unpack

import numpy as np
import pandas as pd

from finter.backtest.base.main import BaseBacktestor
from finter.backtest.config.simulator import SimulatorInputConfig
from finter.backtest.config.templates import AVAILABLE_MARKETS
from finter.backtest.simulator import Simulator


class MultiMarketSimulator:
    """
    multi market simulator
    """

    # No more caching needed - individual Simulators are cached

    def __init__(
        self,
        start: int = 20000101,
        end: int = int(datetime.now().strftime("%Y%m%d")),
        *,
        market_types: list[AVAILABLE_MARKETS],
    ):
        self.start = start
        self.end = end
        self.market_types = sorted(market_types)  # Sort for consistent behavior

        self.union_index: list = []

        self.simulators: Dict[str, Simulator] = {}
        self.positions: Dict[str, pd.DataFrame] = {}
        self.configs: Dict[str, SimulatorInputConfig] = {}
        self.backtestors: Dict[str, BaseBacktestor] = {}

        self.results: dict[str, np.ndarray] = {}

        for market_type in market_types:
            # Use cached Simulator instances
            simulator = Simulator.get_cached_instance(
                market_type=market_type,
                start=self.start,
                end=self.end,
            )
            self.simulators[market_type] = simulator
            self.configs[market_type] = {}

            simulator.builder.data.price.columns

    def seperate_positions(self, position: pd.DataFrame):
        position_columns = set(position.columns)
        for market_type in self.market_types:
            self.positions[market_type] = position.reindex(
                columns=self.simulators[market_type].builder.data.price.columns
            )
            position_columns -= set(self.positions[market_type].columns)

        assert len(position_columns) == 0, f"Unmatched columns: {position_columns}"
        return self

    def update_market_config(
        self,
        market_type: AVAILABLE_MARKETS,
        **kwargs: Unpack[SimulatorInputConfig],
    ):
        assert set(kwargs.keys()) <= set(SimulatorInputConfig.__annotations__.keys()), (
            f"Invalid keys: {set(kwargs.keys()) - set(SimulatorInputConfig.__annotations__.keys())}\n"
            f"Available keys: {SimulatorInputConfig.__annotations__.keys()}"
        )

        self.configs[market_type] = kwargs

        return self

    def build(self):
        price_indices = [
            simulator.builder.data.price.index for simulator in self.simulators.values()
        ]
        max_price_start = max(idx[0] for idx in price_indices)
        min_price_end = min(idx[-1] for idx in price_indices)

        position_indices = [position.index for position in self.positions.values()]
        min_position_start = max(idx[0] for idx in position_indices)
        min_position_end = min(idx[-1] for idx in position_indices)

        max_start = max(max_price_start, min_position_start)
        min_end = min(min_price_end, min_position_end)

        all_indices = pd.DatetimeIndex(
            sorted(reduce(lambda x, y: x.union(y), price_indices))
        )
        all_indices = all_indices[all_indices.slice_indexer(max_start, min_end)]

        for market_type, simulator in self.simulators.items():
            simulator.builder.update(
                price=simulator.builder.data.price.fillna(0)
                .reindex(all_indices)
                .ffill()
                .replace(0, np.nan)
                .fillna(0),
            )
            self.backtestors[market_type] = simulator.build(
                position=self.positions[market_type]
                .fillna(np.inf)
                .reindex(all_indices)
                .ffill()
                .replace(np.inf, np.nan)
                .fillna(0),
                **self.configs[market_type],
            )
        common_indexes = {
            market_type: backtestor.frame.common_index
            for market_type, backtestor in self.backtestors.items()
        }
        self.union_index = sorted(common_indexes.values())[0]

        assert len(set([len(c) for c in list(common_indexes.values())])), (
            "All backtestors must have the same number of rows"
        )
        assert not self.union_index == 0, "Union index is 0"
        self.results["cash"] = np.full(
            (len(self.union_index), 1), np.nan, dtype=np.float64
        )

        # Create market_type to index mapping
        self.market_order = {
            market_type: idx for idx, market_type in enumerate(self.backtestors.keys())
        }

    def run(self, position: pd.DataFrame):
        self.seperate_positions(position)
        self.build()

        # 환율맞추기, 오더링

        total_cash = sum(
            backtestor.vars.result.cash[0, 0]
            for backtestor in self.backtestors.values()
        )

        self.results["cash"][0, 0] = total_cash

        for i in range(1, len(self.union_index)):
            total_weight = sum(
                backtestor.vars.input.weight[i].sum()
                for backtestor in self.backtestors.values()
            )
            total_aum = (
                sum(
                    backtestor.vars.result.aum[i - 1]
                    for backtestor in self.backtestors.values()
                )
                + total_cash
            )

            for market_type, backtestor in self.backtestors.items():
                target_aum = total_aum * (
                    backtestor.vars.input.weight[i].sum() / total_weight
                )

                backtestor.vars.result.cash[i - 1] = total_cash
                backtestor.vars.result.aum[i - 1] = target_aum

                backtestor.run_step(i)

                total_cash = backtestor.vars.result.cash[i, 0]

                backtestor.vars.result.cash[i] = 0
                backtestor.vars.result.aum[i] -= total_cash

            self.results["cash"][i, 0] = total_cash

        for backtestor in self.backtestors.values():
            if not backtestor.optional.debug:
                backtestor._clear_all_variables(clear_attrs=True)
            else:
                backtestor._clear_all_variables(clear_attrs=False)

        sorted_backtestors = sorted(
            self.backtestors.items(), key=lambda x: self.market_order[x[0]]
        )

        # 데이터 추출 및 병합
        markets, backtestors = zip(*sorted_backtestors)
        backtestors = list(backtestors)

        # DataFrame 생성
        result = pd.concat(
            [
                *[bt.summary.valuation for bt in backtestors],
                *[bt.summary.cost for bt in backtestors],
                *[bt.summary.slippage for bt in backtestors],
                pd.DataFrame(self.results["cash"], index=self.union_index),
            ],
            axis=1,
        )

        # 컬럼 설정 및 계산
        val_cols = [f"{m}_valuation" for m in markets]
        cost_cols = [f"{m}_cost" for m in markets]
        slippage_cols = [f"{m}_slippage" for m in markets]

        result.columns = val_cols + cost_cols + slippage_cols + ["cash"]
        result["valuation"] = result[val_cols].sum(axis=1)
        result["cost"] = result[cost_cols].sum(axis=1)
        result["slippage"] = result[slippage_cols].sum(axis=1)

        result["aum"] = result["valuation"] + result["cash"]
        result["nav"] = (result["aum"] / result["aum"].iloc[0]) * 1000

        # 최종 정렬
        return result[
            ["nav", "aum", "cash", "valuation", "cost", "slippage"]
            + val_cols
            + cost_cols
            + slippage_cols
        ]
