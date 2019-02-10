import os

from flask import Flask, make_response, render_template, request, flash, \
    url_for, send_from_directory, redirect
import pdfkit
from werkzeug.utils import secure_filename

from shoptet_translate.cleanup import cleanup_html
from shoptet_translate.translator import TextTranslator

UPLOAD_FOLDER = os.path.abspath('translated/')
ALLOWED_EXTENSIONS = set(['html', 'htm'])
ESHOP_DOMAIN = 'https://eshop.svet-3d-tisku.cz/'

app = Flask(__name__)
app.secret_key = b'\x1c\xa7TT\x07\x99\x86\xe1\xa2\xfd(\xfeRx3\x12'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html', domain=ESHOP_DOMAIN)


@app.route('/translated/<filename>')
def translated(filename):
    base_name = os.path.splitext(filename)[0]
    html_en_filename ='%s-en.html' % base_name
    pdf_en_filename = '%s-en.pdf' % base_name

    orig_html_url = url_for('translated_export', filename=filename)
    translated_html_url = url_for('translated_export', filename=html_en_filename)
    translated_pdf_url = url_for('translated_export', filename=pdf_en_filename)
    return render_template('translated.html',
        filename=filename,
        orig_html_url=orig_html_url,
        translated_html_url=translated_html_url,
        translated_pdf_url=translated_pdf_url)


@app.route('/', methods=['POST'])
def translate():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file was uploaded')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No file was selected')
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash('Not allowed file type: %s' % os.path.splitext(file.filename)[1])
        return redirect(request.url)

    dir = app.config['UPLOAD_FOLDER']
    orig_filename = secure_filename(file.filename)

    html_cz = file.read().decode('utf-8')
    html_cz = cleanup_html(html_cz, domain=request.form['domain'])

    with open(os.path.join(dir, orig_filename), 'wt') as f:
        f.write(html_cz)

    html_en = TextTranslator().translate(html_cz)
    base_name = os.path.splitext(orig_filename)[0]

    html_en_filename ='%s-en.html' % base_name
    html_en_path = os.path.join(dir, html_en_filename)
    pdf_en_filename = '%s-en.pdf' % base_name
    pdf_en_path = os.path.join(dir, pdf_en_filename)

    with open(html_en_path, 'wt') as f:
        f.write(html_en)
    pdfkit.from_string(html_en, pdf_en_path)

    return redirect(url_for('translated', filename=orig_filename))

@app.route('/translated/export/<filename>')
def translated_export(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run()
