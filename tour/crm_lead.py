from openerp import fields, models, api, _

class crm_lead(models.Model):

    _inherit = 'crm.lead'

    # name = fields.Char('Query Name',readonly=True)
    tour_type= fields.Selection([('domestic','Domestic'),('international','International')],'Tour type', required=True)
#     ex_vendor_id=fields.Many2one('tour.hotel.vender', 'Excursion Vendor')
#     tc_vendor_id=fields.Many2one('tour.hotel.vender', 'Ticket Vendor')
#     tr_vendor_id=fields.Many2one('tour.hotel.vender', ' Transportation Vendor')
#     location_id = fields.Many2many('res.better.zip','idt', 'ide',string='Destination',required=True)
    adult_no = fields.Integer('Number of Adult')
    cwb_no = fields.Integer('CWB')
    cw_no = fields.Integer('CNB')
    to_date = fields.Date('Start Date',required=True)
    extra_no = fields.Integer('Extra Adult')
    infants = fields.Integer('Number of infants')
    hotel = fields.Boolean('Hotel')
    visa_p = fields.Boolean('Visa')
    passport=fields.Boolean('Passport')
    ticket = fields.Boolean('Ticket')
    trnsport = fields.Boolean('Transportation')
    extraction = fields.Boolean('Excursion')
    insuracne = fields.Boolean('Insurance')
#     all_ids=fields.One2many('tour.hotel.all', 'tour_id', 'Hotel/Vendor/Invoice Detail', )
    vendor = fields.Boolean('Hotel Vendor')
    direct = fields.Boolean('Direct Hotel')
#     hotel_id = fields.Many2one(
#         'tour.hotel',
#         'Hotel',
#     )
#
#     visa_id = fields.Many2one(
#         'tour.visa',
#         'Visa',
#     )
#
#     # transport_ids = fields.One2many(
#     #      'tour.transport','query',
#     #      'Transport',
#     #  )
#
#     sale_id = fields.Many2one(
#         'sale.order',
#         'Sale Order',
#     )
#
# #     ticket_id = fields.One2many(
# #         'tour.ticket',
# #         'Ticket',
# #     )
# #     insurance_id = fields.Many2one(
# #         'tour.insurance',
# #         'Insurance',
# #     )
#     passport_id = fields.Many2one(
#         'tour.passport',
#         'Passport',
#     )
#     vender_ids=fields.Many2many('tour.hotel.vender', 'vendor_test_rel', 'hote_id', 'wizard_id',string='Vendor Detail')
#    # vender_ids':fields.many2many('tour.hotel.vender','vendor_rel', 'user_id', 'wizard_id',string='Vendor Detail')
#     invoice=fields.Many2many('account.invoice','test_rel','test_2id','id2_test','Last invoice')
#     #'invoice': fields.many2many('account.invoice', 'account_user_rel', 'user_id', 'wizard_id', 'Last invoice'),
#    # extraction_id = fields.One2many('tour.extraction', 'query',string='E,xcursion')
    emp_id = fields.Many2one('hr.employee',string='Employee')
#
    days= fields.Integer('No of Night',required=True)
#     line_ids=fields.One2many('tour.query.line', 'query', 'Excursion', )
#     ticket_emp_id = fields.Many2one('hr.employee',string='Ticket Employee')
#     ticket_ids=fields.One2many('tour.ticket', 'query', 'Ticket Detail', )
#     state =fields.Selection([
#             ('draft', 'Not Confirmed'),
#             ('done', 'Confirmed'),
#             ('cancel','Cancel') ])



