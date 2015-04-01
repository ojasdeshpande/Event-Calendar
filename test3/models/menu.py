response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%s <%s>' % (settings.author, settings.author_email)
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
    (T('Index'),URL('index'),URL('index'),[]),
    (T('Create'),URL('appointment_create'),URL('appointment_create'),[]),
    (T('Select'),URL('appointment_select'),URL('appointment_select'),[]),
    (T('Map'),URL('mymap'),URL('mymap'),[]),
    (T('Calendar'),URL('mycal'),URL('mycal'),[]),
    
]
