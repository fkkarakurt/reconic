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
        if isinstance(self.results['Technologies'], set):
            self.results['Technologies'] = {tech: {} for tech in self.results['Technologies']}

        template = self.env.get_template("report_template.html")
        rendered_html = template.render(results=self.results, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        output_file_path = os.path.join(self.output_dir, output_file)
        with open(output_file_path, 'w') as file:
            file.write(rendered_html)

        print(f"Report generated: {output_file_path}")
        print("\n")

