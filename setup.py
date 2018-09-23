from setuptools import setup

setup(name='shoptet_translate',
      version='0.0.3',
      description='Translate Shoptet invoices',
      url='https://github.com/bzamecnik/shoptet-invoice-en',
      author='Bohumir Zamecnik',
      author_email='bohumir.zamecnik@gmail.com',
      license='MIT',
      packages=['shoptet_translate'],
      package_data={'shoptet_translate': ['data/translations.csv']},
      zip_safe=False,
      install_requires=[
      ],
      setup_requires=['setuptools-markdown'],
      long_description_markdown_filename='README.md',
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',
          'Topic :: Office/Business :: Financial :: Accounting',
          'Topic :: Text Processing :: General',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',

          'Operating System :: POSIX :: Linux',
      ],
      entry_points={
          'console_scripts': [
              'shoptet_translate = shoptet_translate.__main__:main',
          ]
      })
