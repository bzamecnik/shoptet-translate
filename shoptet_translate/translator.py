import argparse
from functools import partial
import os
import re
import unicodedata

import bs4
import pandas as pd
import pdfkit

from shoptet_translate.cleanup import cleanup_html

root_dir = os.path.abspath(os.path.dirname(__file__))


class InvoiceTranslator:
    def __init__(self, cleanup_func=None):
        self.cleanup_func = cleanup_func

    @staticmethod
    def read_invoice_html(path):
        with open(path) as f:
            return f.read()

    @staticmethod
    def write_invoice_html(html, path):
        with open(path, 'w') as f:
            f.write(html)

    @staticmethod
    def html_to_pdf(html_path, pdf_path):
        pdfkit.from_file(html_path, pdf_path)

    def translate(self, input_file):
        directory, basename = os.path.split(input_file)
        name = os.path.splitext(basename)[0]
        html_en_path = os.path.join(directory, '%s-en.html' % name)
        pdf_en_path = os.path.join(directory, '%s-en.pdf' % name)

        html_cz = self.read_invoice_html(input_file)
        if self.cleanup_func is not None:
            html_cz = self.cleanup_func(html_cz)
        html_en = TextTranslator().translate(html_cz)
        self.write_invoice_html(html_en, html_en_path)
        pdfkit.from_string(html_en, pdf_en_path)

        print('Translated to:', pdf_en_path)

        return pdf_en_path


class TextTranslator:
    def __init__(self, dict_path=None):
        if dict_path is None:
            dict_path = os.path.join(root_dir, 'translations.csv')
        self.translations = pd.read_csv(dict_path)

        # Both the document and the translation string need to be normalized
        # otherwise there might be mismatch between various unicode
        # representation of the same characters (with/without combining chars).
        for col in self.translations.columns:
            self.translations[col] = self.translations[col].apply(lambda s: unicodedata.normalize('NFC', s))
        # TODO: better actually perform topological sort...

        self._check_translations_sorted(self.translations)

    @staticmethod
    def _check_translations_sorted(translations):
        for i, row in translations.iterrows():
            superstrings = [other for other in translations['cz'][i + 1:] if row['cz'] in other]
            if superstrings:
                print(
                    'WARNING: translations have to be sorted to that no string is substring of a string after it!')
                print('String "%s" is substring of %s but should be placed after them' % (row['cz'], superstrings))

    def translate(self, html_cz):
        # TODO: We should better mark translated strings and ignore them from further translation.
        # NOTE: Using BeautifulSoup in order to translate only texts, not some HTML code.
        soup = bs4.BeautifulSoup(unicodedata.normalize('NFC', html_cz), features='html5lib')
        for i, row in self.translations.iterrows():
            for string_tag in soup.find_all(string=re.compile(re.escape(row['cz']))):
                string_tag.parent.string = string_tag.replace(row['cz'], row['en'])
        html_en = soup.prettify()
        return html_en


def parse_args():
    parser = argparse.ArgumentParser(
        'shoptet_translate',
        description='Translates Shoptet invoices from Czech (HTML) to English (PDF)')
    parser.add_argument('input_file', metavar='INPUT_FILE', help='Source invoice path (HTML)')
    parser.add_argument('-c', '--cleanup', action='store_true',
        help='First clean up the HTML page (remove scripts, make links absolute)')
    parser.add_argument(
        '-d', '--domain', default='https://eshop.svet-3d-tisku.cz', help='Domain')
    return parser.parse_args()


def main():
    args = parse_args()
    cleanup_func = partial(cleanup_html, domain=args.domain) if args.cleanup else None
    pdf_en_path = InvoiceTranslator(cleanup_func).translate(args.input_file)
    print('Translated to:', pdf_en_path)


if __name__ == '__main__':
    main()
