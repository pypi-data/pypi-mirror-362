***************
Mail Management
***************

Configuration files
===================

mail2ev_evdo.yml
----------------

Content
^^^^^^^

.. mail2ev_evdo.yml-label:
.. code-block:: jinja

 - from: 'bernd.stroehle@gmail.com'
   to:
     - 'bernd.stroehle@kosakya.de'
     - 'bernd.stroehle@gmail.com'
   cc:
     - 'denis.erdem@copitos.de'
   client_id: ''
   client_secret: ''
   tenant_id: ''
   url_authority: 'https://login.microsoftonline.com'
   url_scope: 'https://graph.microsoft.com/.default'
   subject: 'Test Email with Attachment of EcoVadis upload Excel workbook'
   body:
     - 'Please Run the EcoVadis IQ Download with the following Excel Workbook:'
     - '  {}'
   host: 'smtp-mail.outlook.com'
   password: 'BrndStff69!-'
   paths:
     - datetype: 'last'
       d_path:
           app_data: 'key'
           tenant: 'key'
           EV/Dow/EVDO.reg.*.xlsx: 'val'
   sw_attachements: true
   sw_ssl: false
   tls_port: 587
   ssl_port': 465

mail2ev_eviq.yml (jinja2 yml file
---------------------------------

Content
^^^^^^^

.. mail2ev_eviq.yml-label:
.. code-block:: jinja

 - from: 'bernd.stroehle@gmail.com'
   to:
     - 'bernd.stroehle@kosakya.de'
     - 'bernd.stroehle@gmail.com'
   cc:
     - 'denis.erdem@copitos.de'
   client_id: ''
   client_secret: ''
   tenant_id: ''
   url_authority: 'https://login.microsoftonline.com'
   subject: 'Check and Load EcoVadis IQ SRR Workbooks into OmnitTracker'
   body:
     - 'Please check and load the following Excel Workbooks into OmniTracker:'
     - '  EcoVadis IQ Upload Workbook: {}'
     - '  OmniTracker Export Verification Workbook : {}.'
     - '  EcoVadis IQ Upload-Status Workbook: {}'
     - '  EcoVadis IQ Export Workbook: {}'
     - '  mapped EcoVadis IQ Export Workbook: {}'
   host: 'smtp-mail.outlook.com'
   password: 'BrndStff69!-'
   paths:
     - 'datetype': 'last'
       'd_path':
           'app_data': 'key'
           'tenant': 'key'
           'EV/Upl/Dat/EVUP.reg.*.xlsx': 'val'
     - 'datetype': 'last'
       'd_path':
           'app_data': 'key'
           'tenant': 'key'
           'OT/Vfy/OTEX.reg.vfy.*.xlsx': 'val'
     - 'datetype': 'last'
       'd_path':
           'app_data': 'key'
           'tenant': 'key'
           'EV/Dow/EVDO.reg.*.xlsx': 'val'
     - 'datetype': 'last'
       'd_path':
           'app_data': 'key'
           'tenant': 'key'
           'EV/Exp/Eco/EVEX.eco.*.xlsx': 'val'
     - 'datetype': 'last'
       'd_path':
           'app_data': 'key'
           'tenant': 'key'
           'EV/Exp/Umh/EVEX.umh.*.xlsx': 'val'
   sw_attachements: false
   sw_ssl: true
   tls_port: 587
   ssl_port': 465
