from xhtml2pdf import pisa
from jinja2 import Environment, FileSystemLoader

def generate_invoice_pdf(order_data, output_filename):
    # Stel de Jinja2-omgeving in; zoekt naar templates in de "templates"-map
    env = Environment(loader=FileSystemLoader(searchpath="./templates"))
    template = env.get_template("invoice_template.html")
    
    # Render de template met de orderdata uit de webhook (bijvoorbeeld ordernummer, klantgegevens, etc.)
    rendered_html = template.render(order=order_data)
    
    # Maak de PDF aan van het gerenderde HTML
    with open(output_filename, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)
    if pisa_status.err:
        raise Exception("Er is een fout opgetreden bij het genereren van de PDF.")
