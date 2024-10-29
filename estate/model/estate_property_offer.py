import logging

from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError



class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    #Ordering
    _order = 'price desc'

    # Sql constraints

    _sql_constraints = [
        ("positive_offer_price", "CHECK(price > 0)", "The offer price must be strictly  positive"),
    ]

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
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else  :
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    # Actions

    def accept_offer(self):
        # checking whether there is an offer accepted for a particular property
        isOrderAccepted = [offer for offer in self.property_id.offer_ids if offer.status == 'accepted']
        if len(isOrderAccepted) == 0:
            self.status = 'accepted'
            self.property_id.selling_price  = self.price
            self.property_id.partner_id= self.partner_id
        else:
            raise UserError("Only One Offer can be accepted for this property")

    def refuse_offer(self):
        self.status = 'refused'
        self.property_id.selling_price = 0
