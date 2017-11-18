# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Make(models.Model):
    _name = "crm.make"
    _description = "Make"
    _rec_name = 'name'

    name = fields.Char('Make Name', required=True, translate=True)

class Model(models.Model):
    _name = "crm.model"
    _description = "Model"
    _rec_name = 'name'

    name = fields.Char('Model Name', required=True, translate=True)
    make_name = fields.Many2one('crm.make', string='Make Name', index=True,
        help="Make Name Linked to the Model Name")


class Variant(models.Model):
    _name = "crm.variant"
    _description = "Variant"
    _rec_name = 'name'

    name = fields.Char('Variant Name', required=True, translate=True)
    model_name = fields.Many2one('crm.model', string='Model Name', index=True,
        help="Model Name Linked to the Variant Name")


class Lead(models.Model):
    _inherit = 'crm.lead'

    make_id = fields.Many2one('crm.make', string='Make Name', track_visibility='onchange',index=True,
        help="Make Name")
    models_id = fields.Many2one('crm.model', string='Model Name', track_visibility='onchange',index=True,
        help="Model Name")
    variant_id = fields.Many2one('crm.variant', string='Variant Name', track_visibility='onchange', index=True,
        help="Variant Name")


    @api.model
    def _onchange_make_id_values(self, make_id):
        """ returns new values when user_id has changed """
        make=False
        if make_id:
            search_domain = [('make_name','=',make_id)]
            make_search = self.env['crm.model'].search(search_domain, limit=1)
            make = self.env['crm.model'].browse(make_search).id
            if not make:
                return {}
        model_id = make
        return {'models_id': model_id}

    @api.onchange('make_id')
    def _onchange_make_id(self):
        """ When changing the user, also set a team_id or restrict team id to the ones user_id is member of. """
        values = self._onchange_make_id_values(self.make_id.id)
        self.update(values)


    @api.model
    def _onchange_models_id_values(self, models_id):
        """ returns new values when user_id has changed """
        model=False
        if models_id:
            search_domain = [('model_name','=',models_id)]
            models_search = self.env['crm.variant'].search(search_domain, limit=1)
            model = self.env['crm.variant'].browse(models_search).id
            if not model:
                return {}
        variant_id = model
        return {'variant_id': variant_id}

    @api.onchange('models_id')
    def _onchange_models_id(self):
        values = self._onchange_models_id_values(self.models_id.id)
        self.update(values)


