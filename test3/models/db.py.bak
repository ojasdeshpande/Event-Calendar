# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()


########################################
db.define_table('user',
    Field('webmail_id', type='string',
          label=T('Webmail')),
    Field('user_type',type='string',
          label=T('User Type')),
    Field('department', type='string',
          label=T('Department')),
    Field('hostel', type='string',default=None,
          label=T('Hostel')),
    Field('email', type='string',
          label=T('Alternate Email')),
    Field('password', type='password',
          readable=False,
          label=T('Password')),
   Field('year',type='integer',default=None,
         label=T('Year')),
    )


db.user.webmail_id.requires = (IS_NOT_EMPTY(error_message='This field cannot be empty'),IS_NOT_IN_DB(db, db.user.webmail_id))
db.user.user_type.requires = IS_NOT_EMPTY(error_message='This field cannot be empty')
db.user.department.requires = IS_NOT_EMPTY(error_message='This field cannot be empty')
db.user.password.requires = CRYPT(key='sha512:d7c965e8-0685-477a-baae-087e7372943f')
db.user.email.requires = (IS_EMAIL(error_message="This is an invalid email"),
                               IS_NOT_IN_DB(db, db.user.email))
