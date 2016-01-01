# -*- coding: utf-8 -*-
##############################################################################
##############################################################################

from openerp.osv import osv
from openerp.report import report_sxw

class tour_query_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(tour_query_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_return_or_not':self.get_return_or_not,
            'client_flexible_or_not':self.client_flexible_or_not,
        })
    def get_return_or_not(self, twoway):
        if twoway == True:
            return "Yes"
        else:
            return "No"

    def client_flexible_or_not(self, flexible):
        if flexible == True:
            return "Yes"
        else:
            return "No"

class tour_query_report_template_id(osv.AbstractModel):
    _name = 'report.tour.report_tourquery'
    _inherit = 'report.abstract_report'
    _template = 'tour.report_tourquery'
    _wrapped_report_class = tour_query_report
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
