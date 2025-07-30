import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import skew, kurtosis
from IPython.display import display, Markdown
from datetime import datetime

from dynamicts.report_generator import log_message_to_html_report, log_plot_to_html_report

class UnivariateAnalysis:
    def __init__(self, df: pd.DataFrame, target_col: str, index_col: str = "date"):
        self.df = df
        self.target_col = target_col

        column_map = {col.lower(): col for col in self.df.columns}
        target_col_lower = self.target_col.lower()

        if target_col_lower not in column_map:
            raise ValueError(f"Target column '{self.target_col}' not found in dataset columns: {self.df.columns.tolist()}")

        self.target_col = column_map[target_col_lower]
        self.date_col = self.df.index.name

        # Generate report path ONCE per instance
        root_dir = os.path.abspath(os.curdir)
        report_root = os.path.join(root_dir, "reports")
        os.makedirs(report_root, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"analysis_report_{timestamp}.html"
        self.report_path = os.path.join(report_root, report_name)

    def plot_distribution(self) -> plt.Figure:
        y = self.df[self.target_col].dropna()
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        sns.histplot(y, kde=True, ax=axes[0], bins=30, color='cornflowerblue')
        axes[0].set_title(f"Distribution of {self.target_col}")
        axes[0].set_xlabel(self.target_col)
        axes[0].set_ylabel("Frequency")

        sns.boxplot(x=y, ax=axes[1], color="lightcoral")
        axes[1].set_title(f'Boxplot of {self.target_col}')
        axes[1].set_xlabel(self.target_col)

        plt.tight_layout()
        log_plot_to_html_report(fig, title=f"Distribution of {self.target_col}", report_path=self.report_path)
        plt.close(fig)
        return fig

    def check_distribution_stats(self):
        y = self.df[self.target_col].dropna()
        skewness_val = skew(y)
        kurtosis_val = kurtosis(y)

        if abs(skewness_val) < 0.5:
            skew_msg = "approximately_symmetric"
        elif skewness_val > 0:
            skew_msg = "right_skewed"
        else:
            skew_msg = "left_skewed"

        if kurtosis_val < 0:
            kurt_msg = "light_tailed (platykurtic)"
        elif kurtosis_val > 0:
            kurt_msg = "heavy_tailed (leptokurtic)"
        else:
            kurt_msg = "normal_tailed (mesokurtic)"

        full_msg = (
            f"Skewness of '{self.target_col}': {skewness_val:.4f}\n"
            f"Kurtosis of '{self.target_col}': {kurtosis_val:.4f}\n"
            f"→ Distribution is {skew_msg} and {kurt_msg}."
        )

        log_message_to_html_report(message=full_msg, title=f"Distribution Stats: {self.target_col}", report_path=self.report_path)

        return {
            "skewness": skewness_val,
            "kurtosis": kurtosis_val,
            "skewness_interpretation": skew_msg,
            "kurtosis_interpretation": kurt_msg,
            "full_message": full_msg
        }

    def check_missing_values(self):
        series = self.df[self.target_col]
        total_points = len(series)
        missing_count = series.isna().sum()
        missing_percentage = (missing_count / total_points) * 100

        msg = f"""
        Total Observations: {total_points}
        Missing values in '{self.target_col}': {missing_count} ({missing_percentage:.2f}%)
        """

        if missing_count > 0:
            msg += "<b>Recommendation:</b> Consider forward/backward fill or interpolation if your model does not support missing values."

        log_message_to_html_report(message=msg, title=f"Missing Value Analysis for '{self.target_col}'", report_path=self.report_path)
        return {
            "total_observations": total_points,
            "missing_count": missing_count,
            "missing_percentage": missing_percentage,
            "message": msg.strip()
        }

    def detect_outliers(self, method="both", plot=True):
        y = self.df[self.target_col].dropna()

        Q1 = y.quantile(0.25)
        Q3 = y.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = y[(y < Q1 - 1.5 * IQR) | (y > Q3 + 1.5 * IQR)]

        z_scores = np.abs(stats.zscore(y))
        z_outliers = y[z_scores > 3]

        if method == "iqr":
            combined_outliers = iqr_outliers
            method_label = "IQR"
        elif method == "zscore":
            combined_outliers = z_outliers
            method_label = "Z-Score"
        else:
            combined_outliers = y[(y.index.isin(iqr_outliers.index)) | (y.index.isin(z_outliers.index))]
            method_label = "IQR + Z-Score"

        outlier_count = len(combined_outliers)
        total = len(y)
        percentage = (outlier_count / total) * 100

        msg = f"""
        Outlier Detection using: {method_label}
        Total Observations: {total}
        Outliers Detected: {outlier_count} ({percentage:.2f}%)

        <b>Recommendation:</b> Investigate these points manually before deciding to remove or treat them.
        """
        log_message_to_html_report(message=msg, title=f"Outlier Detection ({method_label})", report_path=self.report_path)

        fig = None
        if plot:
            fig, ax = plt.subplots(figsize=(12, 5))
            sns.lineplot(x=y.index, y=y, label="Original Data", ax=ax)
            sns.scatterplot(x=combined_outliers.index, y=combined_outliers, color='red', s=40, label="Outliers", ax=ax)
            ax.set_title(f"Outliers Detected using {method_label}")
            ax.set_ylabel(self.target_col)
            ax.set_xlabel("Date")
            plt.xticks(rotation=45)
            plt.tight_layout()
            log_plot_to_html_report(fig=fig, title=f"{method_label} Outlier Detection for {self.target_col}", report_path=self.report_path)
            plt.close(fig)

        return {
            "method": method_label,
            "total_observations": total,
            "outliers_detected": outlier_count,
            "percentage_outliers": percentage,
            "outlier_indices": combined_outliers.index.tolist(),
            "outlier_values": combined_outliers.tolist(),
            "fig": fig
        }

    def run_univariate_analysis(self, df: pd.DataFrame = None, target_col: str = None, index_col: str = None):
        """
        Run univariate analysis using instance attributes by default, or override with provided arguments.
        """
        df = df if df is not None else self.df
        target_col = target_col if target_col is not None else self.target_col
        index_col = index_col if index_col is not None else self.date_col

        if df is None or target_col is None:
            raise ValueError("DataFrame and target_col must be provided either as arguments or instance attributes.")

        try:
            print(f"\nRunning Univariate Time Series Analysis on '{target_col}' ")
            analysis = UnivariateAnalysis(df=df, target_col=target_col, index_col=index_col)
            results = {}

            fig_dist = analysis.plot_distribution()
            display(fig_dist)
            results["distribution_plot"] = fig_dist

            dist_stats = analysis.check_distribution_stats()
            display(Markdown(f"### Distribution Stats\n{dist_stats['full_message']}"))
            results["distribution_stats"] = dist_stats

            missing = analysis.check_missing_values()
            display(Markdown(f"### Missing Value Info\n{missing['message']}"))
            results["missing_values"] = missing

            outliers = analysis.detect_outliers(method="both", plot=True)
            display(Markdown(f"### Outliers Detected: {outliers['outliers_detected']} ({outliers['percentage_outliers']:.2f}%)"))
            display(outliers["fig"])
            results["outliers"] = outliers

            display(Markdown("Univariate Time Series Analysis Completed."))
            return results

        except Exception as e:
            print(f"Error in univariate analysis: {e}")
            return None

if __name__ == "__main__":
    from dynamicts.data_loader import DataLoader

    loader = DataLoader(filepath="data/complaints.csv", index_col="date")
    df = pd.read_csv("data/complaints.csv")
    analysis = UnivariateAnalysis(
        df=df,
        target_col="complaints",
        index_col="date"
    )
    results = analysis.run_univariate_analysis()