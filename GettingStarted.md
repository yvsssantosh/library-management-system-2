# Getting Started #

So, you've downloaded the Library Management System and installed it into web2py.  Now, what do you do with it? :)

## Using the LMS ##

The left-hand navigation menu should be pretty self-explanatory, and it exposes the top-level functionality of the LMS:
  * Index leads you back to the main page of the LMS, where you start out.
  * Add New Books lets you do just that.
  * The Search menu entry itself doesn't go anywhere, but the two sub items underneath point to the two search modules of the LMS:  Keyword searching or Advanced search.  Advanced mode is not currently implemented, sadly.
  * Admin takes you into the Application Admin (or Appadmin) area of the LMS, where you can more directly mess around with stuff in the database, as well as view the current state of LMS.  Currently only a user logged in to web2py's Admin site can access LMS Appadmin.

Within Appadmin, the menu changes:
  * Database exposes CRUD functions for every table in the underlying LMS database.
  * State shows the current state of LMS, including all internal system variables (see the web2py manual for details on what these mean).
  * Index takes you back to the LMS main index.

## Database settings ##

When you first install the Library Management System, its default settings will create a sqlite database.  If you have a large book collection to manage (more than a few hundred), you'll want to go with a full-scale database server.  MySQL or Postgres should cover most anybody's needs, but web2py also supports Firebird, Microsoft SQL, and Oracle.

## User authentication and security ##

If you plan to set this up for a multi-user environment and you expect to have access control, web2py provides a convenient authentication and authorization framework.  The commented lines near the top of db.py that start with 'auth' lay the groundwork for implementing authentication in LMS.  Just uncomment those lines, and the auth framework will do the rest, including creating the necessary tables in the database.  This also exposes those tables to Appadmin.

Once that's done, look in default.py, the controller file for LMS.  You'll find auth decorators (method calls starting with @auth) all over, which link the various actions of the controllers to authentication requirements.  They're commented out right now to stop them from requiring login to use LMS.  Just uncomment the decorators for whatever functions you want to secure.  But before you do any of that, make sure you've got at least one account created already.  You can create accounts from the Appadmin interface for the tables db.auth\_user, db.auth\_group, and db.auth\_membership.  A simpler interface for account creation is planned for the future.

## Appearance ##

Feel free to play with what the LMS looks like.  Everything in terms of appearance is defined via CSS styles in library.css (listed under 'Static' in the admin view).  If you don't mind messing with Python and HTML, you can restructure LMS's basic appearance by changing layout.html under the Views.  This is the main layout for all LMS pages.