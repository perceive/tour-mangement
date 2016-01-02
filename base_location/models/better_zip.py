# -*- coding: utf-8 -*-
#
#
#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Contributor: Pedro Manuel Baeza <pedro.baeza@serviciosbaeza.com>
#                 Ignacio Ibeas <ignacio@acysos.com>
#                 Alejandro Santana <alejandrosantana@anubia.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from openerp import models, fields, api


class BetterZip(models.Model):
    '''City/locations completion object'''

    _name = "res.better.zip"
    _description = __doc__
    _order = "name asc"
    _rec_name = "display_name"

    display_name = fields.Char('Name', compute='_get_display_name', store=True)
    name = fields.Char('ZIP')
    code = fields.Char('City Code', size=64,
                       help="The official code for the city")
    city = fields.Char('City', required=True)
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')
    day_description = fields.One2many('day.description','res_better_zip_id',string='Description')

    @api.one
    @api.depends(
        'name',
        'city',
        'state_id',
        'country_id',
        )
    def _get_display_name(self):
        print "====================================================================="
#         if self.name:
#             name = [self.name, self.city]
#         else:   
        name = [self.city]
        if self.state_id:
            name.append(self.state_id.name)
        if self.country_id:
            name.append(self.country_id.name)
        if self.name:
            name.append(self.name)
        self.display_name = ", ".join(name)

    @api.onchange('state_id')
    def onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id

    @api.v7
    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=100):
        if context.has_key("state_id"):
            print "context get state id",context.get('state_id')[0][2]
            ids = self.search(cr, user, [('state_id','in',context.get('state_id')[0][2])],limit=limit, context=context)
            return self.name_get(cr, user, ids, context=context)
        if context.has_key('query'):
            tour_query_obj = self.pool.get('tour.query')
            tour_query = tour_query_obj.browse(cr,user,context.get('query'),context)
            print "aasdasdasdasd uuuuuuuuuu",tour_query.location_id.ids
            if tour_query.location_id.id:
                ids = self.search(cr, user, [('id','=',tour_query.location_id.id)],limit=limit, context=context)
                print "iiiiiiiiiiiiiiiiddddddddddddddddsssssssss",ids
        ids = self.search(cr, user, [],limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)

    # @api.onchange('day_description')
    # def onchange_description(self):
    #     day_c = len(self.day_description)
    #     print "callllllll onchange"
        # self.day_description = [(0,0,{'day':day_c + 1})]
        # print day_c
        # self.day_description.with_context(day=day_c+1).default_get(['day','Description'])


class BetterZipLine(models.Model):

    _name = "day.description"

    days = fields.Char('Days')
    Description = fields.Char('Description')
    res_better_zip_id = fields.Many2one('res.better.zip')

    # @api.model
    # def default_get(self,fields):
    #     res = super(BetterZipLine, self).default_get(fields)
    #     print "--------default get callllll-----cont-------",self._context.get('day')
    #     if self._context.has_key('day') and self._context.get('day'):
    #         print "iiiiiiiiiiiffffffffff"
    #         res['day'] = self._context.get('day')
    #     return res

    # @api.model
    # def create(self,vals):
    #     res = super(BetterZipLine, self).create(vals)
    #     print "createeeeeeee",self
    #     print "valsssssssss",vals
    #     return res

