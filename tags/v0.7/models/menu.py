# coding: utf8

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
#If you're exposing appadmin to administrators only, the below lines are a handy way to make a shortcut to appadmin.
#Uncomment both lines and tab the third line over if you want this.  Otherwise it can stay as is.
#If you don't want to expose appadmin to users at all, just comment the third line.
#if 'auth' in globals():
#    if auth.has_membership(auth.id_group('admin')):
response.menu.append([T('Admin'), False, URL(request.application, 'appadmin', 'index'), []])
