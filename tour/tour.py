from datetime import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import workflow
from openerp import fields, models, api, exceptions, _
from openerp.osv import osv
class family_member_rel(models.Model):
    """Travel"""
    _name = 'family.member.rel'
    name = fields.Char('Relation', required=True)    

class family_member(models.Model):
    """Travel"""
    _name = 'family.member'
    _inherit = ['mail.thread']

    name = fields.Char('Name of Member', required=True)
    age = fields.Integer('Age')
    relation = fields.Many2one(
        'family.member.rel',
        'Relation',
       )
    #Selection([ ('son','Son'), ('aunty','Aunty'),('uncle','Uncle'),('father','Father'),('mother','Mother'),('brother','Brother'),('sister','Sister'),('wife','Wife'), ('friend','Friend')],
                           #  'Relation')
    partner_id = fields.Many2one(
        'res.partner',
        'Passenger',
       
        help="Name of Passenger."
    )
    p_no = fields.Char('Passport No',)   
    p_issue_date = fields.Date('Passport Issue Date ')
    p_exp_date = fields.Date('Passport expire Date ')
    p_issue_place = fields.Char('Passport Issue place ')    
    # 
# class family_member(osv.osv):
#     """ CRM Lead Case """
#     _name = "family.memeber"
#     _description = "Family Member Detail"
#     _columns = {
#         'age': fields.integer('Age'),
#         'name': fields.char('Name',)   ,           
#         'relation': fields.selection(),
#         
#         'partner_id': fields.many2one('res.partner', 'Customer'),
#                 }
# 
# 
# class tour_hotel(osv.osv):
#     """ Hotel Detail """
#     _name = "tour.hotel"
#     _inherit = ['mail.thread']
#     _description = "Hotel"
#     _columns = {
#         'name': fields.char('Hotel Name',required=True, )   ,           
#         'partner_id': fields.many2one('res.partner', 'Contact Person'),
#          'direct_suppiler': fields.boolean('Direct Supplier', help="If True then Hotel Link with Tour."),
#          'vender':fields.boolean('Direct Supplier', help="If True then Agent Link with Hotel."),
#          'email': fields.char('Hotel email address',)  ,
#            'zip_id': fields.many2one('res.better.zip', 'City/Location',required=True, )
#                 }
#     
# 
class tour_hotel_contact(models.Model):
    """hotel"""
    _name = 'tour.hotel.contact'
    name = fields.Char('Name of Contact', required=True) 
    co_no = fields.Char('Contact No', required=True) 
    email = fields.Char(
        string='Email',)
    partner_hotel_id = fields.Many2one(
        'tour.hotel',
        'Hotel Person',
        help="Hotel.",)
     
class tour_hotel_meal(models.Model):
    """hotel"""
    _name = 'tour.hotel.meal'
    name = fields.Char('Name of Plan', required=True) 
         
     
class tour_essentials(models.Model):
    """hotel"""
    _name = 'tour.essentials'
    name = fields.Char('Essentials Name ', required=True) 
    desc = fields.Text('Description')
 
class tour_meal_line(models.Model):
    _name = 'tour.meal.line'
    _rec_name="id"
    id = fields.Integer('Sr No', readonly=True),
    meal_id=fields.Many2one('tour.hotel.meal', 'Meal')  
    rate=fields.Float('Rate')  
    hotel_id = fields.Many2one(
        'tour.hotel',
        'Hotel')    


class tour_hotel_room(models.Model):
    """hotel"""
    _name = 'tour.hotel.room'
    name = fields.Char('Room Category', required=True)        
     
class tour_hotel_inv(models.Model):
    """hotel"""
    _name = 'tour.hotel.inv'
    _rec_name='hote_id'
    hote_id = fields.Many2one('tour.hotel','Select Hotel')
    room_id = fields.Many2one('tour.hotel.room','Room Category')   
    rate=fields.Float('Buy Price') 
    r_price = fields.Integer('Number Room')
    dob_range= fields.Date('From Date', )
    dob_to= fields.Date('To Date', )
    tour_id= fields.Many2one('tour.query','Query')    
           
             
class tour_hotel(models.Model):
    """hotel"""
    _name = 'tour.hotel'
    _inherit = ['mail.thread']
    name = fields.Char('Name of Hotel', required=True)
    direct_suppiler = fields.Boolean('Direct Supplier', help="If True then Hotel Link with Tour.")
    vender = fields.Boolean('Vendor', help="If True then Agent Link with Tour.")
    zip_id = fields.Many2one('res.better.zip',string='City/Location')
    meal_id = fields.One2many('tour.meal.line','hotel_id',string='Meal Detail')        
#     partner_id = fields.Many2one(
#         'res.partner',
#         'Contact Person',
#         help="Contact Person.",)
    email = fields.Char(
        string='Email',)
    #
    street = fields.Char('Street', )
    street2 = fields.Char('Street2')    
    be_group= fields.Char('Group')
    phone = fields.Char('Hotel Phone')   
    line_ids=fields.One2many('tour.hotel.contact', 'partner_hotel_id', 'Contact Detail', )     
     
    @api.one
    @api.onchange('zip_id')
    def onchange_zip_id(self):
        if self.zip_id:
            self.zip = self.zip_id.name
            self.city = self.zip_id.city
            self.state_id = self.zip_id.state_id
            self.country_id = self.zip_id.country_id   
              
class tour_hotel_vender_line(models.Model):
    _name = 'tour.hotel.vender.line'
    _rec_name="id"
    id = fields.Integer('Sr No', readonly=True),
    hotel_id=fields.Many2one('tour.hotel', 'Hotel List')  
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor')  


    
class tour_hotel_vender(models.Model):
    """hotel"""
    _name = 'tour.hotel.vender'
    _inherit = ['mail.thread']

    part_id = fields.Many2one('res.partner','Vendor Invoice')
    name = fields.Char('Name of Vendor', required=True)
    line_ids=fields.One2many('tour.hotel.vender.line', 'vendor_id', 'PHS', )
    phone = fields.Char('Vendor Phone', required=True)
    zip_id = fields.Many2one(
        'res.better.zip',string='City/Location')
#         'zip': fields.char('Zip', change_default=True, size=24),
#         'city': fields.char('City'),
#         'state_id': fields.many2one("res.country.state", 'State'),
#         'country_id': fields.many2one('res.country', 'Country')
    email = fields.Char(
                     string='Email',required=True)

    #
    street = fields.Char('Street', )
    street2 = fields.Char('Street2')
     
    
    partner_id = fields.Many2one(
        'res.partner',
        'Contact Person',
        help="Contact Person.",)
    zip_id = fields.Many2one(
        'res.better.zip',string='City/Location')
    partner_id = fields.Many2one(
        'res.partner',
        'Contact Person',
        help="Contact Person.",)
    email = fields.Char(
        string='Email',)

class res_partner(models.Model):
    _inherit = 'res.partner'
    dob= fields.Date('Date of Birth ', )
    dan= fields.Date('Date of Anniviersy ', )
    ref_type= fields.Selection([ ('walking','Walking'), ('referred','Referred'), ],'Type')
    ref_partner_id=fields.Many2one('res.partner', 'Refer by Existing Customer')
    line_ids=fields.One2many('family.member', 'partner_id', 'Family Member', )
    p_no = fields.Char('Passport No',)   
    p_issue_date = fields.Datetime('Passport Issue Date ')
    p_exp_date = fields.Datetime('Passport expire Date ')
    p_issue_place = fields.Datetime('Passport Issue place ')
    city_ids = fields.Many2many(
        'res.better.zip',
        string='Locations',
        help='Destination cities of travel.',
    )    

    
#     _columns = {
#                 'dob': fields.datetime('Date of Birth ', ),
#                 'dan': fields.datetime('Date Anniveaty',),
#                 'ref_type': fields.selection([ ('walking','Walking'), ('existing','Existing'), ],'Type'),
#                 'ref_partner_id': fields.many2one('res.partner', 'Refer by Existing Customer'),
#                 'line_ids': fields.one2many('family.memeber', 'partner_id', 'Family Member', ),
#                 'p_no': fields.char('Passport No',)      ,            
#                 'p_issue_date': fields.datetime('Passport Issue Date '),}
               
#                 'city_ids': fields.many2many(
#         'res.better.zip',
#         string='Locations',
#         help='Destination cities of travel.',
#     )
         
         
#         
#         }    

class tour_package_line(models.Model):
    _name ='tour.package.line'
    name = fields.Char('Name', required=True)
    city = fields.Many2one('res.better.zip',"City/Location")
    desc = fields.Char(string="Description")
    hotel_id = fields.Many2one(
        'tour.hotel',
        string='Hotel')
    extr_id = fields.Many2one('tour.extraction' ,'Excursion')
    ess_id = fields.Many2one('tour.essentials' ,'Essentials')
    pack_id = fields.Many2one('tour.package' ,'Package')
    hotel_id = fields.Many2one('tour.hotel' ,'Hotel')
    
    
class tour_package(models.Model):
    _name ='tour.package'
    _description='tour package'
    _inherit = ['mail.thread']      
    name = fields.Char('Package Name', required=True)
    tour_type= fields.Selection([('domestic','Domestic'),('international','International')],'Tour type')
    tour_pack= fields.Selection([('fixed','Fixed'),('custom','Customized')],'Tour/Package type')
    price = fields.Float('Price per night')
    month =fields.Selection([('01','January'), ('02','February'), ('03','March'), ('04','April'), ('05','May'), ('06','June'),
                                  ('07','July'), ('08','August'), ('09','September'), ('10','October'), ('11','November'), ('12','December')],'Month',)
                                  
    days= fields.Float('No of Nights')
    city = fields.Many2one('res.better.zip',string='City',required=True)    
    country_id = fields.Many2one('res.country',string='Country',required=True)    
    location = fields.Many2many(
        'res.better.zip',
        string='Locations',
        help='Destination cities of travel.',
    )   
    line_ids=fields.One2many('tour.package.line', 'pack_id', 'Days wise Detail', )

class tour_ex_type(models.Model):
    _name ='tour.ex.type'
    _description='tour package'
    name = fields.Char('Name', required=True)  
    description = fields.Text('Description')  

class tour_ext_line(models.Model):
    _name ='tour.ext.line'
    name = fields.Char('Site See Name', required=True)
    date_start = fields.Date('From Date', required=True)
    date_stop = fields.Date('End Date', )
    price = fields.Float('Price')
    day_close = fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of close',  select=True)
    extraction_id = fields.Many2one('tour.extraction',string='Essentials')
    ess_id = fields.Many2many('tour.essentials',id1='line_i', id2='inv_id',string='Essentials')
                                  
        
        

class tour_extraction(models.Model):
    _name ='tour.extraction'
    _inherit = ['mail.thread']  
    _description='Tour extraction'
    name = fields.Char('Excursion Name', required=True)
    date_s = fields.Date('Date')
    query=fields.Many2one('tour.query')
    description = fields.Text('Site seen description')
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor') 
    city = fields.Many2one('res.better.zip','City')
    country_id = fields.Many2one('res.country',string='Country',)
    does_it = fields.Text('Do it ')
    do_not = fields.Text('Donot')
   # line_ids=fields.One2many('tour.ext.line', 'extraction_id', 'Site Seen  Detail', )
    type_ids = fields.Many2many(
        'tour.ex.type',
        string='Type',
    )    
    price = fields.Float('Price')
    
    day_close = fields.Selection([('0','Monday'),('1','Tuesday'),('2','Wednesday'),('3','Thursday'),('4','Friday'),('5','Saturday'),('6','Sunday')], 'Day of close',  select=True)
    ess_id = fields.Many2many('tour.essentials',id1='line_i', id2='inv_id',string='Essentials')
 
class tour_visa(models.Model):
    _name ='tour.visa.type'
    _description='Visa'        
    name = fields.Char('Name', required=True)        
    description = fields.Text('Description')    
    visa = fields.Boolean('Visa Document')
    insuracne = fields.Boolean('Insurance')    
    
    
class tour_visa(models.Model):
    _name ='tour.visa'
    _description='Visa'        
        
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')        
    type_id = fields.Many2one('tour.visa.type',string='Type' ,domain=[('visa','=',True)])  
    amount_price = fields.Float('Visa Price')  
    attach_id = fields.Many2one('ir.attachment',string='Upload') 
   
    
    
    
class tour_passport(models.Model):
    _name ='tour.passport'
    _description='Passport'        
        
    name = fields.Char('Name', required=True)
    attach_id = fields.Many2one('ir.attachment',string='Upload') 
 #   description = fields.Text('Description')        
    #type_id = fields.Many2one('tour.visa.type',string='Type' ,domain=[('visa','=',True)])      
   # amount_price = fields.Float('Passport Price')  
        
        

class tour_insurance(models.Model):
    _name ='tour.insurance'
    _description='Visa'        
    name = fields.Char('Name', required=True) 
    amount_price = fields.Float('Insurance Price') 
    
class tour_ticket(models.Model):
    _name ='tour.ticket'
    _description='Ticket'        
    _inherit = ['mail.thread']      
    name = fields.Char('Name', required=True)
    query=fields.Many2one('crm.lead')
    ticket_date = fields.Date('Date of Travel ')
    ticket_return = fields.Date('Date of return ')
    ref_type= fields.Selection([ ('economy','Economy'), ('first','First class'), ],'Class of travel ')
    mode_type= fields.Selection([ ('bus','Bus'), ('train','Train'),('air','Air') ],'Mode of travel ')   
    client_felxi = fields.Boolean('Client Flexible')
    oneway = fields.Boolean('One way')
    twoway = fields.Boolean('Return')
    client_days = fields.Integer('Flexible Days')
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor')  
    destination = fields.Many2one('res.better.zip','Destination')
    source = fields.Many2one('res.better.zip','Source', )
    amount_price_t = fields.Float('Ticket Price')
    location_id = fields.Many2many(
        'res.better.zip',
        string='Locations',
        help='Destination cities of travel.',
    )    
    def _get_dest(self, cr, uid, context=None):
        res = self.search(cr, uid, [],limit=1,order='id desc',context=context)
        if res:
            data=self.browse(cr,uid,res)
            return data.source.id
        return   False

    _defaults = {      
  'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'tour.ticket') or '/',
  'source':_get_dest
  }     
    def default_get(self, cr, user, fields_list, context=None):
        """
        Returns default values for fields
        @param fields_list: list of fields, for which default values are required to be read
        @param context: context arguments, like lang, time zone
 
        @return: Returns a dict that contains default values for fields
        """
        if context is None:
            context = {}
        values = super(tour_ticket, self).default_get(cr, user, fields_list, context=context)
        return values
 
#     
    def write(self, cr, uid, ids, vals, context=None):
       
        if vals.get('oneway') and  vals.get('twoway'):
            raise osv.except_osv(_('Error!'), _('Select Only One mode!'))      
        return  super(tour_ticket, self).write(cr, uid, ids, vals, context=context)
    
    
     

    def create(self, cr, uid, vals, context=None):
        res_id = super(tour_ticket, self).create(cr, uid, vals, context=context)
        return res_id     
    
     
#         data=self.browse(cr,user,list_ids,context=context)
#        
       
    def onchange_way(self, cr, uid, ids,oneway=False,twoway=False,context=None):
        """This function returns value of  product's member price based on product id.
        """
        if twoway:
            return {'value': {'oneway': False}}
        if oneway:
            return {'value': {'twoway': False}}

        return {'value': {}}

         
    
class tour_transport_line(models.Model):
    _name ='tour.transport.line'
    _description='Transport line'   
    
    date_t = fields.Date('Date of Jouery')
    name =fields.Char('Day no')
    vech_l = fields.Boolean('Vehicle')
    desc = fields.Text('Description') 
    source_l = fields.Many2one('res.better.zip','Source Location')
    destination_l = fields.Many2one('res.better.zip','Destination Location')
           
    tran_id = fields.Many2one(
        'tour.transport',
        'Transport',
    )    
    type = fields.Selection(related='tran_id.type_mode' ,store=True, readonly=True)
    from_date = fields.Date('From Date ')
    to_date = fields.Date('To Date')

class tour_transport(models.Model):
    _name ='tour.transport'
    _description='Transport'        
    _inherit = ['mail.thread']          
    name = fields.Char('Name', required=True)
    no_day = fields.Char('No of Days')
    query =fields.Many2one('crm.lead','Tour')
    type_mode= fields.Selection([ ('point','Point to Point (P2P)'), ('dispo','Disposal'), ],' Select mode of transport')   
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor') 
    vehicle =fields.Char('Vehicle')
#     from_date = fields.Datetime('From Date ')
#     to_date = fields.Datetime('To Date')
    amount_price_tr = fields.Float('Transport Price')
    line_ids=fields.One2many('tour.transport.line', 'tran_id', 'Mode of transport', )
    source_l = fields.Many2one('res.better.zip','Source Location')
    destination_l = fields.Many2one('res.better.zip','Destination Location')
    from_date = fields.Date('From Date ')
    to_date = fields.Date('To Date')
    
    
#     ref_type= fields.Selection([ ('oneway','One way'), ('twoway','Two way'), ],'Type')   
#     client_felxi = fields.Boolean('Client Flexibale')
#     client_days = fields.Integer('Felxibale Days')
#     amount_price_t = fields.Float('Ticket Price')
#     location_id = fields.Many2many(
#         'res.better.zip',
#         string='Locations',
#         help='Destination cities of travel.',
#     )    
#          
#      
    _defaults = {      
  'name': lambda x, y, z, c: x.pool.get('ir.sequence').get(y, z, 'tour.tran') or '/',
  }       
 

class tour_hotel_all(models.Model):
    _name = "tour.hotel.all"
    _rec_name = 'hotel_id'
    check_in=fields.Date('Check IN')
    check_out=fields.Date('Check OUT')
    tour_id =fields.Many2one('crm.lead','Tour')
    hotel_id  = fields.Many2one('tour.hotel', 'Hotel', required=True)
    mean_id=fields.Many2one('tour.hotel.meal','Meal Plan')
    vender_ids = fields.Many2many('tour.hotel.vender',id1='line_id', id2='val_id',string='Vendor Detail')
    vender_id = fields.Many2many('tour.hotel.vender.line',id1='line_id1', id2='val_id',string='Vendor line')
    vendor = fields.Boolean('Vendor')
    send_mail = fields.Boolean('Send Mail')
    diret_hotel = fields.Boolean('Direct')
    invoice_ids = fields.Many2many('account.invoice',id1='line_i', id2='inv_id',string='Invoice')

    def onchange_checkin(self, cr, uid, ids, check_in=False,hotel_id=False):
        res={}
        warning=False
        in_str=''
        iv_obj=self.pool.get('tour.hotel.inv').search(cr,uid,[('hote_id','=',hotel_id),('dob_range','=',check_in)])
        if iv_obj:
            iv_data=self.pool.get('tour.hotel.inv').browse(cr,uid,iv_obj[0])
            in_str= "Number of available Rooms :"+str(iv_data.r_price) +"\n" + "Category :"+  str(iv_data.room_id.name) +"\n"
            in_str+="Price : " +str(iv_data.rate)+"\n"+"From :" + str (iv_data.dob_range)+  "\n" +"To:" +str(iv_data.dob_to)
            
            warn_msg = _(in_str)
            warning = {
                       'title': _('Prepurchased Hotel !'),
                       'message' : warn_msg
                    }
        return {'value': res, 'warning': warning}
    def onchange_hotel_ids(self, cr, uid, ids, hotel_ids=False,vendor=False,diret_hotel=False, context=None):
        res = {}
        case_obj = self.pool.get('tour.query')
        vendor_obj=self.pool.get('tour.hotel.vender')
        acc_obj=self.pool.get('account.invoice')
        vendor_obje_line=self.pool.get('tour.hotel.vender.line')
        data = context and context.get('active_ids', []) or []
        list1=[]
        line_acc=[]
        vender_all=[]
        v=[]
        if hotel_ids :
            line_ids=vendor_obje_line.search(cr,uid,[('hotel_id','=',hotel_ids)],)
            inv_all=acc_obj.search(cr,uid,[('hotel_id','=',hotel_ids)],limit=1, )  
            if line_ids:
                for data in vendor_obje_line.browse(cr,uid,line_ids,context):
                    v.append(data.vendor_id.id)
                vender_all=acc_obj.search(cr,uid,[('vendor_id','in',v)])    
                res['value'] = {'vender_ids': v, 'invoice_ids': vender_all}        
        if hotel_ids  :      
            line_ids=vendor_obje_line.search(cr,uid,[('hotel_id','=',hotel_ids)])
            inv_all=acc_obj.search(cr,uid,[('hotel_id','=',hotel_ids)],limit=1, )  
            if line_ids:
                for data in vendor_obje_line.browse(cr,uid,line_ids,context):
                    v.append(data.vendor_id.id)
                res['value'] = {'vender_ids': v, 'invoice_ids': inv_all}                            
        if hotel_ids:
            line_ids=vendor_obje_line.search(cr,uid,[('hotel_id','=',hotel_ids)])
            inv_all=acc_obj.search(cr,uid,[('hotel_id','=',hotel_ids)],limit=1, )  
            if line_ids:
                for data in vendor_obje_line.browse(cr,uid,line_ids,context):
                    v.append(data.vendor_id.id)
                vender_all=acc_obj.search(cr,uid,[('vendor_id','in',v)])    
                res['value'] = {'vender_ids': v, 'invoice_ids': inv_all+vender_all}              
        else:
               res['value'] = {'vender_ids': [], 'invoice_ids': []}            
        return res        
                          
class tour_query_line(models.Model):
    _name ='tour.query.line'
    name = fields.Char('Day', required=True)
    city = fields.Many2one('res.better.zip',"City")
    to_date = fields.Date('To Date')
    query = fields.Many2one('crm.lead',"Query")
    price = fields.Float(string="Price")
    end_date = fields.Date('End Date')
    hotel_id = fields.Many2one(
        'tour.hotel',
        string='Hotel')
    extr_id = fields.Many2many('tour.extraction','tour_test_rel', 'query','id3' ,'Excursion')
    transport_id = fields.Many2one(
        'tour.transport',
        'Transport',
    )       
    ticket_id = fields.Many2one(
        'tour.ticket',
        'Ticket',
    )              

       
    def onchange_date(self, cr, uid, ids, to_date, end_date, context=None):
        res = {}
        tour_query_obj = self.pool.get('tour.query')
        obj = self.browse(cr, uid, ids, context=context)
        for query in tour_query_obj.browse(cr, uid, [obj.query.id]):
            for line in query.line_ids:
                if line.id > ids[0]:
                    write_true = self.write(cr, uid, line.id, {'to_date':end_date})
                    break
                    

        return {'value': {}}
                    
class tour_query(models.Model):
    _name ='tour.query'
    _inherit = ['mail.thread']
    _description='query'
    name = fields.Char('Query Name',readonly=True)
    customer_id = fields.Many2one(
        'res.partner',
        'Customer', required=True,
        help="Name of Passenger."
    )
    tour_type= fields.Selection([('domestic','Domestic'),('international','International')],'Tour type', required=True)
    ex_vendor_id=fields.Many2one('tour.hotel.vender', 'Excursion Vendor')
    tc_vendor_id=fields.Many2one('tour.hotel.vender', 'Ticket Vendor')
    tr_vendor_id=fields.Many2one('tour.hotel.vender', ' Transportation Vendor')
    location_id = fields.Many2many('res.better.zip','idt', 'ide',string='Destination',required=True)
    adult_no = fields.Integer('Number of Adult')
    cwb_no = fields.Integer('Number of Child with bed CWB')
    cw_no = fields.Integer('Number of Child without Bed CNB')
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
    all_ids=fields.One2many('tour.hotel.all', 'tour_id', 'Hotel/Vendor/Invoice Detail', )
    vendor = fields.Boolean('Hotel Vendor')
    direct = fields.Boolean('Direct Hotel')
    company_id= fields.Many2one('res.company', 'Company')
    hotel_id = fields.Many2one(
        'tour.hotel',
        'Hotel',
    )

    visa_id = fields.Many2one(
        'tour.visa',
        'Visa',
    )
    transport_ids = fields.One2many(
         'tour.transport','query',
         'Transport',
     )

    sale_id = fields.Many2one(
        'sale.order',
        'Sale Order',
    )

#     ticket_id = fields.One2many(
#         'tour.ticket',
#         'Ticket',
#     )
#     insurance_id = fields.Many2one(
#         'tour.insurance',
#         'Insurance',
#     )
    passport_id = fields.Many2one(
        'tour.passport',
        'Passport',
    )
    vender_ids=fields.Many2many('tour.hotel.vender', 'vendor_test_rel', 'hote_id', 'wizard_id',string='Vendor Detail')
   # vender_ids':fields.many2many('tour.hotel.vender','vendor_rel', 'user_id', 'wizard_id',string='Vendor Detail')
    invoice=fields.Many2many('account.invoice','test_rel','test_2id','id2_test','Last invoice')
    #'invoice': fields.many2many('account.invoice', 'account_user_rel', 'user_id', 'wizard_id', 'Last invoice'),
   # extraction_id = fields.One2many('tour.extraction', 'query',string='E,xcursion')
    emp_id = fields.Many2one('hr.employee',string='Employee')

    days= fields.Integer('No of Night',required=True)
    line_ids=fields.One2many('tour.query.line', 'query', 'Excursion', )
    ticket_emp_id = fields.Many2one('hr.employee',string='Ticket Employee')
    ticket_ids=fields.One2many('tour.ticket', 'query', 'Ticket Detail', )
    state =fields.Selection([
            ('draft', 'Not Confirmed'),
            ('done', 'Confirmed'),
            ('cancel','Cancel') ])
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        context = context or {}
        if not default.get('line_ids'):
            #we don't want to propagate the link to the purchase order line except in case of move split
            default['line_ids'] = False
        default['sale_id'] = False
        return super(tour_query, self).copy(cr, uid, id, default, context)

#
#     def onchange_hotel_ids(self, cr, uid, ids, hotel_ids=False, context=None):
#         res = {}
#         case_obj = self.pool.get('tour.query')
#         vendor_obj=self.pool.get('tour.hotel.vender')
#         vendor_obje_line=self.pool.get('tour.hotel.vender.line')
#         data = context and context.get('active_ids', []) or []
#         list1=[]
#         if hotel_ids:
#             line_ids=vendor_obje_line.search(cr,uid,[('hotel_id','=',hotel_ids)])
#             if line_ids:
#                 for data in vendor_obje_line.browse(cr,uid,line_ids,context):
#                     list1.append(data.vendor_id.id)
#             else:
#                 res['value'] = {'vender_ids': []}
#             res['value'] = {'vender_ids': list1}
#         return res

    def open_invoices(self, cr, uid, ids, invoice_ids, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(cr, uid, 'account', 'invoice_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(cr, uid, 'account', 'invoice_tree')
        tree_id = tree_res and tree_res[1] or False

        return {
            'name': _('Invoice'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'res_id': invoice_ids,
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'context': {'type': 'out_invoice'},
            'type': 'ir.actions.act_window',
        }
    def make_invoice(self, cr, uid, ids, context=None):
        case_obj = self.pool.get('tour.query')
        obj_sale_order_line = self.pool.get('sale.order.line')
        sale_obj= self.pool.get('sale.order')
        partner_obj = self.pool.get('res.partner')
        data = context and context.get('active_ids', []) or []
        for case in case_obj.browse(cr, uid, ids, context=context):
            partner = case.sale_id.partner_id
#             partner_addr = partner_obj.address_get(cr, uid, [partner.id],
#                         ['default', 'invoice', 'delivery', 'contact'])
            pricelist = partner.property_product_pricelist.id
            fpos = partner.property_account_position and partner.property_account_position.id or False
            payment_term = partner.property_payment_term and partner.property_payment_term.id or False
            new_ids = []
            #
            a = case.sale_id.partner_id.property_account_receivable.id
            if case.sale_id.partner_id and case.sale_id.partner_id.property_payment_term.id:
                pay_term = case.sale_id.partner_id.property_payment_term.id
            else:
               pay_term = False


            lines=[]
            inv_all=[]
            states = ['confirmed', 'done', 'exception']
            if not case.sale_id.invoice_ids:
                for line in case.sale_id.order_line:
                    if line.invoiced:
                        continue
                    elif (line.state in states):
                        lines.append(line.id)
                created_lines = obj_sale_order_line.invoice_line_create(cr, uid, lines)
                print "==================ddddddddddddddd======================="
                for line in created_lines:
                    inv = {
                        'name': case.sale_id.client_order_ref or '',
                        'origin': case.sale_id.name,
                        'type': 'out_invoice',
                        'reference': "P%dSO%d" % (case.sale_id.partner_id.id, case.sale_id.id),
                        'account_id': a,
                        'partner_id': case.sale_id.partner_invoice_id.id,
                        'invoice_line': [(6, 0, [line])],
                        'currency_id' : case.sale_id.pricelist_id.currency_id.id,
                        'comment': case.sale_id.note,
                        'payment_term': pay_term,
                        'fiscal_position': case.sale_id.fiscal_position.id or case.sale_id.partner_id.property_account_position.id,
                        'user_id': case.sale_id.user_id and case.sale_id.user_id.id or False,
                        'company_id': case.sale_id.company_id and case.sale_id.company_id.id or False,
                        'hotel_id':case.sale_id.hotel_id,
                        'vendor_id':case.sale_id.vendor_id,
                        'date_invoice': fields.date.today(),
                }
                    inv_id = self.pool.get('account.invoice').create(cr, uid, inv)
                    inv_all.append(inv_id)
                if inv_all:
                    sale_obj.write(cr,uid,[case.sale_id.id],{'invoice_ids':[(6, 0,inv_all)]})
                    sale_obj.invalidate_cache(cr, uid, ['invoice_ids'], [case.sale_id.id], context=context)
                    flag = True
                    sale_obj.message_post(cr, uid, [case.sale_id.id], body=_("Invoice created"), context=context)
                    data_sale = sale_obj.browse(cr, uid,case.sale_id.id, context=context)
                    for line in case.sale_id.order_line:
                        if not line.invoiced:
                         flag = False
                         break
                        if flag:
                         line.order_id.write({'state': 'progress'})
                         workflow.trg_validate(uid, 'sale.order', case.sale_id.id, 'all_lines', cr)

#              if not invoices:
# #                  raise osv.except_osv(_('Warning!'), _('Invoice cannot be created for this Sales Order Line due to one of the following reasons:\n1.The state of this sales order line is either "draft" or "cancel"!\n2.The Sales Order Line is Invoiced!'))
#              if context.get('open_invoices', False):
              #      return self.open_invoices(cr, uid, ids, inv_all, context=context)
            return {'type': 'ir.actions.act_window_close'}
    _defaults = {
  'tour_type':'domestic',
 'company_id': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).company_id.id,
  }

    def action_button_confirm(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'})
        return True

    def action_button_(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'cancel'})
        return True
    def create(self, cr, uid, vals, context=None):
        if ('name' not in vals) or (vals.get('name') in ('/', False)):
            if  vals.get('tour_type') == 'domestic':
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'tour.dom') or '/'
            elif vals.get('tour_type') == 'international':
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'tour.int') or '/'

        new_id = super(tour_query, self).create(cr, uid, vals, context=context)
        context = context or {}

        new_id = super(tour_query, self).create(cr, uid, vals, context=context)
        line_obj=self.pool.get('tour.query.line')
        tr_obj=self.pool.get('tour.ticket')
        trac_obj=self.pool.get('tour.transport')
        vals1={}
        tr_vals2={}
        trc_vals={}

        if context is None:
            context = {}
        if vals.get('days')>0:
            for day in range (vals.get('days')+1):
                name2='Day' +str((day+1))
                if day==0:
                    to_date=vals.get('to_date')
                    next_date = datetime.strptime(vals.get('to_date'), '%Y-%m-%d') + relativedelta(days=day+1)
                    #(datetime.strptime(vals.get('to_date'), '%Y-%m-%d') + relativedelta(days=1))
                else :
                    to_date = next_date
                    next_date =(datetime.strptime(vals.get('to_date'), '%Y-%m-%d') + relativedelta(days=day+1))

                vals1.update({'name':name2,'query':new_id,'end_date':next_date,'to_date':to_date})

                tr_vals2.update({'query':new_id,'ticket_date':to_date})
                trc_vals.update({'query':new_id,'from_date':to_date,'to_date':next_date})

                line_obj.create(cr,uid,vals1,context=context)
                tr_obj.create(cr,uid,tr_vals2,context=context)
                trac_obj.create(cr,uid,trc_vals,context=context)
        return new_id

    def onchange_tour_type(self, cr, uid, ids, tour_type, context={}):
        res = {'value': {'name': ''}}
#         if tour_type:
#             if tour_type == 'domestic':
#                 res['value']['name'] = self.pool.get('ir.sequence').get(cr, uid, 'tour.dom') or '/'
#             elif tour_type == 'international':
#                 res['value']['name'] = self.pool.get('ir.sequence').get(cr, uid, 'tour.int') or '/'
        return res

    def write(self, cr, uid, ids, vals, context=None):
        if ids:
            data=self.browse(cr,uid,ids[0],context=context)
            if vals.get('tour_type') == 'domestic':
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'tour.dom') or '/'
            elif vals.get('tour_type') == 'international':
                vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'tour.int') or '/'

            line_obj=self.pool.get('tour.query.line')
            if vals.get('days') and not self.browse(cr,uid,ids[0],context=context).line_ids:
                vals1={}
                for day in range (vals.get('days')):
                    name2='Day' +str((day+1))
                    if day==0:
                        to_date=data.to_date
                        next_date = to_date
                        #(datetime.strptime(vals.get('to_date'), '%Y-%m-%d') + relativedelta(days=1))
                    else :
                        to_date = (datetime.strptime(data.to_date, '%Y-%m-%d') + relativedelta(days=day+1))
                        next_date =to_date
                    vals1.update({'name':name2,'query':ids[0],'end_date':next_date,'to_date':to_date})
                    line_obj.create(cr,uid,vals1,context=context)
        return super(tour_query, self).write(cr, uid, ids, vals, context=context)

class account_invoice(models.Model):
    _inherit ='account.invoice'
    ref_type= fields.Selection([ ('domes','Domestic bookings'), ('international','International booking,'), ('d_ticket','Domestic Ticketing'),
                                 ('domes','Excursion'), ('domes','Domestic bookings'),('e_excursion','Excursion'),('t_tra','Transport'),('passport','Passport'),('i_ticket','International Ticketing') ],'Type')

    hotel_id=fields.Many2one('tour.hotel', 'Hotel')
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor')

    def write(self, cr, uid, ids, vals, context=None):
        res=super(account_invoice, self).write(cr, uid, ids, vals, context=context)
        if vals.get('internal_number'):
            dt=self.browse(cr,uid,ids[0])
            if dt.ref_type:
                new_name=vals.get('internal_number').split('/')
                new_name[0]=dt.ref_type
                t_name='/'.join(new_name)
                vals['internal_number']=t_name
        return res
    
    
    
class sale_order(models.Model):
    _inherit ='sale.order' 
    dis_all= fields.Boolean('Display line')
    tour_id = fields.Many2one(
        'tour.package',
        'Tour Package',
    )     
       
    hote_id=fields.Many2one('tour.hotel', 'Hotel') 
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor')        
       
class sale_order_line(models.Model):
    _inherit ='sale.order.line' 
    vendor_id=fields.Many2one('tour.hotel.vender', 'Vendor')        
    
# class email_template(models.Model):
#     _inherit ='email.template' 
#     
#     @api.cr_uid_id_context
#     def send_mail(self, cr, uid, template_id, res_id, force_send=False, raise_exception=False, context=None):
#         res=super(email_template, self).send_mail(cr, uid,  template_id, res_id, force_send, raise_exception, context)
#         if context.get('active_model')=='tour.query':
#             print "======================================================",res_id
#             for da in case.all_ids:
#                 if da.send_mail:
#                     template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'tour', 'email_template_hotel')[1]
#                     temp_obj.send_mail(cr, uid,
#                                             template_id,
#                                             da.hotel_id,id, context=context)          
#         print a
#         return msg_id       

