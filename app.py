from flask import Flask, request, render_template, send_file
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        filename = request.form['filename']
        text = request.form['text']
        fontsize = int(request.form['fontsize'])  # Get the font size from the form

        if not filename or not text:
            error = 'Both fields are required.'
        else:
            pdf_path = f"static/{filename}.pdf"

            # Create PDF
            pdf = SimpleDocTemplate(
                pdf_path,
                pagesize=letter
            )

            # Container for the 'Flowable' objects
            elements = []

            # Create a custom ParagraphStyle with the user-defined font size
            custom_style = ParagraphStyle(
                'CustomStyle',
                parent=getSampleStyleSheet()['Normal'],
                fontSize=fontsize,
                leading=fontsize * 1.2,  # Line spacing
            )

            # Replace newline characters with line break tags
            text_with_breaks = text.replace("\n", "<br/>")

            # Add the Paragraph with the user's text and custom style
            elements.append(Paragraph(text_with_breaks, custom_style))

            # Build the PDF
            pdf.build(elements)

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f"{filename}.pdf"
            )

    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
