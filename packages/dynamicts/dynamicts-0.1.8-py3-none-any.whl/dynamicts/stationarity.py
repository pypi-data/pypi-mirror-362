"""
stationarity.py
---------------
Provides tools for stationarity diagnostics and visualization for time series data,
including rolling statistics, Augmented Dickey-Fuller (ADF) and KPSS tests, and seasonal decomposition.

Functions:
    - rolling_statistics: Visualizes and logs rolling mean, std, and covariance.
    - adf_test: Performs the Augmented Dickey-Fuller test.
    - kpss_test: Performs the KPSS test.
    - print_adf_summary: Returns a Markdown summary of the ADF test.
    - plot_seasonal_decompose: Plots and logs seasonal decomposition.
    - stationarity_pipeline: Runs a full stationarity analysis pipeline.
"""

import os
from IPython.display import display, Markdown
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from dynamicts.report_generator import log_plot_to_html_report, log_message_to_html_report

class Stationaritychecker:
    def __init__(self, series: pd.Series, window: int = 7) -> None:
        """
        Initialize the Stationaritychecker with a time series and a window size.

        Args:
            series (pd.Series): The time series data.
            window (int): Window size for rolling calculations (default: 7).
        """
        self.series = series
        self.window = window

        # Generate report path ONCE per instance
        root_dir = os.path.abspath(os.curdir)
        report_root = os.path.join(root_dir, "reports")
        os.makedirs(report_root, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"stationarity_report_{timestamp}.html"
        self.report_path = os.path.join(report_root, report_name)

    def rolling_statistics(self, window=None) -> dict:
        """
        Compute and plot rolling mean, standard deviation, and covariance for a time series.

        Args:
            window (int): Window size for rolling calculations (default: self.window).

        Returns:
            dict: Dictionary containing rolling statistics, the figure, and a summary message.
        """
        try:
            win = window if window is not None else self.window
            roll_mean = self.series.rolling(win).mean()
            roll_std = self.series.rolling(win).std()
            roll_cov = self.series.rolling(win).cov(self.series.shift(1))

            fig, ax = plt.subplots(figsize=(15, 6))
            ax.plot(self.series.index, self.series, label="Original", alpha=0.5)
            ax.plot(roll_mean.index, roll_mean, label="Rolling Mean", color='blue')
            ax.plot(roll_std.index, roll_std, label="Rolling Std Dev", color='green')
            ax.plot(roll_cov.index, roll_cov, label="Rolling Covariance", color='purple')
            ax.set_title(f"Rolling Statistics (Window={win})")
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Use .name if Series, else fallback
            series_name = getattr(self.series, 'name', None)
            if not series_name:
                series_name = 'series'
            log_plot_to_html_report(fig, title=f"Rolling Statistics of {series_name}", report_path=self.report_path)
            plt.close(fig)

            msg = f"""
            Rolling statistics over window = {win} computed for:
            1. Mean
            2. Standard Deviation
            3. Covariance (with lagged series)

            <b>Tip:</b> Rolling metrics help identify trends, volatility, and local stability.
            """
            log_message_to_html_report(message=msg.strip(), title="Rolling Statistics Summary", report_path=self.report_path)

            return {
                "window": win,
                "rolling_mean": roll_mean,
                "rolling_std": roll_std,
                "rolling_cov": roll_cov,
                "fig": fig,
                "message": msg.strip()
            }
        except Exception as e:
            log_message_to_html_report(f"Error in rolling_statistics: {e}", title="Rolling Statistics Error", report_path=self.report_path)
            print(f"Exception in rolling_statistics: {e}")
            return {}

    def adf_test(self, autolag='AIC'):
        """
        Perform Augmented Dickey-Fuller test and return results as a dictionary.

        Args:
            autolag (str): Method to use when automatically determining the lag (default: 'AIC').

        Returns:
            dict: Results of the ADF test.
        """
        try:
            result = adfuller(self.series.dropna(), autolag=autolag)
            output = {
                'ADF Statistic': result[0],
                'p-value': result[1],
                'Num Lags Used': result[2],
                'Num Observations Used': result[3],
                'Critical Values': result[4],
                'IC Best': result[5]
            }
            return output
        except Exception as e:
            log_message_to_html_report(f"Error in adf_test: {e}", title="ADF Test Error", report_path=self.report_path)
            print(f"Exception in adf_test: {e}")
            return {}

    def kpss_test(self, regression='c', lags='auto'):
        """
        Perform KPSS test and return results as a dictionary.

        Args:
            regression (str): Type of regression for the test ('c' or 'ct').
            lags (str or int): Number of lags to use (default: 'auto').

        Returns:
            dict: Results of the KPSS test.
        """
        try:
            result = kpss(self.series.dropna(), regression=regression, lags=lags)
            output = {
                'KPSS Statistic': result[0],
                'p-value': result[1],
                'Num Lags Used': result[2],
                'Critical Values': result[3]
            }
            return output
        except Exception as e:
            log_message_to_html_report(f"Error in kpss_test: {e}", title="KPSS Test Error", report_path=self.report_path)
            print(f"Exception in kpss_test: {e}")
            return {}

    def print_adf_summary(self, autolag='AIC'):
        """
        Return a Markdown-formatted summary of the ADF test results.

        Args:
            autolag (str): Method for lag selection.

        Returns:
            str: Markdown-formatted summary.
        """
        try:
            result = self.adf_test(autolag)
            if not result:
                return "ADF test failed. See logs for details."
            summary_md = f"""
**Augmented Dickey-Fuller Test Results**

- **ADF Statistic:** `{result['ADF Statistic']:.4f}`
- **p-value:** `{result['p-value']:.4g}`
- **Num Lags Used:** `{result['Num Lags Used']}`
- **Num Observations Used:** `{result['Num Observations Used']}`

**Critical Values:**
"""
            for key, value in result['Critical Values'].items():
                summary_md += f"\n- `{key}`: `{value:.4f}`"
            summary_md += f"\n- **IC Best:** `{result['IC Best']:.4f}`"

            if result["p-value"] <= 0.05:
                summary_md += "\n\n**-->** ✅ **Reject the null hypothesis:** The time series is **stationary**."
            else:
                summary_md += "\n\n**-->** ⚠️ **Fail to reject the null hypothesis:** The time series is **non-stationary**."
            log_message_to_html_report(message=summary_md.strip(), title="ADF Test Summary", report_path=self.report_path)
            return summary_md
        except Exception as e:
            log_message_to_html_report(f"Error in print_adf_summary: {e}", title="ADF Summary Error", report_path=self.report_path)
            print(f"Exception in print_adf_summary: {e}")
            return "ADF summary failed. See logs for details."

    def plot_seasonal_decompose(
        self,
        model: str = 'additive',
        period: int = 12,
        title: str = 'Seasonal Decomposition'
    ) -> plt.Figure:
        """
        Plot and log the seasonal decomposition of a time series.

        Args:
            model (str): 'additive' or 'multiplicative'.
            period (int): The period for decomposition (e.g., 12 for monthly data).
            title (str): Plot title.

        Returns:
            plt.Figure: The matplotlib figure object.
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            decomposition = seasonal_decompose(self.series.dropna(), model=model, period=period)
            fig = decomposition.plot()
            fig.set_size_inches(10, 8)
            plt.suptitle(title)
            plt.tight_layout()
            log_plot_to_html_report(fig, title=f"Seasonal Decomposition", report_path=self.report_path)
            plt.close(fig)
            return fig
        except Exception as e:
            log_message_to_html_report(f"Error in plot_seasonal_decompose: {e}", title="Seasonal Decompose Error", report_path=self.report_path)
            print(f"Exception in plot_seasonal_decompose: {e}")
            return None

    def run_stationarity_pipeline(self, window: int = 12, adf_autolag: str = 'AIC', decompose_model: str = 'additive', decompose_period: int = None):
        """
        Run a pipeline: rolling average visual, ADF summary, and seasonal decomposition.
        Args:
            self: Stationaritychecker instance (uses self.series).
            window: int, window for rolling statistics.
            adf_autolag: str, autolag parameter for ADF test.
            decompose_model: str, 'additive' or 'multiplicative' for seasonal decomposition.
            decompose_period: int, period for seasonal decomposition.
        """

        try:
            print("="*60)
            print("**1. Augmented Dickey-Fuller Test**".center(60))
            print("="*60)
            display(Markdown("### 1. Augmented Dickey-Fuller Test"))
            display(Markdown(self.print_adf_summary(autolag=adf_autolag)))

            print("\n" + "="*60)
            print("**2. Seasonal Decomposition Visual**".center(60))
            print("="*60)
            display(Markdown("### 2. Seasonal Decomposition Visual"))
            display(self.plot_seasonal_decompose(model=decompose_model, period=decompose_period))

            print("\n" + "="*60)
            print("**3. Rolling Statistics Visual**".center(60))
            print("="*60)
            display(Markdown("### 3. Rolling Statistics Visual"))
            rolling_stats = self.rolling_statistics(window=window)
            display(Markdown(rolling_stats.get('message', '')))
            display(rolling_stats.get('fig', None))
        except Exception as e:
            log_message_to_html_report(f"Error in stationarity_pipeline: {e}", title="Stationarity Pipeline Error", report_path=self.report_path)
            print(f"Exception in stationarity_pipeline: {e}")  

if __name__ == "__main__":
    import pandas as pd

    # Example: Load a time series from CSV
    # Replace with your actual file and column names
    df = pd.read_csv("data/complaints.csv", parse_dates=["date"], index_col="date")
    series = df["complaints"]

    # Create an instance of Stationaritychecker
    checker = Stationaritychecker(series, window=12)

    # Run rolling statistics
    rolling_stats = checker.rolling_statistics()
    print("Rolling statistics computed and logged.")

    # Run ADF test and print summary
    adf_summary = checker.print_adf_summary()
    print(adf_summary)

    # Run KPSS test
    kpss_result = checker.kpss_test()
    print("KPSS test result:", kpss_result)

    # Plot and log seasonal decomposition
    checker.plot_seasonal_decompose(model='additive', period=12)

    # Or run the full pipeline
    # Stationaritychecker.stationarity_pipeline(series, window=12, adf_autolag='AIC', decompose_model='additive', decompose_period=