# Shoptet invoice translator (Czech to English)

Goal: Translate PDF invoices produced by Shoptet from Czech to English.

## Solution

Shoptet itself renders invoices from HTML to PDF using PHP library `mPDF`.
Fortunately it's admin UI provides invoices as HTML page for printing. We can
download this HTML (using `requests`), substitute strings from one language to
another (using `beautifulsoup`) and then render it to PDF again (using `pdfkit`).

## Requirements

### pdfkit

https://pypi.org/project/pdfkit/

```bash
# OSX:
brew cask install wkhtmltopdf
# Ubuntu:
sudo apt-get install wkhtmltopdf
# or install from https://wkhtmltopdf.org/
```

## Installation

```
git clone https://github.com/bzamecnik/shoptet-translate.git

# or

git@github.com:bzamecnik/shoptet-translate.git

cd shoptet-translate/
pip install -r requirements.txt

mkvirtualenv shoptet_translate
pip install -e .
```

On Ubuntu it needs to run via xvfb since native QT headless doesn't work well
in Debian. [Workaround](https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server):

```bash
sudo apt install wkhtmltopdf
sudo apt install xvfb
sudo printf '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh
sudo chmod a+x /usr/bin/wkhtmltopdf.sh
sudo ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf
# test it
wkhtmltopdf http://www.google.com output.pdf
```

## Usage

### Downloading from the web by hand

Login to Shoptet admin UI in your browser, go to the page with the document to
be translated. Find button Print (`Tisk - standardní` or `Vytisknout
objednávku`), click Save as to download the file locally. Move the file to a
location where `shoptet_translate` can see it.

```bash
# with default domain
$ shoptet_translate invoice.html

# or specifying the domain
$ shoptet_translate invoice.html -d https://example.com
```

It will clean up the HTML page from scripts and fix links to images, translate
from Czech to English, save as HTML and convert to PDF as well. Output:

- invoice-en.pdf
- invoice-en.html

### Downloading from web by the script

Login to Shoptet admin in your browser and find out the PHP session id and
server id of the sticky session.

Then call the script with the numeric invoice id and the login identifiers.

```bash
shoptet_translate_from_web -i INVOICE_ID -t INVOICE_TYPE -p PHPSESSID -s SRV_ID
```

It will download the invoice HTML, clean it up, translate from Czech to English
and convert to PDF. By default it's saved to `./data/INVOICE_TYPE-INVOICE_ID.html`.

If you need to change the translations, modify `data/translations.csv`.

### Web application

Development:

```
FLASK_ENV=debug FLASK_APP=shoptet_translate/webapp.py flask run
```

Open: http://localhost:5000
