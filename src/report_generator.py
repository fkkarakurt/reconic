"""
HTML Report Generator

This script, part of a broader project, is dedicated to generating HTML reports from given data. 
It utilizes the Jinja2 templating engine to render HTML content dynamically, 
based on the results passed to it and the current date and time. The script is designed to be flexible, 
allowing for the specification of different templates and output files.

The ReportGenerator class encapsulates the functionality for generating these reports. 
It initializes with the data (results) to be included in the report and the path to the template folder. 
The generate_html_report method then renders a specified template with the provided data and the current timestamp, 
outputting the final report to a specified file.

Features:
- Dynamic HTML report generation using Jinja2 templating.
- Customizable report templates and output file names.
- Integration of current date and time for report metadata.

Important:
This tool is designed for projects requiring automated report generation, such as data analysis, 
web scraping, or monitoring applications. It is essential to have the Jinja2 package installed and 
to provide a valid template file within the specified template folder.


Example Use Case:
Could be used in an automated web scraping project to generate a summary report of the data collected over a period, 
providing insights into trends or changes.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-11
Last Updated: 2024-02-18
"""


import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

class ReportGenerator:
    def __init__(self, results, template_folder='templates'):
        self.results = results
        # Using __file__ to determine the project home directory
        project_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        template_folder = os.path.join(project_root, template_folder)
        self.env = Environment(loader=FileSystemLoader(template_folder))
        
        # The path to the output directory is relative to the project root directory
        self.output_dir = os.path.join(project_root, "output")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_html_report(self, output_file='report.html'):
        template = self.env.get_template("report_template.html")
        rendered_html = template.render(results=self.results, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        output_file_path = os.path.join(self.output_dir, output_file)
        with open(output_file_path, 'w') as file:
            file.write(rendered_html)

        print(f"Report generated: {output_file_path}")
        print("\n")

