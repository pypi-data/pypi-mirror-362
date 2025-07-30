# DynamicTS

## What is DynamicTS?

**DynamicTS** is an educational-first Python library for time series analysis and preprocessing.  
It is designed to make time series workflows easy to use, easy to interpret, and easy to teach.  
DynamicTS provides clear, automated reports and visualizations that help users not only run analyses, but also understand and explain the results.

Whether you are a student, educator, or practitioner, DynamicTS aims to bridge the gap between powerful time series methods and accessible, readable outputs.  
With a focus on transparency and best practices, DynamicTS is your companion for learning, teaching, and applying time series analysis in Python.
A Python library for time series analysis.

## Main Features

DynamicTS is built to make time series analysis accessible and insightful by combining robust analytics with clear, user-friendly reporting. Each module is designed to automate best practices and generate readable reports that help users interpret results with confidence.

- **Data Loader Module**  
  Load your time series data from CSV files with robust handling of date parsing and index regularity checks. The loader automatically validates your data, checks for  irregular timestamps, and saves metadata reports for easy reference.
2
- **Analysis Module**  
  Perform comprehensive univariate analysis on your time series data. This module automatically generates distribution plots, missing value checks and outlier detection. All results are compiled into a well-structured Markdown or HTML report, making it easy to review and share insights.

- **Lag Correlation Module**  
  Explore autocorrelation and partial autocorrelation with ACF and PACF plots, as well as lag matrix visualizations. The module summarizes findings in a report, highlighting significant lags and patterns to help you understand temporal dependencies in your data.


- **Stationarity Module**  
  Assess the stationarity of your time series using statistical tests like the Augmented Dickey-Fuller (ADF) test and rolling statistics. The module generates clear visualizations and a summary report, guiding you through the interpretation of stationarity results and next steps.

- **Volatility Check Module**  
  Assess the volatility and variability of your time series using advanced models such as ARCH and GARCH. This module applies these models to detect and visualize periods of changing volatility, helping you understand the dynamic behavior of your data. Results are presented through intuitive plots and a concise, user-friendly report, making it easy to interpret volatility patterns and their implications for stationarity.

All modules are designed to output their results as readable, shareable reports (Markdown or HTML) saved next to your data file by default. This ensures that every analysis is not only rigorous, but also easy to understand and communicate.

## Where to Get DynamicTS

You can easily install DynamicTS using pip from the Python Package Index (PyPI):

```sh
pip install dynamicts
```

PyPI page: [https://pypi.org/project/dynamicts/](https://pypi.org/project/dynamicts/)

Alternatively, you can get the latest development version directly from GitHub:

```sh
pip install git+https://github.com/Chinar-Quantum-AI-Ltd/DynamicTS.git
```

GitHub repository: [https://github.com/Chinar-Quantum-AI-Ltd/DynamicTS](https://github.com/Chinar-Quantum-AI-Ltd/DynamicTS)

## Maintainers

### Cultivating AI Excellence

DynamicTS is maintained by [Chinar Quantum AI (CQAI)](https://chinarqai.com), an organization dedicated to advancing AI education and workforce readiness.

At CQAI, we believe in training differently to address the exponential growth of the AI industry and the evolving demands of the job market. Our tailored training programs, rooted in first principles, bridge the gap between diverse backgrounds and industry requirements. By focusing on generative AI, we empower individuals to meet the industry's burgeoning demands and play a significant role in mitigating the global unemployment crisis.

Our approach is multifaceted, with strategic objectives such as industry-grade projects, comprehensive mathematical and computational training, and partnerships with various institutions. Through these initiatives, we democratize AI education, empowering individuals from diverse backgrounds to pursue rewarding careers in AI and Data Science.

Learn more about our mission and programs at [chinarqai.com](https://chinarqai.com).

## Dependencies

DynamicTS relies on a set of well-established Python libraries to provide robust time series analysis and reporting:

- **pandas**: For data manipulation and handling time series data structures.
- **numpy**: For efficient numerical computations and array operations.
- **matplotlib**: For generating high-quality plots and visualizations.
- **statsmodels**: For advanced statistical modeling and time series analysis, including stationarity tests.
- **seaborn**: For enhanced statistical data visualization.
- **pytest (>=7.4.0)**: For running the test suite and ensuring code reliability.
- **IPython**: For interactive computing and improved notebook integration.
- **arch (==7.2.0)**: For volatility modeling using ARCH and GARCH models.

These dependencies ensure that DynamicTS delivers a comprehensive, reliable, and user-friendly experience for time series analysis and education.
