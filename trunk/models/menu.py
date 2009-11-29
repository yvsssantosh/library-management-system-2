# coding: utf8

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = T('Library Management System')
response.subtitle = T('customize me!')

##########################################
## this is the authentication menu
## remove if not necessary
##########################################

if 'auth' in globals():
    if not auth.is_logged_in():
       response.menu_auth = [
           [T('Login'), False, auth.settings.login_url, []],
           ]
    else:
        response.menu_auth = [
            ['User: '+auth.user.first_name,False,None,
             [
                    [T('Logout'), False, 
                     URL(request.application,'default','user/logout')],
                    [T('Change Password'), False,
                     URL(request.application,'default','user/change_password')]]
             ],
            ]

##########################################
## this is the main application menu
## add/remove items as required
##########################################

response.menu = [
    [T('Index'), False, 
     URL(request.application,'default','index'), []],
    [T('Add New Books'), False,
     URL(request.application, 'default','addoredit'), []],
    [T('Search'), False,
     '#', [
      [T('Keyword'), False,
       URL(request.application, 'default', 'kwdsearch'), []],
      [T('Advanced'), False,
       URL(request.application, 'default', 'advsearch'), []],
     ]],
    ]


##########################################
## this is here to provide shortcuts
## during development. remove in production 
##########################################

response.menu_edit=[
  [T('Edit'), False, URL('admin', 'default', 'design/%s' % request.application),
   [
            [T('Controller'), False, 
             URL('admin', 'default', 'edit/%s/controllers/default.py' \
                     % request.application)],
            [T('View'), False, 
             URL('admin', 'default', 'edit/%s/views/%s' \
                     % (request.application,response.view))],
            [T('Layout'), False, 
             URL('admin', 'default', 'edit/%s/views/layout.html' \
                     % request.application)],
            [T('Stylesheet'), False, 
             URL('admin', 'default', 'edit/%s/static/base.css' \
                     % request.application)],
            [T('DB Model'), False, 
             URL('admin', 'default', 'edit/%s/models/db.py' \
                     % request.application)],
            [T('Menu Model'), False, 
             URL('admin', 'default', 'edit/%s/models/menu.py' \
                     % request.application)],
            [T('Database'), False, 
             URL(request.application, 'appadmin', 'index')],
            ]
   ],
  ]
