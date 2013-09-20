from setuptools import setup, find_packages
setup (name     = 'arsespyder',
       version  = '0.0.1',
       packages = find_packages(),
       scripts  = [''],            # The one to go to exec dir (/usr/bin basically)
       install_requires = ['bs4'], # For Beautiful Soup, version 4
       package_data = {},          #
       author   = "Sergio",
       author_email = "sergio@undersea", # WARNING: It will be published on the Internet
       description = "Web Spider to retrieve links",
       license = "",
       keywords = "",
       url = "github.com/mypypy", # MANDATORY
       long_description = "",
       download_url = "", )
