import argparse
import os

import bs4
import requests

invoice_types = ['invoice', 'proformaInvoice', 'deliveryNote', 'creditNote']

def download_invoice(invoice_id, invoice_type, html_path, domain, cookies):
    # invoice_type - invoice/proformaInvoice/deliveryNote/creditNote
    if invoice_type not in invoice_types:
        raise ValueError('Invalid invoice type: %s (known types: %s)' %
            (invoice_type, ', '.join(invoice_types)))

    if not html_path:
        html_path = 'data/'
    if not os.path.basename(html_path):
        html_path = os.path.join(html_path, '%s-%s.html' % (invoice_type, invoice_id))

    url = domain + '/admin/tisk-dokladu/?type=%s&id=%s' % (invoice_type, invoice_id)
    response = requests.get(url, cookies=cookies)
    if response.status_code != 200:
        raise ValueError('Could not download %s: %s' % (invoice_type, invoice_id))

    html = cleanup_html(response.text, domain)

    print('Saving page to:', html_path)
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, 'w') as f:
        f.write(html)

    return html_path


def cleanup_html(html, domain):
    # Make links to script/image resource absolute (then there's no need to download them locally).
    # NOTE: These resources don't need authorization.
    html = html.replace('href="/cms/', 'href="%s/cms/' % domain)
    html = html.replace('src="/user/', 'src="%s/user/' % domain)

    page = bs4.BeautifulSoup(html, features='html5lib')
    # remove print dialog on load
    del page.body['onload']

    # remove scripts
    for s in page.find_all('script'):
        s.decompose()

    return page.prettify()


def parse_args():
    parser = argparse.ArgumentParser(
        'shoptet_download_invoice',
        description='Downloads an invoice as HTML from Shoptet admin UI')
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
    print('Downloaded to:', html_cz_path)


if __name__ == '__main__':
    main()
