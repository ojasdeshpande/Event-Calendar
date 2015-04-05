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
    return dict(form=form,curr_user = session.curr_user)

def error():
    return dict()

# all events added by the user logged in
def private_event():
    if session.curr_user==None:
        redirect('login')
    rows=db(db.t_events.owner==session.curr_user).select()
    return dict(rows=rows,curr_user = session.curr_user)

# all events is of a particular department and user is of that department
# this fucntion is verified
def department_event():
    if session.curr_user==None:
        redirect('login')
    rowid = []
    if session.curr_type=="student" or session.curr_type=="special_user":
        strin = session.curr_dept
    elif session.curr_type=="faculty":
        strin = session.curr_dept + "_faculty"
    allrows = db(db.t_events.owner!="").select() # this selects all rows
    for r in allrows:
        visible_to = r.f_visible
        ln = len(visible_to)
        st = ""
        owner = r.id
        for i in range(0,ln):
            if(visible_to[i]!=','):
                st = st + visible_to[i]
            if(st==strin and i==ln-1):
                if (not rowid or rowid[-1]!=r.id):  
                    rowid.append(r.id)
            elif(visible_to[i]==','):
                if(st==strin):
                    if (not rowid or rowid[-1]!=r.id):  
                        rowid.append(r.id)
                st = ""
    #response.flash = len(rowid)
    return dict(rows=rowid,curr_user = session.curr_user)

# only gensec of a hostel can add this type of event and only students can see it
# this function has been verified
def hostel_event():
    if session.curr_user==None:
        redirect('login')
    rowid = []
    strin = session.curr_hostel
    if session.curr_type=="student" or session.curr_type=="special_user":
        allrows = db(db.t_events.owner!="").select() # this selects all rows
        for r in allrows:
            visible_to = r.f_visible
            ln = len(visible_to)
            st = ""
            owner = r.id
            for i in range(0,ln):
                if(visible_to[i]!=','):
                    st = st + visible_to[i]
                if(st==strin and i==ln-1):
                    if (not rowid or rowid[-1]!=r.id):  
                        rowid.append(r.id)
                elif(visible_to[i]==','):
                    if(st==strin):
                        if (not rowid or rowid[-1]!=r.id):  
                            rowid.append(r.id)
                    st = ""
    return dict(rows=rowid,curr_user = session.curr_user)

def all():
    if session.curr_user==None:
        redirect('login')
    rows3 = db(db.t_events.owner==session.curr_user).select() # this takes care of all the private events
    if session.curr_type == "student":
        allrows = db(db.t_events.owner!="").select() # this selects all rows
        for r in allrows:
            visible_to = r.f_visible
            ln = len(visible_to)
            st = ""
            for i in range(0,ln):
                if(visible_to[i]!=','):
                    st = st + visible_to[i]
                if((st==session.curr_user or st=="stud" or st==session.curr_dept or st==session.curr_hostel) and i==(ln-1)):
                    arow = db(db.t_events.id==r.id).select()
                    rows3 = arow | rows3
                elif(visible_to[i]==','):
                    if(st==session.curr_user or st=="stud" or st==session.curr_dept or st==session.curr_hostel):
                        arow = db(db.t_events.id==r.id).select()
                        rows3 = arow | rows3
                    st = ""
    if session.curr_type == "faculty":
        strin = session.curr_dept + "_faculty"
        allrows = db(db.t_events.user_type=="faculty").select() # this selects all rows
        for r in allrows:
            visible_to = r.f_visible
            ln = len(visible_to)
            st = ""
            for i in range(0,ln):
                if(visible_to[i]!=','):
                    st = st + visible_to[i]
                if((st==strin or st=="faculty" or st==session.curr_user) and (i==ln-1)):
                    arow = db(db.t_events.id==r.id).select()
                    rows3 = arow | rows3
                elif(visible_to[i]==','):
                    if(st==strin or st=="faculty" or st==session.curr_user):
                        arow = db(db.t_events.id==r.id).select()
                        rows3 = arow | rows3
                    st = ""
    return dict(rows=rows3,curr_user = session.curr_user) # using | will remove all the duplicates

#this funtion is verified
def invites():
    if session.curr_user==None:
        redirect('login')
    rowid = []
    if session.curr_type == "student":
        allrows = db(db.t_events.owner!="").select() # this selects all rows
        for r in allrows:
            visible_to = r.f_visible
            ln = len(visible_to)
            st = ""
            owner = r.owner
            for i in range(0,ln):
                if(visible_to[i]!=','):
                    st = st + visible_to[i]
                if((st==session.curr_user or st=="stud" or st==session.curr_dept or st==session.curr_hostel) and i==(ln-1)):
                    if (not rowid or rowid[-1]!=r.id):  
                        rowid.append(r.id)
                elif(visible_to[i]==','):
                    if(st==session.curr_user or st=="stud" or st==session.curr_dept or st==session.curr_hostel):
                        if (not rowid or rowid[-1]!=r.id):  
                            rowid.append(r.id)
                    st = ""
    if session.curr_type == "faculty":
        strin = session.curr_dept + "_faculty"
        allrows = db(db.t_events.user_type=="faculty").select() # this selects all rows
        for r in allrows:
            visible_to = r.f_visible
            ln = len(visible_to)
            st = ""
            owner = r.id
            for i in range(0,ln):
                if(visible_to[i]!=','):
                    st = st + visible_to[i]
                if(st==strin or st=="faculty" or st==session.curr_user and i==ln-1):
                    if (not rowid or rowid[-1]!=r.id):  
                        rowid.append(r.id)
                elif(visible_to[i]==','):
                    if(st==strin or st=="faculty" or st==session.curr_user):
                        if (not rowid or rowid[-1]!=r.id):  
                            rowid.append(r.id)
                    st = ""
    #response.flash = len(rowid)
    return dict(rows=rowid,curr_user = session.curr_user) # using | will remove all the duplicates

def create_event():
    event_form = SQLFORM.factory(Field('start_time','datetime'),
                               Field('end_time','datetime'),
                               Field('location','string'),
                               Field('description','text'),
                               Field('visibility')).process()
    
    
    if request.vars.start_time and request.vars.end_time and request.vars.visibility:
        if session.curr_type=='faculty':
            user_list=[]
            user_list=request.vars.visibility.split(',')
          #  response.flash = user_list
            dept = ""
            for row in db((db.user.webmail_id==session.curr_user)).select():
                dept = row.department
            for u in user_list:
                flag=0
                response.flash = u
                if u!="stud" and u!="faculty" and u!=(dept+"_faculty") and db((db.user.webmail_id==u)).isempty():
                    flag=1
                    break
            if flag==1:
                response.flash = 'Invalid user in list'
            else:
                db.t_events.insert(owner=session.curr_user,f_start_time=request.vars.start_time,f_end_time=request.vars.end_time,f_location=request.vars.location,f_visible=request.vars.visibility)
                email_id = ""
                for row in db((db.user.webmail_id==session.curr_user)).select():
                    email_id = row.email
                x = mail.send(to=[email_id],
                subject='Event created',
                message= "event created"
            )

            if x == True:
                response.flash = 'email sent sucessfully.'
            else:
                response.flash = 'fail to send email sorry!'
        elif session.curr_type=='special_user':
            user_list=[]
            user_list=request.vars.visibility.split()
            flag=0
            l = []
            rows = db((db.t_permissions.webmail==sessions.curr_user)).select()
            for r in rows:
                l.append(r.permissions)
            nl=[]
            nl = l[0].split(',')
            for u in user_list:
                response.flash = u
                flag=1
                for i in nl:
                    if u==i:
                        flag=0
                if flag==0:
                    continue
                if db((db.user.webmail_id==u)).isempty() :
                    flag=1
                    break
            if flag==1:
                response.flash = 'Invalid user in list'
            else:
                db.t_events.insert(owner=session.curr_user,f_start_time=request.vars.start_time,f_end_time=request.vars.end_time,f_location=request.vars.location,f_visible=request.vars.visibility)
        elif session.curr_type=='student':
            user_list=[]
            user_list=request.vars.visibility.split()
            for u in user_list:
                flag=0
                response.flash = u
                if db((db.user.webmail_id==u)).isempty():
                    flag=1
                    break
            if flag==1:
                response.flash = 'Invalid user in list'
            else:
                db.t_events.insert(owner=session.curr_user,f_start_time=request.vars.start_time,f_end_time=request.vars.end_time,f_location=request.vars.location,f_visible=request.vars.visibility)
                email_id = ""
                for row in db((db.user.webmail_id==session.curr_user)).select():
                    email_id = row.email
                if mail:
                    x = mail.send(to=[email_id],
                    subject='Event created',
                    message= "event created"
                    )
                    if x == True:
                        response.flash = 'email sent sucessfully.'
                    else:
                        response.flash = 'fail to send email sorry!'
                else:
                    response.flash = 'mail not set'
    else:
        response.flash = 'Enter event details'
    return locals()

def logout():
    session.curr_user = None
    session.curr_day = None
    redirect('login')
