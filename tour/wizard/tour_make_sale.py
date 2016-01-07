# -*- coding: utf-8 -*-

#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import workflow


class tour_make_sale(osv.osv_memory):
    """ Make sale order for crm """

    _name = "tour.make.sale"
    _description = "Make sales"

    def _selectPartner(self, cr, uid, context=None):
        """
        This function gets default value for partner_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('tour.query')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.read(cr, uid, [active_id], ['customer_id'], context=context)[0]
        return lead['customer_id'][0] if lead['customer_id'] else False

    def view_init(self, cr, uid, fields_list, context=None):
        return super(tour_make_sale, self).view_init(cr, uid, fields_list, context=context)

    def makeOrder_sale(self, cr, uid, ids, context=None):
        """
        This function  create Quotation on given case.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of crm make sales' ids
        @param context: A standard dictionary for contextual values
        @return: Dictionary value of created sales order.
        """
        # update context: if come from phonecall, default state values can make the quote crash lp:1017353
        context = dict(context or {})

        case_obj = self.pool.get('tour.query')
        sale_obj = self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        data = context and context.get('active_ids', []) or []

        for make in self.browse(cr, uid, ids, context=context):
            partner = make.partner_id
            partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                                                   ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False
            payment_term = partner.property_payment_term and partner.property_payment_term.id or False
            new_ids = []
            for case in case_obj.browse(cr, uid, data, context=context):
                if not partner and case.partner_id:
                    partner = case.partner_id
                    fpos = partner.property_account_position and partner.property_account_position.id or False
                    payment_term = partner.property_payment_term and partner.property_payment_term.id or False
                    partner_addr = partner_obj.address_get(cr, uid, [partner.id],
                                                           ['default', 'invoice', 'delivery', 'contact'])
                    pricelist = partner.property_product_pricelist.id
                if False in partner_addr.values():
                    raise osv.except_osv(_('Insufficient Data!'), _('No address(es) defined for this customer.'))
                line_obj = self.pool.get('sale.order.line')
                vals = {
                    'origin': _('Tour: %s') % str(case.id),
                    'partner_id': partner.id,
                    'pricelist_id': pricelist,
                    'partner_invoice_id': partner_addr['invoice'],
                    'partner_shipping_id': partner_addr['delivery'],
                    'date_order': fields.date.context_today(self, cr, uid, context=context),
                    'fiscal_position': fpos,
                    'payment_term': payment_term,
                    'hotel_id': case.hotel_id,
                    # 'vendor_id':case.vendor_id,

                }
                if partner.id:
                    vals['user_id'] = partner.user_id and partner.user_id.id or uid
                new_id = False
                total_amt = 0.0
                if not case.sale_id:
                    new_id = sale_obj.create(cr, uid, vals, context=context)
                    case_obj.write(cr, uid, [case.id], {'sale_id': new_id})
                    if case.hotel_id:
                        line_obj.create(cr, uid, {
                            'name': 'Hotel Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.hr_amount,

                        }, context=context)
                        total_amt += make.hr_amount
                    if case.transport_ids:
                        line_obj.create(cr, uid, {
                            'name': 'Transport Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.tr_amount,
                            'vendor_id': case.tr_vendor_id.id,
                        }, context=context)
                        total_amt += make.tr_amount
                    if case.visa_id:
                        line_obj.create(cr, uid, {
                            'name': 'Visa Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.v_amount,
                        }, context=context)
                        total_amt += make.v_amount
                    if case.ticket_ids_one:
                        line_obj.create(cr, uid, {
                            'name': 'Ticket  Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.trc_amount,
                            'vendor_id': case.tc_vendor_id.id,
                        }, context=context)
                        total_amt += make.trc_amount
                    if case.ticket_ids_round:
                        line_obj.create(cr, uid, {
                            'name': 'Ticket  Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.trc_amount,
                            'vendor_id': case.tc_vendor_id.id,
                        }, context=context)
                        total_amt += make.trc_amount
                    if case.ticket_ids_multi:
                        line_obj.create(cr, uid, {
                            'name': 'Ticket  Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.trc_amount,
                            'vendor_id': case.tc_vendor_id.id,
                        }, context=context)
                        total_amt += make.trc_amount
                    if make.is_amount:
                        line_obj.create(cr, uid, {
                            'name': 'Insurance Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.is_amount,
                        }, context=context)
                        total_amt += make.is_amount
                    if case.passport_id:
                        line_obj.create(cr, uid, {
                            'name': 'Passport Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.pas_amount,
                        }, context=context)
                        total_amt += make.pas_amount
                    if case.line_ids:
                        line_obj.create(cr, uid, {
                            'name': 'Excursion Exp',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': make.ex_amount,
                            'vendor_id': case.ex_vendor_id.id,
                        }, context=context)
                        total_amt += make.ex_amount
                    if make.margin_amount:
                        mr = 0.0
                        #                         line_obj.create(cr, uid, {
                        #                             'name':'Margin Amount',
                        #                              'order_id': new_id,
                        #                         'product_uom_qty': 1,
                        #                         'price_unit': make.margin_amount
                        #                             }, context=context)
                        if make.absolute:
                            total_amt += make.margin_amount
                            mr = make.margin_amount
                        elif make.percentage:
                            total_amt = total_amt * make.margin_amount / 100
                            # mrtotal_amt*make.margin_amount/100
                        line_obj.create(cr, uid, {
                            'name': 'Margin Amount',
                            'order_id': new_id,
                            'product_uom_qty': 1,
                            'price_unit': mr
                        }, context=context)

                    sale_order = sale_obj.browse(cr, uid, new_id, context=context)
                    self.write(cr, uid, make.id, {'total_amount': total_amt})
                    case_obj.write(cr, uid, [case.id], {'ref': 'sale.order,%s' % new_id})
                    new_ids.append(new_id)
                    message = _("Query has been <b>converted</b> to the quotation <em>%s</em>.") % (sale_order.name)
                    case.message_post(body=message)
                #             if make.close:
                #                 case_obj.case_mark_won(cr, uid, data, context=context)
            if case.sale_id:
                new_ids.append(case.sale_id.id)
            if not new_ids:
                return {'type': 'ir.actions.act_window_close'}
            if len(new_ids) <= 1:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': _('Quotation'),
                    'res_id': new_ids and new_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', new_ids)]),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'sale.order',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'name': _('Quotation'),
                    'res_id': new_ids
                }
            return value

    def onchange_absolute(self, cr, uid, ids, margin_amount=0.0, absolute=False, percentage=False, context=None):
        """This function returns value of  product's member price based on product id.
        """
        if percentage:
            return {'value': {'absolute': False}}
        if absolute:
            return {'value': {'percentage': False}}
        return {'value': {}}

    _columns = {
        'partner_id': fields.many2one('res.partner', 'Customer', required=True, domain=[('customer', '=', True)]),
        'tr_amount': fields.float('Transport amount'),
        'hr_amount': fields.float('Hotel amount'),
        'trc_amount': fields.float('Ticket amount'),
        'v_amount': fields.float('Visa amount'),
        'is_amount': fields.float('Insurance amount'),
        'ex_amount': fields.float('Excursion amount'),
        'pas_amount': fields.float('Passport amount'),
        'margin_amount': fields.float('Margin amount'),
        'total_amount': fields.float('Total Amount'),
        'absolute': fields.boolean('Absolute'),
        'percentage': fields.boolean('Percentage'),

    }
    _defaults = {
        'close': False,
        'partner_id': _selectPartner,
    }


class tour_send_query(osv.osv_memory):
    """ Make sale  order for crm """

    _name = "tour.send.query"
    _description = "Query"

    def _selectPartner(self, cr, uid, context=None):
        """
        This function gets default value for partner_id field.
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param context: A standard dictionary for contextual values
        @return: default value of partner_id field.
        """
        if context is None:
            context = {}

        lead_obj = self.pool.get('tour.send.query')
        active_id = context and context.get('active_id', False) or False
        if not active_id:
            return False

        lead = lead_obj.read(cr, uid, [active_id], ['customer_id'], context=context)[0]
        return lead['customer_id'][0] if lead['customer_id'] else False

    def view_init(self, cr, uid, fields_list, context=None):
        return super(tour_send_query, self).view_init(cr, uid, fields_list, context=context)

    def makeOrder(self, cr, uid, ids, context=None):
        active_id = context and context.get('active_ids', []) or []
        temp_obj = self.pool.get('email.template')
        case_obj = self.pool.get('tour.query')
        ven_obj = self.pool.get('tour.hotel.vender')
        vender_email_list = []
        for make in self.browse(cr, uid, ids, context=context):
            for case in case_obj.browse(cr, uid, active_id, context=context):
                if case.ticket == True and case.tc_vendor_id:
                    if case.tc_vendor_id.email and case.tc_vendor_id.email not in vender_email_list:
                        vender_email_list.append(case.tc_vendor_id.email)
                if case.hotel == True and case.all_ids:
                    for hotel_info in case.all_ids:
                        if hotel_info.vender_ids.email and hotel_info.vender_ids.email not in vender_email_list:
                            vender_email_list.append(hotel_info.vender_ids.email)
                if case.trnsport == True and case.tr_vendor_id:
                    if case.tr_vendor_id.email and case.tr_vendor_id.email not in vender_email_list:
                        vender_email_list.append(case.tr_vendor_id.email)
                if case.extraction == True and case.ex_vendor_id:
                    if case.ex_vendor_id.email and case.ex_vendor_id.email not in vender_email_list:
                        vender_email_list.append(case.ex_vendor_id.email)
        if len(vender_email_list) > 0:
            for vender_email in vender_email_list:
                data = ''
                # ven_id = ven_obj.search(cr,uid,[('email','=',vender_email)],context)
                # print ven_id,ven_id,ven_id,ven_id,ven_id
                # ven_rec = ven_obj.browse(cr,uid,ven_id,context)
                for case in case_obj.browse(cr, uid, active_id, context=context):
                    data += '<table border=2 width="100%"><tr><td bgcolor="#03578D" colspan=7><font color="white"><b>Customer Detail</b></font></td></tr>'
                    data += '<tr><td><b>Name</b></td><td>%s</td></tr>'%(case.customer_id.name or '')
                    data += '<tr><td><b>Number of Adults</b></td><td>%s</td></tr>'%(case.adult_no or '')
                    data += '<tr><td><b>Extra Adult</b></td><td>%s</td></tr>'%(case.extra_no or '')
                    data += '<tr><td><b>Infants</b></td><td>%s</td></tr>'%(case.infants or '')
                    data += '<tr><td><b>Children With Bead</b></td><td>%s</td></tr>'%(case.cwb_no or '')
                    data += '<tr><td><b>Child With out Bead</b></td><td>%s</td></tr></table><br/>'%(case.cw_no or '')
                    vender_name = ''
                    if case.ticket == True and case.tc_vendor_id:
                        if case.tc_vendor_id.email == vender_email:
                            data += '<table border=1 width="100%"><tr><td bgcolor="#03578D" colspan=7><font color="white"><b>Ticket Detail</b></font></td></tr><tr><td><b>Mode</b></td><td><b>Origin</b></td><td><b>Destination</b></td><td><b>Depart Date</b></td><td><b>Flexible Days</b></td><td><b>Class of travel</b></td></tr>'
                            if case.one_way:
                                vender_name = case.tc_vendor_id.name
                                for ticket_rec in case.ticket_ids_one:
                                    data += '<tr>'
                                    data += '<td>%s</td>'%(ticket_rec.mode_type or '')
                                    data += '<td>%s</td>'%(ticket_rec.source.city or '')
                                    data += '<td>%s</td>'%(ticket_rec.destination.city or '')
                                    data += '<td>%s</td>'%(ticket_rec.ticket_date or '')
                                    data += '<td>%s</td>'%(ticket_rec.client_days or '')
                                    data += '<td>%s</td>'%(ticket_rec.ref_type or '')
                                    data += '</tr>'
                            elif case.round_trip:
                                vender_name = case.tc_vendor_id.name
                                for ticket_rec in case.ticket_ids_round:
                                    data += '<tr>'
                                    data += '<td>%s</td>'%(ticket_rec.mode_type or '')
                                    data += '<td>%s</td>'%(ticket_rec.source.city or '')
                                    data += '<td>%s</td>'%(ticket_rec.destination.city or '')
                                    data += '<td>%s</td>'%(ticket_rec.ticket_date or '')
                                    data += '<td>%s</td>'%(ticket_rec.client_days or '')
                                    data += '<td>%s</td>'%(ticket_rec.ref_type or '')
                                    data += '</tr>'
                            if case.multicity:
                                vender_name = case.tc_vendor_id.name
                                for ticket_rec in case.ticket_ids_multi:
                                    data += '<tr>'
                                    data += '<td>%s</td>'%(ticket_rec.mode_type)
                                    data += '<td>%s</td>'%(ticket_rec.source.city)
                                    data += '<td>%s</td>'%(ticket_rec.destination.city)
                                    data += '<td>%s</td>'%(ticket_rec.ticket_date)
                                    data += '<td>%s</td>'%(ticket_rec.client_days)
                                    data += '<td>%s</td>'%(ticket_rec.ref_type)
                                    data += '</tr>'
                            data += '</table><br/><br/>'

                    if case.hotel == True and case.all_ids:
                        hotel_data = ''
                        for hotel_info in case.all_ids:
                            if hotel_info.vender_ids.email == vender_email:
                                vender_name = case.tc_vendor_id.name
                                hotel_data += '<tr>'
                                hotel_data += '<td>%s</td>'%(hotel_info.hotel_id.name or '')
                                hotel_data += '<td>%s</td>'%(hotel_info.hotel_id.name or '')
                                hotel_data += '<td>%s</td>'%(hotel_info.check_in or '')
                                hotel_data += '<td>%s</td>'%(hotel_info.check_out or '')
                                hotel_data += '<td>%s</td>'%(hotel_info.mean_id.name or '')

                        if hotel_data != '':
                            data += '<table border=1 width="100%"><tr><td bgcolor="#03578D" colspan=5><font color="white"><b>Hotel Detail</b></font></td></tr><tr><td><b>Hotel Name</b></td><td><b>Number of Night</b></td><td><b>Check IN</b></td><td><b>Check OUT</b></td><td><b>Meal Plan</b></td></tr>'
                            data += '%s'%(hotel_data)
                            data += '</table><br/><br/>'

                    if case.trnsport == True and case.tr_vendor_id:
                        if case.tr_vendor_id.email == vender_email:
                            vender_name = case.tc_vendor_id.name
                            data += '<table border=1 width="100%"><tr><td bgcolor="#03578D" colspan=6><font color="white"><b>Transportation Detail</b></font></td></tr><tr><td><b>From Date</b></td><td><b>Source Location</b></td><td><b>To Date</b></td><td><b>Destination Location</b></td><td><b>mode of transport</b></td><td><b>Vehicle</b></td></tr>'
                            for trnsport_rec in case.transport_ids:
                                data += '<tr>'
                                data += '<td>%s</td>'%(trnsport_rec.from_date or '')
                                data += '<td>%s</td>'%(trnsport_rec.source_l.city or '')
                                data += '<td>%s</td>'%(trnsport_rec.to_date or '')
                                data += '<td>%s</td>'%(trnsport_rec.destination_l.city or '')
                                tr_type = ''
                                if trnsport_rec.type_mode == 'dispo':
                                    tr_type = 'Disposal'
                                else:
                                    tr_type = 'Point to Point'
                                data += '<td>%s</td>'%(tr_type or '')
                                data += '<td>%s</td>'%(trnsport_rec.vehicle or '')
                                data += '</tr>'
                            data += '</table><br/><br/>'

                    if case.extraction == True and case.ex_vendor_id:
                        if case.ex_vendor_id.email == vender_email:
                            vender_name = case.tc_vendor_id.name
                            data += '<table border=1 width="100%"><tr><td bgcolor="#03578D" colspan=7><font color="white"><b>Excursion Detail</b></font></td></tr><tr><td><b>Days</b></td><td><b>Date</b></td><td><b>City</b></td><td><b>Discription</b></td></tr>'
                            for ext_rec in case.line_ids:
                                data += '<tr>'
                                data += '<td>%s</td>'%(ext_rec.name or '')
                                data += '<td>%s</td>'%(ext_rec.to_date or '')
                                data += '<td>%s</td>'%(ext_rec.city.city or '')
                                data += '<td>%s</td>'%(ext_rec.city_description or '')
                                data += '</tr>'
                            data += '</table><br/><br/>'

                    mail_obj=self.pool.get('mail.mail')
                    email_server=self.pool.get('ir.mail_server')
                    email_sender_id=email_server.search(cr, uid, [],limit=1)
                    email_sender_rec = email_server.browse(cr,uid,email_sender_id,context)
                    # if ven_rec.id:
                    #     ven_name = ven_rec.name or ""
                    mail_data={
                       'email_from':email_sender_rec.smtp_user,
                       'email_to':vender_email,
                       'subject':"%s | %s"%(str(case.name),str(case.customer_id.name)),
                       'body_html':'<div><p>Dear %s,</p> </br>'
                                    '<p>Greetings From Shree Salasar Holidays</p>'
                                    '<p>Require Quotation for below described details</p>'
                                    '<p>%s</p>'
                                    '<p>Best Regards<br/>'
                                   'Shree Salasar Holidays<br/>'
                                   'Phone : +0261-4021666, +91 9998030666,<br/></p>'
                                   %(vender_name,data),
                    }
                    mail_id = mail_obj.create(cr, uid, mail_data, context)
                    mail_obj.send(cr, uid, mail_id, context)

                # for tour_query in case_obj.browse(cr, uid, active_id, context=context):
                #     print "========>>>>>>case",tour_query.name
                #     if tour_query.ticket == True and tour_query.tc_vendor_id:
                #         if tour_query.tc_vendor_id.email == vender_email:
                #
                # print "email list ============>>>>>>>>>>>",vender_email_list

    # def makeOrder(self, cr, uid, ids, context=None):
    #     case_obj = self.pool.get('tour.query')
    #     partner_obj = self.pool.get('hr.employee')
    #     data = context and context.get('active_ids', []) or []
    #     temp_obj = self.pool.get('email.template')
    #     for make in self.browse(cr, uid, ids, context=context):
    #         for case in case_obj.browse(cr, uid, data, context=context):
    #             #                 all_ready= self.pool.get('mail.message').search(cr,uid,[('res_id','=',case.id),('model','=','tour.query')])
    #             #                 if all_ready:
    #             if case.tc_vendor_id.id and case.tr_vendor_id and case.ex_vendor_id:
    #                 f = case.tc_vendor_id.id == case.tr_vendor_id.id == case.ex_vendor_id.id
    #                 if f:
    #                     template_id = \
    #                     self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour', 'email_template_tour_all')[
    #                         1]
    #                     temp_obj.send_mail(cr, uid,
    #                                        template_id,
    #                                        case.id, context=context)
    #
    #                     #  email_template_tour_all
    #             else:
    #                 if case.ticket and case.ticket_ids:
    #                     template_id = \
    #                     self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour', 'email_template_ticket')[1]
    #                     temp_obj.send_mail(cr, uid,
    #                                        template_id,
    #                                        case.id, context=context)
    #                 if case.hotel:
    #                     if case.all_ids:
    #
    #                         #                             template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour', 'email_template_hotel')[1]
    #                         #                             temp_obj.send_mail(cr, uid,
    #                         #                                             template_id,
    #                         #                                             da.hotel_id.id, context=context)
    #                         #
    #
    #                         template_id = \
    #                         self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour', 'email_template_tour')[
    #                             1]
    #                         for da in case.all_ids:
    #                             temp_obj.send_mail(cr, uid,
    #                                                template_id,
    #                                                case.id, context=context)
    #
    #                 if case.trnsport and case.transport_ids:
    #                     template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour',
    #                                                                                       'email_template_trasnport')[1]
    #                     temp_obj.send_mail(cr, uid,
    #                                        template_id,
    #                                        case.id, context=context)
    #
    #                 if case.extraction and case.line_ids:
    #                     template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour',
    #                                                                                       'email_template_excursion')[1]
    #                     temp_obj.send_mail(cr, uid,
    #                                        template_id,
    #                                        case.id, context=context)
    #
    #         return {'type': 'ir.actions.act_window_close'}

# _defaults = {
#         'employee_id': _selectPartner,
#     }

class tour_query_hotel(osv.osv_memory):
    _name = 'tour.query.hotel'
    _description = 'Transport query'
    _columns = {
        'invoice': fields.many2many('account.invoice', 'account_user_rel', 'user_id', 'wizard_id', 'Last invoice'),
        'hotel_ids': fields.many2one('tour.hotel', 'Hotel'),
        'vender_ids': fields.many2many('tour.hotel.vender', 'vendor_rel', 'user_id', 'wizard_id',
                                       string='Vendor Detail')
    }

    def onchange_hotel_ids(self, cr, uid, ids, hotel_ids=False, context=None):
        res = {}
        case_obj = self.pool.get('tour.query')
        vendor_obj = self.pool.get('tour.hotel.vender')
        vendor_obje_line = self.pool.get('tour.hotel.vender.line')
        data = context and context.get('active_ids', []) or []
        list1 = []
        if hotel_ids:
            line_ids = vendor_obje_line.search(cr, uid, [('hotel_id', '=', hotel_ids)])
            if line_ids:
                for data in vendor_obje_line.browse(cr, uid, line_ids, context):
                    list1.append(data.vendor_id.id)
            else:
                res['value'] = {'vender_ids': []}
            res['value'] = {'vender_ids': list1}
        return res

    def get_order(self, cr, uid, ids, context=None):
        #         case_obj = self.pool.get('tour.query')
        #         vendor_obj=self.pool.get('tour.hotel.vender')
        #         vendor_obje_line=self.pool.get('tour.hotel.vender.line')
        #         data = context and context.get('active_ids', []) or []
        #         list1=[]
        #         for make in self.browse(cr, uid, ids, context=context):
        #             for case in case_obj.browse(cr, uid, data, context=context):
        #                 if make.hotel_ids:
        #                    line_ids=vendor_obje_line.search(cr,uid,[('hotel_id','=',make.hotel_ids.id)])
        #                    if line_ids:
        #                        for data in vendor_obje_line.browse(cr,uid,line_ids,context):
        #                            print "88888============8888888", data.vendor_id.id,data.vendor_id.name
        #                            list1.append(data.vendor_id.id)
        #                 res['value'] = {'vender_ids': list1}
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
