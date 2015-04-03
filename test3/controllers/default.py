def index():
    redirect(URL('login'))

def login():
    if session.curr_day:
        session.curr_day = session.curr_day + 1
        if session.curr_day <=3:
            redirect(URL('mycal'))
        else:
            session.curr_day = None
            session.curr_user = None
            redirect(URL('login'))
    else:
        form = SQLFORM.factory(Field('webmail_id'),
                               Field('password'),
                               Field('user_type'),
                               Field('remember_me', 'boolean')).process()
        if request.vars.webmail_id and request.vars.password and request.vars.user_type:
            passw = str(CRYPT(digest_alg='sha512',key='d7c965e8-0685-477a-baae-087e7372943f',salt=False)(request.vars.password)[0])
            failure = db((db.user.webmail_id==request.vars.webmail_id) & (db.user.password==passw) & (db.user.user_type==request.vars.user_type)).isempty()
            if failure == False:
                    session.curr_user = request.vars.webmail_id
                    session.curr_type = request.vars.user_type
                    if(request.vars.remember_me):
                        session.curr_day = 1
                    redirect(URL('mycal'))
            else:
                    response.flash = 'Wrong credentials ! '
        else:
            response.flash = 'Enter credentials'
        return locals()

def mycal():
    rows=db(db.t_events.owner==session.curr_user).select()
    return dict(rows=rows)

def read_event():
    record = db.t_events(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_events,record)
    return dict(form=form)

def error():
    return dict()
