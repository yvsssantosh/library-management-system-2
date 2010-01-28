# coding: utf8

# If you want to enable authentication, uncomment lines with @auth decorator functions. 
import re
import amazonproduct

_aws_id = ''
_aws_key = ''
_aws_ns = {'aws': 'http://webservices.amazon.com/AWSECommerceService/2009-10-01'}

_aws_api = amazonproduct.API(_aws_id, _aws_key, locale='us')

def book_search(kwds):
    if len(kwds):
        terms = []
        for k in kwds:
            terms.append(k + ':' + kwds[k])
        pwrsrch = ' and '.join(terms)
        nodes = _aws_api.item_search('Books', ResponseGroup='ItemAttributes', Power=pwrsrch)
        books = []
        for book in nodes.xpath('//aws:Items/aws:Item', namespaces=_aws_ns):
            try:
                books.append((book.ItemAttributes.Author, book.ItemAttributes.Title, "%010d" % book.ItemAttributes.ISBN.pyval))
            except:
                books.append((book.ItemAttributes.Author, book.ItemAttributes.Title, 'ASIN:%s' % book.ASIN))
        return books
    else:
        return None

def item_lookup(isbn):
    if isbn.startswith('ASIN:'):
        asin = isbn.split(':')[1]
        node = _aws_api.item_lookup(asin, ResponseGroup='ItemAttributes')
    else:
        newisbn = ''.join(isbn.split('-'))
        node = _aws_api.item_lookup(newisbn, IdType='ISBN', SearchIndex='Books', ResponseGroup='ItemAttributes')
    nodeatts = node.xpath('//aws:ItemAttributes', namespaces=_aws_ns)
    book = {'author': nodeatts[0].Author}
    book['title'] = nodeatts[0].Title
    try:
        book['isbn'] = nodeatts[0].ISBN
    except:
        book['isbn'] = ''
    book['publisher'] = nodeatts[0].Publisher
    book['copyright'] = nodeatts[0].PublicationDate.pyval.split('-')[0]
    return book

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
        form = SQLFORM(db.books, db.books[request.args[0]], showid=False, submit_button='Save')
        isbnform=None
        atform=None
        booklist=None
    else:
        kwds={'nothin': 'nothin'}
        form = SQLFORM(db.books, submit_button='Add')
        isbnform = FORM(TABLE(TR('Enter ISBN:',
            INPUT(_name='isbn', _type='text'),
            INPUT(_type='submit', _value='Lookup'))), _name='isbnform')
        atform = FORM(TABLE(TR('Author:', INPUT(_name='author', _type='text')),
            TR('Title:', INPUT(_name='title', _type='text')),
            TR('Copyright:', INPUT(_name='pubdate', _type='text')),
            TR(TD(INPUT(_type='submit', _value='Search'), _colspan=2))))
        booklist=None
        if isbnform.accepts(request.vars, session, formname='isbnform'):
            book = item_lookup(isbnform.vars.isbn)
            form.vars.isbn = book['isbn']
            form.vars.author = book['author']
            form.vars.title = book['title']
            form.vars.publisher = book['publisher']
            form.vars.copyright = book['copyright']
        if atform.accepts(request.vars, session, formname='atform'):
            kwds = {}
            if atform.vars.author:
                kwds['author'] = atform.vars.author
            if atform.vars.title:
                kwds['title'] = atform.vars.title
            if atform.vars.pubdate:
                kwds['pubdate'] = atform.vars.pubdate
            booklist = book_search(kwds)
    if form.accepts(request.vars, session):
        if request.args:
            redirect(URL(r=request, f="show", args=request.args[0]))
        else:
            response.flash = 'Book saved'
    elif form.errors:
        response.flash = 'Form has errors'
    return dict(form=form, isbnform=isbnform, atform=atform, booklist=booklist)
    
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
            loans = book.loans.select()
            return dict(book=book, loans=loans, cols=COLUMN_NAMES, names=COLUMN_AVAIL[1:])
        except:
            raise HTTP(404, "Book with id %d not available!" % request.args[0])
    else:
        raise HTTP(500, "Malformed URL!")
        
def addeditloan():
    if request.args:
        book = db.books[request.args[0]]
        if len(request.args) > 1:
            loan = db.loans[request.args[1]]
            form = SQLFORM(db.loans, loan, fields=['name', 'lndate', 'comments'], showid=False, submit_button='Save')
            return dict(form=form, bkid=book.id)
        else:
            form = SQLFORM(db.loans, fields=['name', 'lndate', 'comments'], submit_button='Add')
            form.vars.id_books = book.id
        if form.accepts(request.vars, session):
            redirect(URL(r=request, f="show", args=request.args[0]))
        elif form.errors:
            response.flash = 'Form has errors'
        return dict(form=form, bkid=book.id)
    else:
        raise HTTP(500, "Malformed URL!")
        
def delloan():
    if len(request.args) and request.args[0]:
        book_id = db.loans[request.args[0]].id_books
        form = FORM('Are you sure you want to delete this loan?',
            INPUT(_name='certain', _type='checkbox'),
            INPUT(_type='submit', _value='OK'))
        if form.accepts(request.vars, session):
            if form.vars.certain:
                del db.loans[request.args[0]]
            redirect(URL(r=request, f='show', args=book_id))
        elif form.errors:
            redirect(URL(r=request, f='show', args=book_id))
        return dict(form=form)

kwdform = FORM(TABLE(TR(TD('Keyword Search:  ', INPUT(_name='keywords', requires=IS_NOT_EMPTY()))),
        TR(TD("Columns to display", BR(), SELECT(COLUMN_AVAIL[:-1], _name='columns', _multiple=True, value='All', requires=[IS_IN_SET(COLUMN_AVAIL[:-1], multiple=True), IS_NOT_EMPTY()]))),
        TR(INPUT(_type='submit', _value='Search'))))

advform = FORM(TABLE(
   TR('Author: ', INPUT(_name='author')),
   TR('Title: ', INPUT(_name='title')),
   TR('Illustrator: ', INPUT(_name='illus')),
   TR(TD("Columns to display", BR(), SELECT(COLUMN_AVAIL[:-1], _name='columns', _multiple=True, value='All', requires=[IS_IN_SET(COLUMN_AVAIL[:-1], multiple=True), IS_NOT_EMPTY()]))),
   TR(INPUT(_type='submit', _value='Search')),
))

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
    form = kwdform
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
    form=advform
    return dict(form=form, results=None)

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
