import logging

from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from pyparsing import empty


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one(
        string='Partner ',
        comodel_name='res.partner',
        required=True
    )

    property_id = fields.Many2one(
        string='Property',
        comodel_name='estate.property',
        required=True
    )

    property_type_id = fields.Many2one(
        string='Property Type',
        related='property_id.property_type_id',
        store=True
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline'
    )

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    #Actions

    def accept_offer(self):

        # checking whether there is an offer accepted for a particular property
        isOrderAccepted = [ offer for offer in self.property_id.offer_ids if offer.status == 'accepted']
        if len(isOrderAccepted) == 0:
            self.status = 'accepted'
        else :
            raise UserError("Only One Offer can be accepted for this property")

    def refuse_offer(self):
        self.status = 'refused'


