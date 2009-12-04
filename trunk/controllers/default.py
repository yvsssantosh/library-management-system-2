# coding: utf8

# If you want to enable authentication, uncomment lines with @auth decorator functions. 
import re

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    return dict(message=T('Welcome to the Library Management System.'))
    
#@auth.requires_login()
def addoredit():
    """
    allows adding new books
    """
    if request.args:
        form = SQLFORM(db.books, db.books[request.args[0]], showid=False)
    else:
        form = SQLFORM(db.books)
    if form.accepts(request.vars, session):
        if request.args:
            redirect(URL(r=request, f="show", args=request.args[0]))
        else:
            response.flash = 'Book saved'
    elif form.errors:
        response.flash = 'Form has errors'
    return dict(form=form)
    
#@auth.requires_login()
def delete():
    if len(request.args) and request.args[0]:
        form = FORM('Are you sure you want to delete this book?',
            INPUT(_name='certain', _type='checkbox'),
            INPUT(_type='submit', _value='OK'))
        if form.accepts(request.vars, session):
            if form.vars.certain:
                del db.books[request.args[0]]
                redirect(URL(r=request, f='kwdsearch'))
            else:
                redirect(URL(r=request, f='show', args=request.args[0]))
        elif form.errors:
            redirect(URL(r=request, f='show', args=request.args[0]))
        return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

def get_terms(search_string):
    regex = re.compile(r'(-?"(?:[a-zA-Z]+(?![0-9]+)|[0-9]+)(?: (?:(?:[a-zA-Z]+(?![0-9]+))|(?:[0-9]+))+)+")')
    term_list1 = regex.split(search_string)
    terms = []
    for term in term_list1:
        if (term.startswith('-"') or term.startswith('"')):
            if term.startswith('-'):
                terms.append(('exclude', term.strip('-"')))
            else:
                terms.append(('include', term.strip('"')))
        else:
            term = term.strip(' ').split(' ')
            for t in term:
                if t.startswith('-'):
                    terms.append(('exclude', t.strip('-')))
                else:
                    terms.append(('include', t))
    return terms

COLUMN_NAMES={'ISBN': 'isbn', 'Author': 'author', 'Title': 'title', 'Illustrator': 'illustrator', 'Series': 'series', 'Place in Series': 'place', 'Publisher': 'publisher', 'Genre': 'genre', 'Classification': 'classification', 'Age Level': 'age_level', 'Copyright': 'copyright', 'Edition': 'edition', 'No. of Copies': 'num_copies', 'Awards': 'awards', 'Language': 'language', 'Condition': 'condition', 'Signed': 'signed', 'Antique': 'antique', 'Comments': 'comments'}
COLUMN_AVAIL=['All', 'ISBN', 'Author', 'Title', 'Illustrator', 'Series', 'Place in Series', 'Publisher', 'Genre', 'Classification', 'Age Level', 'Copyright', 'Edition', 'No. of Copies', 'Awards', 'Language', 'Condition', 'Signed', 'Antique', 'Comments']

#uncomment this line to require login to view books
#@auth.requires_login()
def show():
    if request.args:
        try:
            book = db.books[request.args[0]]
            return dict(book=book, cols=COLUMN_NAMES, names=COLUMN_AVAIL[1:])
        except:
            raise HTTP(404, "Book with id %d not available!" % request.args[0])
    else:
        raise HTTP(500, "Malformed URL!")

#uncomment this line to require login to search books by keyword
#@auth.requires_login()
def kwdsearch():
    """
    performs a keyword search
    """
    if len(request.args):
        if request.args[0] == 'new':
            session.keywords = ''
            redirect(URL(r=request, f='kwdsearch'))
    response.view = "%s/search.%s" % (request.controller, request.extension)
    form = FORM(TABLE(TR(TD('Keyword Search:  ', INPUT(_name='keywords', requires=IS_NOT_EMPTY()))),
        TR(TD("Columns to display", BR(), SELECT(COLUMN_AVAIL[:-1], _name='columns', _multiple=True, value='All', requires=[IS_IN_SET(COLUMN_AVAIL[:-1], multiple=True), IS_NOT_EMPTY()]))),
        TR(INPUT(_type='submit', _value='Search'))))
    results = None
    terms=None
    query=None
    columns=None
    if session.keywords:
        form.vars.keywords = session.keywords
    if form.accepts(request.vars, session, keepvalues=True):
        terms = get_terms(form.vars.keywords)
        session.keywords = form.vars.keywords
        for t in range(0,len(terms)):
            if t == 0:
                if terms[t][0] == 'exclude':
                    query = (~(db.books.author.like("%" + terms[t][1] + "%")) & ~(db.books.title.like("%" + terms[t][1] + "%")) & ~(db.books.series.like("%" + terms[t][1] + "%")))
                else:
                    query = ((db.books.author.like("%" + terms[t][1] + "%")) | (db.books.title.like("%" + terms[t][1] + "%")) | (db.books.series.like("%" + terms[t][1] + "%")))
            else:
                if terms[t][0] == 'exclude':
                    query &= (~(db.books.author.like("%" + terms[t][1] + "%")) & ~(db.books.title.like("%" + terms[t][1] + "%")) & ~(db.books.series.like("%" + terms[t][1] + "%")))
                else:
                    query &= ((db.books.author.like("%" + terms[t][1] + "%")) | (db.books.title.like("%" + terms[t][1] + "%")) | (db.books.series.like("%" + terms[t][1] + "%")))
            results = db(query).select()
            if len(form.vars.columns) == 0:
                form.vars.columns = 'All'
            if 'All' in form.vars.columns or len(form.vars.columns):
                columns = COLUMN_AVAIL[1:-1]
            else:
                columns = form.vars.columns
    elif form.errors:
        response.flash='Errors were found that require correction!'
    return dict(form=form, results=results, columns=columns, names=COLUMN_NAMES)

#uncomment this line to require login to search books by field
#@auth.requires_login()    
def advsearch():
    response.view = "%s/search.%s" % (request.controller, request.extension)
    return dict(form="Sorry, this function has not yet been implemented.", results=None)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
