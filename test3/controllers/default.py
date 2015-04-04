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
                               Field('password',type='password'),
                               Field('user_type'),
                               Field('remember_me', 'boolean')).process()
        if request.vars.webmail_id and request.vars.password and request.vars.user_type:
            passw = str(CRYPT(digest_alg='sha512',key='d7c965e8-0685-477a-baae-087e7372943f',salt=False)(request.vars.password)[0])
            failure = db((db.user.webmail_id==request.vars.webmail_id) & (db.user.password==passw) & (db.user.user_type==request.vars.user_type)).isempty()
            if failure == False:
                    session.curr_user = request.vars.webmail_id
                    session.curr_type = request.vars.user_type
                    rows = db(db.user.webmail_id==session.curr_user).select() 
                    session.curr_dept = rows[0].department
                    session.curr_hostel = rows[0].hostel
                    if(request.vars.remember_me):
                        session.curr_day = 1
                    redirect(URL('mycal'))
            else:
                    response.flash = 'Wrong credentials ! '
        else:
            response.flash = 'Enter credentials'
        return locals()

def mycal():
    if session.curr_user==None:
        redirect('login')
    return dict()

#read an event by clicking on it
def read_event():
    if session.curr_user==None:
        redirect('login')
    record = db.t_events(request.args(0)) or redirect(URL('error'))
    form=crud.read(db.t_events,record)
    return dict(form=form)

def error():
    return dict()

# all events added by the user logged in
def private_event():
    if session.curr_user==None:
        redirect('login')
    rows=db(db.t_events.owner==session.curr_user).select()
    return dict(rows=rows)

# all events is of a particular department and user is of that department
def department_event():
    if session.curr_user==None:
        redirect('login')
    rows=db(db.t_events.f_visible==session.curr_dept).select()
    return dict(rows=rows)

# all events of a particular hostel and user is of that hostel
def hostel_event():
    if session.curr_user==None:
        redirect('login')
    rows=db(db.t_events.f_visible==session.curr_hostel).select()
    return dict(rows=rows)

def all():
    if session.curr_user==None:
        redirect('login')
    rows1 =db(db.t_events.owner==session.curr_user).select() # private events
    rows2 = db(db.t_events.f_visible==session.curr_dept).select() # department events
    rows3 = db(db.t_events.f_visible==session.curr_hostel).select() # hostel events
    # if user is student then check for any stud event
    #
    # now we want those events in which user has been specifically added by some other user
    
    return dict(rows=rows1 | rows2 | rows3) # using | will remove all the duplicates

def logout():
    session.curr_user = None
    session.curr_day = None
    redirect('login')
