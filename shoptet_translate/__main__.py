import argparse

from shoptet_translate.translator import InvoiceTranslator
from shoptet_translate.download import download_invoice, invoice_types


def parse_args():
    parser = argparse.ArgumentParser(
        'shoptet_translate',
        description='Downloads an invoice from Shoptet admin UI, translates it to English and converts to PDF')
    parser.add_argument('-i', '--invoice-id', required=True, help='Invoice number')
    parser.add_argument('-t', '--invoice-type', required=True, choices=invoice_types,
        help='Invoice type (%s)' % ', '.join(invoice_types))
    parser.add_argument('-p', '--php-session-id', required=True, help='Existing admin UI session (cookie PHPSESSID)')
    parser.add_argument('-s', '--server-id', required=True, help='For sticky sessions (cookie SRV_ID)')
    parser.add_argument('-o', '--output', default='data/', help='Output dir or name')
    parser.add_argument('-d', '--domain', default='https://eshop.svet-3d-tisku.cz', help='Domain')
    return parser.parse_args()


def main():
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
