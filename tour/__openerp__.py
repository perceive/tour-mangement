# -*- encoding: utf-8 -*-
##############################################################################

##############################################################################

{
    'name': 'Tour',
    'version': '2.0',
    'category': 'Tour',
    'description': """

    """,
    'summary': 'Tour',
    'author': 'Bhumika Shrimali ',
    'website': '',
    'depends': ['mail',
        'base_location','crm','hr','account','sale'],
    'data': ['wizard/tour_make_sale_view.xml',
             'tour_seq.xml',
             'tour_email_template.xml',
             'tour_view.xml',
             'report_saleorder_custom.xml',
             'sale_report.xml',
             'views/tour_query_report.xml',
             'crm_lead_view.xml',
 'report.xml',
    ],    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
    'images': [],
}
