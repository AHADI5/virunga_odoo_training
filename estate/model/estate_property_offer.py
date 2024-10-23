from odoo import fields, models


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
<<<<<<< HEAD
    
    property_type_id = fields.Many2one(
        string='Property Type',
        related='property_id.property_type_id', 
        store=True
    )
    
    
=======
>>>>>>> computed_fields
