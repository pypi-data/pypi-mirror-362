from dynamicts.analysis import UnivariateAnalysis
from dynamicts.data_loader import DataLoader
from dynamicts.lag_correlation import Correlation


class DynamicTSA:
    def __init__(self, filepath, target_col, index_col=None, parse_dates = True, lags = 20):
        self.filepath  = filepath
        self.target_col = target_col
        self.index_col = index_col
        self.parse_dates = parse_dates
        self.lags = lags
        self.data = None

    def run(self):
        # Loading data
        loader = DataLoader(filepath=self.filepath, index_col=self.index_col, parse_dates=self.parse_dates)
        df = loader.run_pipeline()

        if df is None:
            print("Data loading failed or data is not regular.")
            return
        
        # Univariate analysis
        ua = UnivariateAnalysis(df, target_col=self.target_col, index_col=self.index_col, output_filepath=self.filepath )
        ua.plot_distribution()
        ua.check_distribution_stats()
        ua.check_missing_values()
        ua.detect_outliers()

        # lag correlation (ACF/PACF)
        corr = Correlation(df=df, target_col=self.target_col, lags=self.lags, output_filepath=self.filepath)
        corr = Correlation(df=df, target_col=self.target_col, lags=self.lags, output_filepath=self.filepath)
        corr.acf_plot()
        corr.pacf_plot()

        print("Dynamic time series analysis pipeline completed.")

# Example usage:
if __name__ == "__main__":
    tsa = DynamicTSA(
        filepath="data/bitcoin_price.csv",
        target_col="Close",
        index_col="Date",
        lags=30
    )
    tsa.run()