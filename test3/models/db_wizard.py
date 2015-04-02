### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


########################################
db.define_table('t_events',
    Field('owner', type='string',
          label=T('Webmail')),
    Field('f_start_time', type='datetime',
          label=T('Start Time')),
    Field('f_end_time', type='datetime',
          label=T('End Time')),
    Field('f_location', type='string',
          label=T('Location')),
    Field('f_desc', type='text',
          represent=lambda x: MARKMIN(x),
          comment='WIKI (markmin)',
          label=T('Event Description')),
    Field('f_visible',type='string',
          label=T('Visible To')),
    )
