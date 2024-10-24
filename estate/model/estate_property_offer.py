from odoo import fields, models, api
from datetime import datetime, timedelta


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

    validity = fields.Integer(default=7)
    ceate_date = fields.Date(default=fields.Date.context_today)
    date_deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline'
    )

    @api.depends('validity', 'create_date')
    def _compute_field(self):
        for record in self:
            record.date_deadline = record.create_date + \
                timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - record.create_date).days
