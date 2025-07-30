import os
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_circuit
from jinja2 import Environment, FileSystemLoader
from .visualization import create_performance_plot
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ReportGenerator:
    def __init__(self, template_dir="templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def generate(self, data, output_format="pdf"):
        logger.info(f"Generating {output_format} report")
        
        # Generate visualizations
        fig1 = plot_histogram(data['counts'])
        plt.savefig('counts_histogram.png')
        
        fig2 = plot_circuit(data['circuit'])
        fig2.savefig('circuit_diagram.png')
        
        fig3 = create_performance_plot(data['metrics'])
        fig3.savefig('performance_metrics.png')
        
        # Render LaTeX template
        template = self.env.get_template("report_template.tex")
        rendered = template.render(
            title=data['title'],
            metrics=data['metrics'],
            circuit_image='circuit_diagram.png',
            histogram_image='counts_histogram.png',
            performance_image='performance_metrics.png'
        )
        
        # Write to file
        with open("report.tex", "w") as f:
            f.write(rendered)
        
        # Compile to PDF if requested
        if output_format == "pdf":
            os.system("pdflatex report.tex")
        
        return "report.pdf"
