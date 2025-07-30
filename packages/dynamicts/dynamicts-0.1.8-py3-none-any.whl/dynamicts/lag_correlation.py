"""
lag_correlation.py

This module provides the Correlation class for analyzing and visualizing autocorrelation (ACF)
and partial autocorrelation (PACF) in time series data. It supports logging results and plots to HTML reports.
"""

import pandas as pd
from datetime import datetime
import os
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from dynamicts.report_generator import log_plot_to_html_report, log_message_to_html_report
from dynamicts.data_loader import DataLoader

class Correlation:
    """
    A class for computing and visualizing autocorrelation and partial autocorrelation
    for time series data.
    """
    def __init__(self, df: pd.DataFrame = None, target_col: str = None, lags: int = 20):
        """
        Initialize the Correlation class.

        Args:
            df (pd.DataFrame, optional): DataFrame containing the time series data.
            target_col (str, optional): Name of the column to analyze.
            lags (int, optional): Number of lags to use for correlation plots.

        Raises:
            TypeError: If df is not a pandas DataFrame.
            ValueError: If target_col is not provided or not found in df.
        """
        self.df = df
        self.target_col = target_col
        self.lags = lags
        self.date_col = None  # will be set if df is valid

        # If df is provided, validate it
        if self.df is not None:
            if not isinstance(self.df, pd.DataFrame):
                raise TypeError("Expected a pandas DataFrame for `df`.")

            # Save date_col if index name is present
            self.date_col = self.df.index.name or "index"

            # If target_col is missing
            if not self.target_col:
                raise ValueError("`target_col` must be provided when passing a DataFrame.")

            # Validate column name case-insensitively
            column_map = {col.lower(): col for col in self.df.columns}
            target_col_lower = self.target_col.lower()

            if target_col_lower not in column_map:
                raise ValueError(
                    f"Target column '{self.target_col}' not found in DataFrame. "
                    f"Available columns: {self.df.columns.tolist()}"
                )

            self.target_col = column_map[target_col_lower]
        # Generate report path ONCE per instance
        root_dir = os.path.abspath(os.curdir)
        report_root = os.path.join(root_dir, "reports")
        os.makedirs(report_root, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"correlation_report_{timestamp}.html"
        self.report_path = os.path.join(report_root, report_name)
        

    def acf_plot(self, data: pd.Series = None, lags: int = None, save: bool = True):
        """
        Plot the autocorrelation function (ACF) for the given time series.

        Args:
            data (pd.Series, optional): Time series data to analyze. If None, uses initialized data.
            lags (int, optional): Number of lags to plot. Defaults to instance lags.
            save (bool, optional): Whether to save the plot to an HTML report.

        Returns:
            matplotlib.figure.Figure: The generated ACF plot.

        Raises:
            ValueError: If no data is provided.
        """
        series = data if data is not None else self.df[self.target_col]

        if series is None:
            raise ValueError("No data provided for ACF plot. Pass `data` or instantiate with DataFrame and target_col.")

        lags = lags if lags is not None else self.lags
        title = f"Auto correlation Plot, lags = {lags}"

        fig, ax = plt.subplots(figsize = (14, 8))
        plot_acf(series, lags=lags, ax=ax)
        ax.set_title(title)

        if save:
            log_plot_to_html_report(fig=fig, title=title, report_path=self.report_path)
        
        return fig
    

    def pacf_plot(self, data: pd.Series = None, lags: int = None, save: bool = True):
        """
        Plot the partial autocorrelation function (PACF) for the given time series.

        Args:
            data (pd.Series, optional): Time series data to analyze. If None, uses initialized data.
            lags (int, optional): Number of lags to plot. Defaults to instance lags.
            save (bool, optional): Whether to save the plot to an HTML report.

        Returns:
            matplotlib.figure.Figure: The generated PACF plot.

        Raises:
            ValueError: If no data is provided.
        """
        series = data if data is not None else self.df[self.target_col]

        if series is None:
            raise ValueError("No data provided for PACF plot. Pass `data` or instantiate with DataFrame and target_col.")
        lags = lags if lags is not None else self.lags
        title = f"Partial Autocorrelation Plot (lags={lags})"

        fig, ax = plt.subplots(figsize = (12, 6))
        plot_pacf(series, lags=lags, ax=ax)    
        ax.set_title(title)

        if save:
            log_plot_to_html_report(fig=fig, title=title, report_path=self.report_path)

        return fig
    def run_lag_correlation(self, data: pd.Series = None, lags: int = None):
        """
        Run both ACF and PACF plots and log them to the report.

        Args:
            data (pd.Series, optional): Time series data to analyze. If None, uses initialized data.
            lags (int, optional): Number of lags to plot. Defaults to instance lags.

        Returns:
            dict: Dictionary with ACF and PACF figures.
        """
        acf_fig = self.acf_plot(data=data, lags=lags, save=True)
        pacf_fig = self.pacf_plot(data=data, lags=lags, save=True)
        return {
            "acf_fig": acf_fig,
            "pacf_fig": pacf_fig
        }
    
if __name__ == "__main__":
    # Load the data
    loader = DataLoader(filepath="data/complaints.csv", index_col="date")
    df = loader.run_pipeline()

    if df is not None:
        # ✅ Option 1: Instance-based usage (uses internal config)
        print("Using instance-based plotting...")
        corr_instance = Correlation(df=df, target_col="complaints", lags=30)
        corr_instance.acf_plot()
        corr_instance.pacf_plot()

        # ✅ Option 2: Standalone-style usage (no target_col needed, just a Series)
        print("Using standalone-style plotting...")
        corr_flex = Correlation()  # No args needed
        # corr_flex.acf_plot(data=df["revenue"], lags=30)
        # corr_flex.pacf_plot(data=df["revenue"], lags