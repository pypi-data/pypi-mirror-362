import base64
import io
from datetime import datetime
import os

def log_plot_to_html_report(fig, title, report_path):
    """
    Logs a matplotlib figure to an HTML report file, saving in the root 'reports' directory.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The matplotlib figure to be saved.
    title : str
        The title for the plot section in the report.
    mod_name : str, optional
        Module name to use in the report file name.
    """
    # Ensure the reports directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    # Save figure to a BytesIO buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Convert image to base64 string
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # HTML content
    html_block = f"""
    <h2>{title}</h2>
    <img src="data:image/png;base64,{encoded}" style="max-width:100%; height:auto;">
    <p><em>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    <hr>
    """

    # Write or append to HTML file
    if not os.path.exists(report_path):
        with open(report_path, "w") as f:
            f.write("<html><head><title>Time Series Analysis Report</title></head><body>")
            f.write(html_block)
    else:
        with open(report_path, "a") as f:
            f.write(html_block)

def log_message_to_html_report(message, title, report_path):
    """
    Logs a text message to an HTML report file at the given report_path.
    """
    # Ensure the reports directory exists
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    html_block = f"""
    <h2>{title}</h2>
    <p style="font-family: monospace; white-space: pre-wrap;">{message}</p>
    <p><em>Logged on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    <hr>
    """

    if not os.path.exists(report_path):
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Time Series Analysis Report</title></head><body>")
            f.write(html_block)
    else:
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(html_block)