"""
Cleans up an invoice downloaded from Shoptet in HTML - removes scripts and makes
links to resources (CSS, images) absolute (for given e-shop domain).
"""

import argparse
import os

import bs4


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


def cleanup_invoice(input_path, domain, output_path):
    print('Opening:', input_path)
    with open(input_path, 'r') as f:
        html = f.read()

    print('Cleaning at domain:', domain)
    cleaned_html = cleanup_html(html, domain)

    print('Saving to:', output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(cleaned_html)


def parse_args():
    parser = argparse.ArgumentParser(
        'shoptet_cleanup_invoice',
        description='Cleans up an HTML invoice from Shoptet')
    parser.add_argument('input_html', help='Input HTML path')
    parser.add_argument(
        '-d', '--domain', default='https://eshop.svet-3d-tisku.cz', help='Domain')
    return parser.parse_args()


def main():
    args = parse_args()

    input_path = args.input_html
    input_name, input_ext = os.path.splitext(os.path.basename(input_path))
    output_path = os.path.join(os.path.dirname(
        input_path), '{}_clean{}'.format(input_name, input_ext))
    cleanup_invoice(input_path, args.domain, output_path)


if __name__ == '__main__':
    main()
