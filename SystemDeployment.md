# Deploying the Library Management System #

The [web2py manual](http://www.web2py.com/examples/default/docs) has many examples and recipes for deploying web2py using the Apache webserver.  They're available starting on pg 281 (pg 297 of the actual document :)).  So I'll focus here on how I did it for my own in-house needs at home.


## Setting up ##

I assembled the following beforehand:
  1. Apache webserver 2.2 (with mod\_ssl)
  1. mod\_wsgi (Python handler module for Apache)
  1. Python 2.6
  1. PostgreSQL server
  1. psycopg (Python database connector to Postgres)
  1. web2py source distribution
  1. LMS application files

I installed Apache, Postgres, and Python to their default locations (respectively referred to hereafter as %APACHE%, %POSTGRES%, and %PYTHON%).  I put mod\_wsgi in Apache's modules directory.  I installed psycopg with default settings and put web2py in D:\web2py.  And of course, LMS :) installed in web2py applications folder.

## Configure web2py to run on port 80 ##

Web2py is designed to pick up an options file if it's present.  The file is named options.py and is the root of the web2py folder.  Find this file now and read its contents.  If you don't have options.py, find options\_std.py (which is an options file loaded with web2py's defaults).  Looks pretty standard, yes?  Just key=value pairs.  These will be loaded when web2py gets accessed from your webserver.

I just took the options\_std.py file, copied it to options.py, and used those settings for what I needed.  The port setting can be ignored, since web2py will run on whatever port the webserver is on.  The password is the special one, though.

A quick note about web2py's password setting:  This password controls access to the admin interface.  You set it the first time you ran web2py, in the GUI that came up.  Once the web2py server was running, a file was created that had this password stored in it, with the name parameters\_X (X is the port number that the server runs on).  That file gets loaded with every launch of the web2py server on that same port.

This led to a bit of a wrinkle during my deployment:  I had never run web2py on port 80, so there was no parameters\_80 file.  I had to start web2py at least once with an admin password set on port 80 for that file to be generated.  Thereafter, web2py would load that parameters file and recycle the password I had set before.  The appropriate command for that is:
```
python web2py.py -port 80 -a password
```
If you plan to secure web2py using SSL connections, do this for port 443 as well.

## Set up SSL certs ##

You only need this part if you're going to put web2py behind SSL.

Create SSL cert files and store them in %APACHE%\conf.  There are plenty of howtos on this, especially for self-signed certs, which is the way to go if you're not exposing LMS to anyone outside your network.  Just Google 'howto ssl self-sign'; you'll find it.

I will say this:  If you get errors about openssl.cnf, set an environment variable called OPENSSL\_CONF containing the path to the openssl.cnf file, which contains openssl's settings and configuration for running commands.  Apache with mod\_ssl stores this in %APACHE%\conf.

## Postgres configuration ##

If you have no previous experience in administering a Postgres database, I highly recommend the pgadmin GUI tool.  It installs with Postgres on Windows.  I don't know about Linux, though.

Create a login account that you'll use to access your database.  I called mine libuser.  Then create a new database with default settings, and change the owner to the account you just created.

Change web2py's db.py file to point to the new postgres database:
```
db=DAL('postgres://libuser:pswd@localhost/lmsweb')
```
The above connection string would point to a database called lmsweb hosted on localhost, with login libuser and password pswd.

After the first connection (to create the db tables and everything else), you might want to switch your connection setting to another user account with more limited privileges.  This would reduce the chance of screwy SQL messing up your database.

## Set up Apache ##

Now the fun part:  the Apache config file.

Web2py is designed to want to be hosted at the root of a virtual host.  The web2py manual explains (or attempts to explain) how to fool web2py about this using routes and URL rewrites, but I won't get into that here.

If you don't mind having a virtual host configured with web2py at its root, here's a sample config that works in that model:
```
<VirtualHost *:80>
	ServerName localhost
	ServerAdmin email@local
	DocumentRoot %WEB2PY%/applications/
	WSGIScriptAlias / %WEB2PY%/wsgihandler.py

	# static files do not need WSGI
	<LocationMatch "ˆ(/[\w_]*/static/.*)">
		Order Allow,Deny
		Allow from all
	</LocationMatch> 
        
        # everything else goes to web2py via wsgi
	<Location "/">
		Order deny,allow
		Allow from all
	</Location>
</VirtualHost>
```
This works for any OS, since Apache configs use only forward slashes.  Replace %WEB2PY% with wherever you've got web2py installed at.  Note that this only sets up port 80 and not https.

If you plan to secure the admin interface behind SSL, you'll want to require SSL on it by putting this before <Location "/">:
```
<Location "/admin">
 SSLRequireSSL
</Location>
```
Then add a second virtual host with the SSL configuration directives.  The web2py manual has recipes for that, too, which I omit here.

And that's it!  At this point, using these steps, I could access web2py on http://web2py.localhost/.  If you have problems using this config, please consult the web2py manual.