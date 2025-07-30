"""
volatility_check.py

This module provides the VolatilityChecker class for analyzing and visualizing time series volatility
using ARCH and GARCH models. It supports logging results and plots to HTML reports.
"""

import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from arch import arch_model
from dynamicts.report_generator import log_plot_to_html_report, log_message_to_html_report

class VolatilityChecker:
    """
    A class for checking and visualizing volatility in time series data using ARCH and GARCH models.
    """

    def __init__(self, df: pd.DataFrame = None, target_col: str = None):
        """
        Initialize the VolatilityChecker.

        Args:
            df (pd.DataFrame, optional): DataFrame containing the time series data.
            target_col (str, optional): Name of the column to analyze for volatility.

        Raises:
            TypeError: If df is not a pandas DataFrame.
            ValueError: If target_col is not provided or not found in df.
            RuntimeError: For any other initialization errors.
        """
        self.df = None
        self.series = None

        # Generate report path ONCE per instance
        root_dir = os.path.abspath(os.curdir)
        report_root = os.path.join(root_dir, "reports")
        os.makedirs(report_root, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"volatility_report_{timestamp}.html"
        self.report_path = os.path.join(report_root, report_name)

        try:
            if df is not None:
                if not isinstance(df, pd.DataFrame):
                    raise TypeError("Expected a pandas DataFrame for `df`.")

                if not target_col:
                    raise ValueError("`target_col` must be provided when passing a DataFrame.")

                column_map = {col.lower(): col for col in df.columns}
                target_col_lower = target_col.lower()

                if target_col_lower not in column_map:
                    raise ValueError(f"Column '{target_col}' not found. Available: {list(df.columns)}")

                self.df = df
                self.series = df[column_map[target_col_lower]].pct_change().dropna() * 100
        except Exception as e:
            raise RuntimeError(f"Initialization failed in VolatilityChecker: {str(e)}") from e

    def arch_volatility(self, data: pd.Series = None, save: bool = True):
        """
        Compute and plot volatility using an ARCH(1) model.

        Args:
            data (pd.Series, optional): Time series data to analyze. If None, uses initialized data.
            save (bool, optional): Whether to save the plot and summary to an HTML report.

        Returns:
            matplotlib.figure.Figure: The generated volatility plot.

        Raises:
            RuntimeError: If computation fails.
        """
        try:
            series = data.pct_change().dropna() * 100 if data is not None else self.series
            if series is None:
                raise ValueError("No time series data provided. Use `data=` or initialize the class with a DataFrame.")

            model = arch_model(series, vol="ARCH", p=1)
            res = model.fit(disp='off')
            cond_vol = res.conditional_volatility

            # Plot
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.plot(cond_vol, label="ARCH(1) Volatility", color='orange')
            ax.set_title("ARCH(1) Estimated Volatility")
            ax.set_ylabel("Volatility")
            ax.legend()

            if save:
                log_plot_to_html_report(fig, title="ARCH Volatility", report_path=self.report_path)

                message = f"""ARCH(1) Volatility Report:
                            - Mean: {cond_vol.mean():.4f}%
                            - Max: {cond_vol.max():.4f}%
                            - Min: {cond_vol.min():.4f}%
                            - Std Dev: {cond_vol.std():.4f}%
                            - Spikes (>1.5×mean): {(cond_vol > 1.5 * cond_vol.mean()).sum()}
                            """
                log_message_to_html_report(message, title="ARCH Volatility Summary", report_path=self.report_path)

            return fig

        except Exception as e:
            raise RuntimeError(f"ARCH volatility computation failed: {str(e)}") from e

    def garch_volatility(self, data: pd.Series = None, save: bool = True):
        """
        Compute and plot volatility using a GARCH(1,1) model.

        Args:
            data (pd.Series, optional): Time series data to analyze. If None, uses initialized data.
            save (bool, optional): Whether to save the plot and summary to an HTML report.

        Returns:
            matplotlib.figure.Figure: The generated volatility plot.

        Raises:
            RuntimeError: If computation fails.
        """
        try:
            series = data.pct_change().dropna() * 100 if data is not None else self.series
            if series is None:
                raise ValueError("No time series data provided. Use `data=` or initialize the class with a DataFrame.")

            model = arch_model(series, vol="GARCH", p=1, q=1)
            res = model.fit(disp='off')
            cond_vol = res.conditional_volatility

            # Plot
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.plot(cond_vol, label="GARCH(1,1) Volatility", color='purple')
            ax.set_title("GARCH(1,1) Estimated Volatility")
            ax.set_ylabel("Volatility")
            ax.legend()

            if save:
                log_plot_to_html_report(fig, title="GARCH Volatility", report_path=self.report_path)

                message = f"""GARCH(1,1) Volatility Report:
                            - Mean: {cond_vol.mean():.4f}%
                            - Max: {cond_vol.max():.4f}%
                            - Min: {cond_vol.min():.4f}%
                            - Std Dev: {cond_vol.std():.4f}%
                            - Spikes (>1.5×mean): {(cond_vol > 1.5 * cond_vol.mean()).sum()}
                            """
                log_message_to_html_report(message, title="GARCH Volatility Summary", report_path=self.report_path)

            return fig

        except Exception as e:
            raise RuntimeError(f"GARCH volatility computation failed: {str(e)}") from e
    def run_volatility_pipeline(self, data: pd.Series = None):
        """
        Run both ARCH and GARCH volatility analysis and log results to the report.

        Args:
            data (pd.Series, optional): Time series data to analyze. If None, uses initialized data.

        Returns:
            dict: Dictionary with ARCH and GARCH volatility figures.
        """
        print("="*60)
        print("**1. ARCH(1) Volatility Analysis**".center(60))
        print("="*60)
        arch_fig = self.arch_volatility(data=data, save=True)

        print("\n" + "="*60)
        print("**2. GARCH(1,1) Volatility Analysis**".center(60))
        print("="*60)
        garch_fig = self.garch_volatility(data=data, save=True)

        return {
            "arch_fig": arch_fig,
            "garch_fig": garch_fig
        }

if __name__ == "__main__":
    from dynamicts.data_loader import DataLoader

    loader = DataLoader(filepath="data/complaints.csv", index_col="date")
    df = loader.run_pipeline()

    # Option 1: Use instance-based approach
    vc = VolatilityChecker(df=df, target_col="complaints")
    vc.arch_volatility()
    vc.garch_volatility()

    # Option 2: Use flexible function-style
    vc2 = VolatilityChecker()
    # vc2.arch_volatility(data=df["revenue"])
    # vc2.garch_volatility(data=df["revenue"])