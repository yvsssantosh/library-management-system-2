# coding: utf8

#db = DAL('postgres://libuser:pswd@localhost/booksdb') # sample connection string for postgres
db = DAL('sqlite://storage.sqlite')       # use SQLite or other DB

from gluon.tools import *
# The below lines are commented out to disable authentication completely.  If you want to turn authentication on,
# just uncomment them, and then uncomment @auth decorators in appadmin.py and default.py as needed.
#auth=Auth(globals(),db)                      # authentication/authorization
#auth.settings.hmac_key='sha512:32b6c31c-d643-408f-8415-e7e07efb91e0'
#auth.settings.actions_disabled.append('register') # block user registration, only admins can add new users
#auth.settings.actions_disabled.append('profile')  # block access to profiles, as they are not required
#auth.settings.actions_disabled.append('retrieve_username') # block access to username retrieval
#auth.settings.actions_disabled.append('retrieve_password') # block access to password retrieval
#auth_table =db.define_table(auth.settings.table_user_name, # custom user table
#    Field('first_name', length=128, default=''),
#    Field('last_name', length=128, default=''),
#    Field('username', length=128, default=''),
#    Field('email', unique=True, length=128, default=''),
#    Field('password', 'password', length=256, default='', readable=False, label='Password'),
#    Field('registration_key', length=128, readable=False, writable=False))
#auth_table.first_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty) #validators req'd by web2py
#auth_table.last_name.requires = IS_NOT_EMPTY(error_message=auth.messages.is_empty)
#auth_table.username.requires = IS_NOT_IN_DB(db, auth_table.username)
#auth_table.password.requires = [IS_STRONG(), CRYPT()]
#auth_table.email.requires = [IS_EMAIL(error_message=auth.messages.invalid_email), IS_NOT_IN_DB(db, auth_table.email)]
#auth.settings.table_user = auth_table # set above table definition as user table for db
#auth.define_tables()                         # creates all needed tables
#crud=Crud(globals(),db)                      # for CRUD helpers using auth

# the below are for people that use internal mail servers and want to set up email-based auth.
# crud.settings.auth=auth                      # enforces authorization on crud
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = \
#  'Click on the link http://.../user/verify_email/%(key)s to verify your email'
## more options discussed in gluon/tools.py
#########################################################################

# options for <select> fields
GENRE_CHOICES = (
    'Sci-Fi/Fantasy',
    'Textbook',
    'Religious',
    'Self-Help',
    'Comic',
    'Poetry',
    'Action/Adventure',
    'General',
    'Writing Reference',
    'General Reference',
    'Cookbook'
)

CLASSIF_CHOICES = [
    'Adult',
    'Young Adult',
    'Child - Chapter',
    'Child - Picture']
    
AGELVL_CHOICES = [
    'Adult',
    'Young Adult',
    'Intermediate',
    'Primary']

COND_CHOICES = [
    'Excellent',
    'Good',
    'Fine',
    'Poor']

#table declarations
db.define_table("books",
    Field("isbn", "string", label="ISBN", length=20, default=None),
    Field("author", "string", length=50, notnull=True, default=None),
    Field("title", "string", length=100, notnull=True, default=None),
    Field("illustrator", "string", length=50, default=None),
    Field("series", "string", length=100, default=None),
    Field("place", "integer", label="Place in Series", length=3, default=0),
    Field("publisher", "string", length=30, default=None),
    Field("genre", "string", length=20, notnull=True, default=None, requires=IS_IN_SET(GENRE_CHOICES)),
    Field("classification", "string", notnull=True, default=None, requires=IS_IN_SET(CLASSIF_CHOICES)),
    Field("age_level", "string", notnull=True, default=None, requires=IS_IN_SET(AGELVL_CHOICES)),
    Field("copyright", "integer", length=4, default=None),
    Field("edition", "integer", length=2, default=None),
    Field("num_copies", "integer", label='No. of Copies', notnull=True, default=1),
    Field("awards", "string", length=50, default=None),
    Field("language", "string", length=20, notnull=True, default=None),
    Field("condition", "string", length=10, notnull=True, default=None, requires=IS_IN_SET(COND_CHOICES)),
    Field("signed", "boolean", label='Signed', notnull=True, default=False),
    Field("antique", "boolean", label='Antique', notnull=True, default=False),
    Field("comments", "text", default=None))

from datetime import datetime

db.define_table("loans",
    Field("id_books", db.books),
    Field("name", "string", length=50, notnull=True, default=None),
    Field("lndate", "date", label='Date of Loan:', notnull=True, default=datetime.now()),
    Field("comments", "text", default=None, notnull=False))

# define relation between loans and books
db.loans.id_books.requires=IS_IN_DB(db, 'books.id', '%(author)s %(title)s')
