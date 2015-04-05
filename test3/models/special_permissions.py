########################################
db.define_table('t_permissions',
    Field('webmail', type='string',
          label=T('Webmail')),
    Field('permissions', type='string',
          label=T('Permissions'))
    )
