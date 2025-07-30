import base64
import io
from datetime import datetime
import os


class Reports:
    def __init__(self, fig=None, title: str = None, message: str = None, data_filepath: str = None, report_name: str = "report.html", mod_name: str = "default_mod"):
        self.fig = fig
        self.title = title
        self.message = message
        self.mod_name = mod_name
        # Default data_filepath to current file's directory if not provided
        if data_filepath is None:
            self.data_filepath = os.path.dirname(__file__)
        else:
            self.data_filepath = data_filepath

        # Set up report directory and path
        base_name = os.path.splitext(os.path.basename(self.data_filepath))[0]
        root_dir = os.path.abspath(os.curdir)
        self.report_root = os.path.join(root_dir, "reports")
        os.makedirs(self.report_root, exist_ok=True)
        self.report_path = os.path.join(self.report_root, self.mod_name+report_name)

        # Check if the report file exists
        self.report_exists = os.path.exists(self.report_path)

        # Optionally, create the file if it doesn't exist
        if not self.report_exists:
            with open(self.report_path, "w", encoding="utf-8") as f:
                f.write("")  # Create an empty file

    def log_plot_to_md_report(self, report_name: str = "report.md") -> None:
        """
        Logs a matplotlib figure to a Markdown report file, saving in a directory based on the data file name.
        """
        # Check if the report file exists, create if not
        if not os.path.exists(self.report_path):
            with open(self.report_path, "w", encoding="utf-8") as f:
                f.write("")
            self.report_exists = True

        # Save plot to memory
        buf = io.BytesIO()
        self.fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)

        # Convert to base 64
        encoded = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()

        # MD Embed
        markdown_block = f"""
    ## {self.title}
    ![{self.title}](data:image/png;base64,{encoded})
    <sub>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</sub>
    ---
    """

        # Append to report file
        with open(self.report_path, "a") as f:
            f.write(markdown_block)

    def log_plot_to_html_report(self, report_name: str = "report.html") -> None:
        """
        Logs a matplotlib figure to an HTML report file, saving in a directory based on the data file name.
        """
        # Check if the report file exists, create if not
        if not os.path.exists(self.report_path):
            with open(self.report_path, "w") as f:
                f.write("<html><head><title>Time Series Analysis Report</title></head><body>")
            self.report_exists = True

        # Save figure to a BytesIO buffer
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        # Convert image to base64 string
        encoded = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        # HTML content
        html_block = f"""
    <h2>{self.title}</h2>
    <img src="data:image/png;base64,{encoded}" style="max-width:100%; height:auto;">
    <p><em>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    <hr>
    """

        # Write or append to HTML file
        with open(self.report_path, "a") as f:
            f.write(html_block)

    def log_message_to_html_report(self, report_name: str = "report.html") -> None:
        """
        Logs a text message to an HTML report file, saving in a directory based on the data file name.
        """
        # Check if the report file exists, create if not
        if not os.path.exists(self.report_path):
            with open(self.report_path, "w", encoding="utf-8") as f:
                f.write("<html><head><title>Time Series Analysis Report</title></head><body>")
            self.report_exists = True

        html_block = f"""
    <h2>{self.title}</h2>
    <p style="font-family: monospace; white-space: pre-wrap;">{self.message}</p>
    <p><em>Logged on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    <hr>
    """

        with open(self.report_path, "a", encoding="utf-8") as f:
            f.write(html_block)

    @staticmethod
    def append_all_reports(combined_report: str = "combined_report.html") -> None:
        """
        Appends the contents of all HTML reports in the reports directory into one combined report.
        Only runs if the reports directory exists and is not empty.
        """
        report_dir = os.path.dirname(os.path.dirname(__file__)) + "/reports"
        combined_path = os.path.join(report_dir, combined_report)

        # Check if reports directory exists and is not empty
        if not os.path.isdir(report_dir):
            print(f"Reports directory '{report_dir}' does not exist.")
            return
        report_files = [
            f for f in os.listdir(report_dir)
            if f.endswith(".html") and f != combined_report
        ]
        if not report_files:
            print(f"No HTML reports found in '{report_dir}'.")
            return

        contents = []
        for report_file in report_files:
            path = os.path.join(report_dir, report_file)
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Remove opening and closing HTML/body tags to avoid nesting
                    content = content.replace("<html>", "").replace("</html>", "")
                    content = content.replace("<body>", "").replace("</body>", "")
                    contents.append(f"<h1>{report_file}</h1>\n" + content)

        # Write combined content to new file
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Combined Report</title></head><body>\n")
            f.write("<hr>\n".join(contents))
            f.write("\n</body></html>")