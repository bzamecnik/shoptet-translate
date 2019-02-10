"""
Translates a Shoptet invoice from Czech to English and converts to PDF.
"""
import argparse
from functools import partial

from shoptet_translate.cleanup import cleanup_html
from shoptet_translate.download import download_invoice, invoice_types
from shoptet_translate.translator import InvoiceTranslator


def main():
    def parse_args():
        parser = argparse.ArgumentParser(
            'shoptet_translate',
            description='Translates a Shoptet invoice from Czech (HTML) to English (PDF, HTML)')

        parser.add_argument('input_file', metavar='INPUT_FILE', help='Source invoice path (HTML)')
        parser.add_argument('-d', '--domain', default='https://eshop.svet-3d-tisku.cz', help='Domain')

        return parser.parse_args()

    args = parse_args()
    cleanup_func = partial(cleanup_html, domain=args.domain)
    InvoiceTranslator(cleanup_func).translate(args.input_file)


def download_and_translate():
    def parse_args():
        parser = argparse.ArgumentParser(
            'shoptet_translate',
            description='Downloads an invoice from Shoptet admin UI, '
                        'translates it to English and converts to PDF')
        parser.add_argument('-i', '--invoice-id', required=True, help='Invoice number')
        parser.add_argument('-t', '--invoice-type', required=True, choices=invoice_types,
            help='Invoice type (%s)' % ', '.join(invoice_types))
        parser.add_argument('-p', '--php-session-id', required=True, help='Existing admin UI session (cookie PHPSESSID)')
        parser.add_argument('-s', '--server-id', required=True, help='For sticky sessions (cookie SRV_ID)')
        parser.add_argument('-o', '--output', default='data/', help='Output dir or name')
        parser.add_argument('-d', '--domain', default='https://eshop.svet-3d-tisku.cz', help='Domain')

        return parser.parse_args()

    args = parse_args()
    # TODO: retrieve the cookie by opening the login page
    cookies = {
        'SRV_ID': args.server_id,
        'PHPSESSID': args.php_session_id,
    }
    html_cz_path = download_invoice(
        args.invoice_id, args.invoice_type,
        args.output, args.domain,
        cookies)
    InvoiceTranslator().translate(html_cz_path)


if __name__ == '__main__':
    main()
