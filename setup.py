from setuptools import setup

setup(name = 'scrapenhl',
      version = '0.1',
      description = 'Scraping and manipulating NHL PbP data',
      url = 'https://github.com/muneebalam/scrapenhl',
      author = 'Muneeb Alam',
      author_email = 'muneeb.alam@gmail.com',
      license = 'MIT',
      packages = ['scrapenhl'],
      install_requires=[
            'pandas',
            'numpy',
            'scipy',
            'scikit-learn',
            'matplotlib',
            'seaborn',
          'feather-format'
      ],
      zip_safe = False)