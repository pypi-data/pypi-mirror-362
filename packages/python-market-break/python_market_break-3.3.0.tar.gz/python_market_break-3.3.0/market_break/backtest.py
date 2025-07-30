# backtest.py

from typing import Sequence, Iterable
import datetime as dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from market_break.labels import (
    ENTRY, EXIT, LONG, SHORT, TYPE, RETURNS
)

__all__ = [
    "Report",
    "Trades",
    "Plot"
]


type TradesDF = pd.DataFrame
type Returns = pd.Series


class Trades:

    EMPTY = -1

    @staticmethod
    def adjust(trades: TradesDF) -> TradesDF:
        trades = trades[trades[EXIT] != Trades.EMPTY]
        trades = trades[trades[ENTRY] != Trades.EMPTY]

        return trades

    @staticmethod
    def generate_raw(
        up: Sequence[bool] | bool,
        down: Sequence[bool] | bool,
        index: Iterable = None,
    ) -> TradesDF:
        if len(up) != len(down):
            raise ValueError(
                'up and down must have the same length, '
                f'but {len(up)} and {len(down)} where given.'
            )

        if index is None:
            index = np.array(list(range(len(up))))

        entries = np.array([-1] * len(index)).astype(int)
        exits = np.array([-1] * len(index)).astype(int)
        types = np.array([""] * len(index)).astype(str)

        entries[up] = index[up]
        entries[down] = index[down]
        types[up] = LONG
        types[down] = SHORT

        last = None

        for i, entry in enumerate(entries):
            if last is None:
                last = types[i]

            elif last != types[i]:
                exits[i] = index[i]

        return pd.DataFrame(
            {ENTRY: entries, EXIT: exits, TYPE: types}
        )

    @staticmethod
    def generate(
        up: Sequence[bool] | bool,
        down: Sequence[bool] | bool,
        index: Iterable = None,
        adjust: bool = False,
        raw: bool = False
    ) -> TradesDF:
        if raw:
            if adjust:
                raise ValueError(
                    "Cannot adjust when asked to generate raw trades, "
                    "which are not necessarily aligned."
                )

            return Trades.generate_raw(up=up, down=down, index=index)

        if len(up) != len(down):
            raise ValueError(
                'up and down must have the same length, '
                f'but {len(up)} and {len(down)} where given.'
            )

        long = short = first_long = first_short = Trades.EMPTY
        long_count = short_count = 0

        data: list[tuple[int, int, str]] = []

        if index is None:
            index = range(len(up))

        for i in index:
            long_signal = up[i]
            short_signal = down[i]

            if long_count == short_count == 0:
                add_long = long_signal
                add_short = (not add_long) and short_signal

            elif long_count == short_count:
                add_long = (first_long < first_short) and long_signal
                add_short = (not add_long) and ((first_long > first_short) and short_signal)

            elif (long_count > 0) and (short_count > 0):
                add_long = (long < short) and long_signal
                add_short = (not add_long) and ((long > short) and short_signal)

            else:
                add_long = (long_count < short_count) and long_signal
                add_short = (not add_long) and ((long_count > short_count) and short_signal)

            if (first_long == Trades.EMPTY) and (long != Trades.EMPTY):
                first_long = long

            elif (first_short == Trades.EMPTY) and (short != Trades.EMPTY):
                first_short = short

            if add_long:
                long = i
                long_count += 1
                data.append((short, long, SHORT))

            elif add_short:
                short = i
                short_count += 1
                data.append((long, short, LONG))

        if data and (data[-1][1] != Trades.EMPTY):
            data.append((data[-1][1], Trades.EMPTY, LONG if data[-1][2] == SHORT else SHORT))

        arr_data = np.array(data)
        trades = pd.DataFrame(
            {
                ENTRY: (arr_data[:, 0] if data else np.array([])).astype(int),
                EXIT: (arr_data[:, 1] if data else np.array([])).astype(int),
                TYPE: (arr_data[:, 2] if data else np.array([])).astype(str)
            }
        )

        if adjust:
            trades = Trades.adjust(trades)

        return trades

    @staticmethod
    def limit(
        trades: TradesDF,
        bid: Sequence[float],
        ask: Sequence[float],
        take: float | Sequence[float] = None,
        stop: float | Sequence[float] = None,
        decay: float | Sequence[float] = None,
        dynamic: bool = False
    ) -> TradesDF:
        if len(bid) != len(ask):
            raise ValueError(
                'bid and ask must have the same length, '
                f'but {len(bid)} and {len(ask)} where given.'
            )

        if isinstance(bid, pd.Series):
            bid = bid.values

        if isinstance(ask, pd.Series):
            ask = ask.values

        trades = trades.copy()

        if (stop is None) and (take is None):
            return trades

        constant_take = isinstance(take, (int, float, np.integer, np.floating))
        constant_stop = isinstance(stop, (int, float, np.integer, np.floating))
        constant_decay = isinstance(decay, (int, float, np.floating))

        if constant_decay and not (0 < decay <= 1):
            raise ValueError("Decay must be between 0 and 1.")

        for i, row in trades.iterrows():
            # noinspection PyTypeChecker
            start: int = row[ENTRY]
            # noinspection PyTypeChecker
            limit: int = row[EXIT]

            max_returns = 1
            current_decay = 1

            for end in range(start + 1, limit):
                if row[TYPE] == LONG:
                    current_returns = bid[end] / ask[start]

                elif row[TYPE] == SHORT:
                    current_returns = bid[start] / ask[end]

                else:
                    continue

                current_decay *= (
                    (decay if constant_decay else decay[end])
                    if decay is not None else 1
                )
                current_stop = (
                    (stop if constant_stop else stop[end])
                    if stop is not None else current_returns
                )
                current_take = (
                    (take if constant_take else take[end])
                    if take is not None else current_returns
                )

                current_stop = 1 - (1 - current_stop) * current_decay

                if not (current_stop < current_returns < current_take):
                    trades.loc[i, EXIT] = end

                    break

                elif dynamic and (current_returns > max_returns):
                    max_returns = current_returns
                    start = end

        return trades

    @staticmethod
    def returns(
        trades: TradesDF,
        bid: Sequence[float],
        ask: Sequence[float],
        fee: float | Sequence[float] = 0.0
    ) -> Returns:
        if len(bid) != len(ask):
            raise ValueError(
                'bid and ask must have the same length, '
                f'but {len(bid)} and {len(ask)} where given.'
            )

        if not isinstance(ask, np.ndarray):
            ask = np.array(ask)

        if not isinstance(bid, np.ndarray):
            bid = np.array(bid)

        if not isinstance(fee, (float, np.integer, np.floating)):
            fee = np.array(fee)

        trades = Trades.adjust(trades)
        flip_short = trades[TYPE] == SHORT
        returns = bid[trades[EXIT]] / ask[trades[ENTRY]]
        returns[flip_short] = (
                bid[trades[ENTRY]][flip_short] /
                ask[trades[EXIT]][flip_short]
        )
        returns = (returns - 1) * (1 - fee)

        return pd.Series(returns, index=trades[EXIT], name=RETURNS)


type Index = int | float | pd.Timestamp | dt.datetime | dt.date


class Report:

    @staticmethod
    def generate[I: Index](
        index: Sequence[I],
        returns: Sequence[float],
        long: Sequence[int],
        short: Sequence[int],
        balance: Sequence[float] = None
    ) -> dict[str, dict[str, float | I]]:
        if not isinstance(index, pd.Series):
            index = pd.Series(index)

        if not isinstance(returns, np.ndarray):
            returns = np.array(returns)

        if balance is None:
            balance = np.cumsum(returns)

        if not isinstance(balance, np.ndarray):
            balance = np.array(balance)

        tick_time = (index.iloc[1:] - index.values[:-1])
        mean_tick_time = tick_time.mean()
        min_tick_time = tick_time.min()
        max_tick_time = tick_time.max()
        tuw = (index.iloc[short] - index.iloc[long].values)
        mean_tuw = tuw.mean()
        max_tuw = tuw.max()
        min_tuw = tuw.min()

        gains = returns[returns > 0]
        losses = returns[returns < 0]

        gain_sum = (gains.sum() if len(gains) > 0 else np.nan)
        loss_sum = (losses.sum() if len(losses) > 0 else np.nan)

        return {
            'index': {
                'start': index.iloc[0] if len(index) > 0 else None,
                'end': index.iloc[-1] if len(index) > 0 else None,
                'total duration': index.iloc[-1] - index.iloc[0] if len(index) > 0 else None,
                'min. tick duration': (
                    min_tick_time.to_pytimedelta()
                    if isinstance(min_tick_time, pd.Timedelta) else
                    min_tick_time
                ),
                'max. tick duration': (
                    max_tick_time.to_pytimedelta()
                    if isinstance(max_tick_time, pd.Timedelta) else
                    max_tick_time
                ),
                'avg. tick duration': (
                    mean_tick_time.to_pytimedelta()
                    if isinstance(mean_tick_time, pd.Timedelta) else
                    mean_tick_time
                ),
                'ticks': len(index)
            },
            'trades': {
                'long trades': len(long),
                'short trades': len(short),
                'min. TUW': (
                    min_tuw.to_pytimedelta()
                    if isinstance(min_tuw, pd.Timedelta) else
                    min_tuw
                ),
                'max. TUW': (
                    max_tuw.to_pytimedelta()
                    if isinstance(max_tuw, pd.Timedelta) else
                    max_tuw
                ),
                'avg. TUW': (
                    mean_tuw.to_pytimedelta()
                    if isinstance(mean_tuw, pd.Timedelta) else
                    mean_tuw
                )
            },
            'gains': {
                '[%] min. gain': (gains.min() if len(gains) > 0 else np.nan) * 100,
                '[%] max. gain': (gains.max() if len(gains) > 0 else np.nan) * 100,
                '[%] avg. gain': (gains.mean() if len(gains) > 0 else np.nan) * 100,
                '[%] total gains': gain_sum * 100,
                'winning trades': len(gains)
            },
            'losses': {
                '[%] min. loss': (losses.max() if len(losses) > 0 else np.nan) * 100,
                '[%] max. loss': (losses.min() if len(losses) > 0 else np.nan) * 100,
                '[%] avg. loss': (losses.mean() if len(losses) > 0 else np.nan) * 100,
                '[%] total losses': loss_sum * 100,
                'losing trades': len(losses)
            },
            'performance': {
                'PnL factor': (gain_sum / -loss_sum),
                'avg. profit factor': (1 + returns.mean() if len(returns) > 0 else np.nan),
                '[%] win rate': (len(gains) / len(returns)) * 100 if len(returns) > 0 else np.nan,
                '[%] total profit': (balance[-1] if len(balance) > 0 else 0.0) * 100
            }
        }

    @staticmethod
    def repr[I: Index](
        data: dict[str, dict[str, float | I]],
        padding: int = 23,
        precision: int = 4
    ) -> str:
        output = []

        for title, values in data.items():
            output.append(f"{'\n' if output else ''}[{title.title()}]")

            for key, value in values.items():
                if isinstance(value, (int, float, np.number)):
                    value = round(value, precision)

                elif isinstance(value, (dt.datetime, dt.timedelta, pd.Timedelta, pd.Timestamp)):
                    value = str(value)[:-4]

                output.append(f"{key:<{padding}}{value:>{padding}}")

        return "\n".join(output)


class Plot:

    plt.style.use('fivethirtyeight')

    @staticmethod
    def style(style: str) -> None:
        plt.style.use(style)

    @staticmethod
    def returns_histogram(returns: pd.Series, bins: int | None = 50) -> None:
        returns_pct = returns * 100

        gains_pct = returns_pct[returns_pct > 0]
        losses_pct = returns_pct[returns_pct < 0]

        returns_pct_average = returns_pct.mean()
        gains_pct_average = gains_pct.mean()
        losses_pct_average = losses_pct.mean()

        curve = None
        x = None

        if bins:
            try:
                y, x = np.histogram(returns_pct, bins=bins)
                y = np.concatenate([y, np.array([0])])

                with np.testing.suppress_warnings() as sup:
                    sup.filter(np.exceptions.RankWarning)

                    curve = np.poly1d(np.polyfit(x, y, min(len(x), 7)))(x)

            except (np.linalg.LinAlgError, TypeError):
                pass

        plt.figure(figsize=(14, 4))
        plt.title('Transaction Returns Histogram')
        plt.xlabel('Returns (%)')
        plt.ylabel('Count')
        plt.axvline(0, color='blue', label='zero', lw=1.5, linestyle='dashed')
        plt.axvline(
            returns_pct_average, color='orange',
            label=f'mean return {returns_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axvline(
            gains_pct_average, color='green',
            label=f'mean gain {gains_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axvline(
            losses_pct_average, color='red',
            label=f'mean loss {losses_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.hist(returns_pct, bins=bins, alpha=0.85, label=f'returns ({bins} bins)')

        if curve is not None:
            plt.plot(x, curve, alpha=1, lw=2.5, c="cyan")

        plt.legend()
        plt.show()

    @staticmethod
    def returns_signals(
        returns: pd.Series,
        index: np.ndarray | pd.Series = None,
        curve: bool = True
    ) -> None:

        returns_pct = returns * 100

        if index is None:
            index = returns.index

        gains_pct = returns_pct[returns_pct > 0]
        losses_pct = returns_pct[returns_pct < 0]

        returns_pct_average = returns_pct.mean()
        gains_pct_average = gains_pct.mean()
        losses_pct_average = losses_pct.mean()

        curve_data = None

        if curve:
            try:
                x = np.array(list(range(len(returns_pct))))

                with np.testing.suppress_warnings() as sup:
                    sup.filter(np.exceptions.RankWarning)

                    curve_data = np.poly1d(np.polyfit(x, returns_pct, min(len(x), 7)))(x)

            except (np.linalg.LinAlgError, TypeError):
                pass

        plt.figure(figsize=(14, 4))
        plt.title('Transaction Returns')
        plt.xlabel('Date-Time')
        plt.ylabel('Returns (%)')
        plt.scatter(
            index[gains_pct.index], gains_pct,
            c='green', s=15, alpha=0.875
        )
        plt.scatter(
            index[losses_pct.index], losses_pct,
            c='red', s=15, alpha=0.875
        )
        plt.plot(
            index[returns_pct.index], returns_pct,
            lw=1.5, label='returns', alpha=0.85
        )
        plt.axhline(
            returns_pct_average, color='orange',
            label=f'mean {returns_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axhline(
            gains_pct_average, color='green',
            label=f'mean gain {gains_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axhline(
            losses_pct_average, color='red',
            label=f'mean loss {losses_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axhline(0, color='blue', label=f'zero', lw=1.5, linestyle='dashed')

        if curve_data is not None:
            plt.plot(index[returns.index], curve_data, alpha=1, lw=2.5, c="cyan")

        plt.legend()
        plt.show()

    @staticmethod
    def returns_pie(returns: pd.Series) -> None:
        # noinspection PyUnresolvedReferences
        returns_counts = (returns > 0).value_counts()
        values = [returns[returns > 0].sum(), -1 * returns[returns < 0].sum()]

        wins = returns_counts.get(True, 0)
        losses = returns_counts.get(False, 0)
        returns_sizes = pd.Series(values) * 100

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        fig.suptitle('Transaction Returns')
        ax1.pie([wins, losses], startangle=90, autopct='%1.2f%%')
        ax1.legend(labels=[f'Wins {wins}', f'Losses {losses}'])
        ax2.pie(returns_sizes[returns_sizes != 0.0], startangle=90, autopct='%1.2f%%')
        ax2.legend(
            labels=[
                *([f'Gains {returns_sizes[0]:.3f}%'] if returns_sizes[0] > 0 else []),
                *([f'Losses {returns_sizes[1]:.3f}%'] if returns_sizes[1] > 0 else [])
            ]
        )
        plt.show()

    @staticmethod
    def returns_balance(returns: pd.Series, index: np.ndarray | pd.Series = None) -> None:

        returns = returns.copy() * 100

        if index is None:
            index = returns.index

        returns_pct = pd.Series(
            np.concatenate([np.array([0]), returns.values]),
            index=[0] + list(returns.index)
        )

        gains_pct = returns_pct[returns_pct >= 0]
        losses_pct = returns_pct[returns_pct <= 0]

        balance_pct = returns_pct.cumsum()
        total_gains_pct = gains_pct.cumsum()
        total_losses_pct = losses_pct.cumsum()

        plt.figure(figsize=(14, 4))
        plt.title('Transaction Balance')
        plt.xlabel('Date-Time')
        plt.ylabel('Returns (%)')
        plt.plot(
            index[balance_pct.index], balance_pct,
            lw=4, label=(
                f'cumulative returns '
                f'{balance_pct.iloc[-1] if len(balance_pct) > 0 else 0.0:.3f}%'
            )
        )
        plt.plot(
            index[total_gains_pct.index], total_gains_pct,
            lw=2, c='green', linestyle='dashed',
            label=(
                f'cumulative gains '
                f'{total_gains_pct.iloc[-1] if len(total_gains_pct) > 0 else 0:.3f}%'
            )
        )
        plt.plot(
            index[total_losses_pct.index], -total_losses_pct,
            lw=2, c='red', linestyle='dashed',
            label=(
                f'cumulative losses '
                f'{-total_losses_pct.iloc[-1] if len(total_losses_pct) > 0 else 0:.3f}%'
            )
        )
        plt.axvline(index.values[-1], color='blue', label='now', lw=1.5)
        plt.legend()
        plt.show()

    @staticmethod
    def price_signals(
        bid: pd.Series,
        ask: pd.Series,
        long: Sequence[int] = None,
        short: Sequence[int] = None,
        index: np.ndarray | pd.Series = None
    ) -> None:

        if len(bid) != len(ask):
            raise ValueError(
                'bid and ask must have the same length, '
                f'but {len(bid)} and {len(ask)} where given.'
            )

        if index is None:
            index = bid.index

        mid = ask / 2 + bid / 2

        plt.figure(figsize=(14, 4))
        plt.title('Strategy Actions')
        plt.xlabel('Date-Time')
        plt.ylabel('Price')

        if (long is not None) and (short is not None):
            new_long = long[long != short]
            new_short = short[short != long]

            long = new_long
            short = new_short

        if long is not None:
            plt.scatter(
                index[long], ask[long],
                marker='^', color='green', s=35, label='long'
            )

        if short is not None:
            plt.scatter(
                index[short], bid[short],
                marker='v', color='red', s=35, label='short'
            )

        plt.plot(
            index[bid.index], bid, lw=1, alpha=0.875,
            label=f'bid {bid.iloc[-1] if len(bid) > 0 else np.nan:.5f}',
        )
        plt.plot(
            index[ask.index], ask, lw=1, alpha=0.875,
            label=f'ask {ask.iloc[-1] if len(ask) > 0 else np.nan:.5f}',
        )
        plt.plot(
            index[mid.index], mid, lw=0.75, alpha=0.75,
            label=f'mid {round(mid.iloc[-1], 5) if len(mid) > 0 else np.nan:.5f}'
        )

        plt.legend()
        plt.show()
