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
git clone https://github.com/bzamecnik/shoptet-invoice-en.git

# or

git@github.com:bzamecnik/shoptet-invoice-en.git

cd shoptet-invoice-en/
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

Login to Shoptet admin in your browser and find out the PHP session id and
server id of the sticky session.

Then call the script with the numeric invoice id and the login identifiers. 

```
shoptet_translate -i INVOICE_ID -p PHPSESSID -s SRV_ID
```

It will download the invoice HTML, clean it up, translate from Czech to English
and convert to PDF. By default it's saved to `./data/invoice-INVOICE_ID.html`.

If you need to change the translations, modify `data/translations.csv`.
