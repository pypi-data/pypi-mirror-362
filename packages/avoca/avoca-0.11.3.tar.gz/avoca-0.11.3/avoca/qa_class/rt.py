"""Quality assurance for retention times."""

from __future__ import annotations

import numpy as np
import pandas as pd

from avoca.flags import QA_Flag
from avoca.logging import SUSPISCIOUS
from avoca.qa_class.abstract import AbstractQA_Assigner


class RetentionTimeChecker(AbstractQA_Assigner):
    """Tries to check if there is a problem with the assignment of the retention times.

    The very simple way of doing, it to check the correlation between the
    retention times of the measurements.
    The correlation is usually very high. If one compound has a low correlation
    with the others, it probably means that is was miss-assigned at some points.
    """

    runtypes: list[str] = ["air", "std"]
    flag = QA_Flag.SUSPICIOUS_RT

    RT_THRESHOLD: float = 2.0

    rt_ref: pd.Series

    def fit(self, df: pd.DataFrame):
        cols = [(compound, "rt") for compound in self.compounds]

        df_rt: pd.DataFrame = df[cols]
        self.df_train = df_rt
        df_corr = df_rt.corr()
        self.corr = df_corr.mean()
        mean_corr = self.corr.mean()
        std_corr = self.corr.std()

        deviation = np.abs(self.corr - mean_corr)
        threshold = 2 * std_corr
        self.logger.debug(f"{deviation=}, {threshold=}")

        possibly_wrong = deviation > threshold
        self.possibly_wrong = possibly_wrong[possibly_wrong].index.tolist()
        if len(self.possibly_wrong) > 0:
            self.logger.log(
                SUSPISCIOUS, f"Possibe RT assignement issue: {self.possibly_wrong=}"
            )

        # Get a dataframe for a mean reference
        self.rt_ref = df_rt.median(axis="index")

    def assign(self, df: pd.DataFrame) -> dict[str, pd.Index]:
        """Assing flags when expected rt values does not match the measured ones."""
        rt_cols: list[tuple[str, str]] = [
            (compound, "rt") for compound in self.compounds
        ]
        df_rt = df[rt_cols]
        # Take the reference retention times
        x = self.rt_ref.loc[rt_cols].to_numpy()

        outliers = {}

        for t, row in df_rt.iterrows():
            # Make a lin reg line
            y = row.to_numpy()
            mask_not_nan = ~np.isnan(y)
            if np.sum(mask_not_nan) < 3:
                self.logger.warning(
                    f"{self} skipping {t} because there are not enough compounds"
                    " measured"
                )
                continue

            params = np.polyfit(x[mask_not_nan], y[mask_not_nan], 1)
            f = np.poly1d(params)
            y_lin_reg = f(x)

            # Get the points which are too far from the reg line
            mask_bad = np.abs(y - y_lin_reg) > self.RT_THRESHOLD
            if np.any(mask_bad):
                outliers[t] = mask_bad

        # Create a dataframe with the flags
        out_dict = {}
        df_outliers = pd.DataFrame(outliers, index=self.compounds).T

        for compound in self.compounds:
            col = df_outliers[compound]
            out_dict[compound] = col.loc[col].index

        return out_dict

    def plot(self):

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        assigned = self.assign(self.df_train)

        for compound in self.compounds:
            ax.scatter(
                self.df_train.index,
                self.df_train[(compound, "rt")],
                label=compound,
                marker="+",
            )
            df_flagged = self.df_train.loc[assigned[compound]]
            if len(df_flagged) > 0:
                ax.scatter(
                    df_flagged.index,
                    df_flagged[(compound, "rt")],
                    # label=f"{compound} flagged",
                    color="red",
                    marker="x",
                )

        ax.legend()
        plt.show()
