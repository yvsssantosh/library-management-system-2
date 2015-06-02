## Minimum Requirements ##

  1. Python 2.6
  1. A database engine and the appropriate Python adapter for it
  1. web2py 1.74.3

## Recommended ##

  1. A web server (such as Apache)
  1. A version of mod\_wsgi appropriate for your web server
  1. lxml and python-amazon-product-api Python modules

You can install the LMS in one of two ways:  From SVN or from a w2p package.

You start by downloading web2py and unzipping it somewhere.  After that, run it with this command from your command prompt (you must be in the directory where web2py was unzipped to):
```
python web2py.py
```
You'll be prompted to set an adminstrator password.  After doing so, you can run web2py using this command to reuse your original admin password:
```
python web2py.py -a <recycle>
```

# From W2P #

  1. Download a prepackaged W2P file from this site.
  1. Login to web2py's admin site and click "browse" under "upload existing application".
  1. Browse to the W2P file.
  1. Give the new app a name, like library.
  1. Click Install.

# From SVN #

  1. Checkout the source from the SVN trunk to the applications folder of your web2py.
  1. The folder you check out to can only have letters in its name.
  1. Refresh the web2py site page, and you should see LMS listed by the folder name you checked out to.