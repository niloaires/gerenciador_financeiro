""""import io
import os
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, landscape
import datetime
from previsoes.models import PrevisoesModel

def converter_milimetro_ponto(mm):

    return mm/0.352777
def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 15, leading=None)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #p.drawImage()
    p.drawString(converter_milimetro_ponto(100), converter_milimetro_ponto(100), "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    data=datetime.datetime.now().strftime('%d-%m-%y')
    return FileResponse(buffer, as_attachment=True, filename='relatorio_previsoes_{}.pdf'.format(data))"""

import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from previsoes.models import PrevisoesModel
data=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
def some_view(request):
    contexto={
        'object_list':PrevisoesModel.objects.all(),
        'data_hora':data

    }
    html_string=render_to_string('relatorios/teste.html', contexto)
    html=HTML(string=html_string)
    html.write_pdf(target='/tmp/{}.pdf'.format(data));
    fs=FileSystemStorage('/tmp')
    with fs.open('{}.pdf'.format(data)) as pdf:
        response=HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition']='attachment; filename="relatorio_previsoes {}.pdf"'.format(data)
        return response
    return response

