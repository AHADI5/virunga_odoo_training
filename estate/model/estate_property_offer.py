from odoo import fields , models  


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'


    price  = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'), 
        ],
        copy=False
    )
    partner_id  = fields.Many2one(
        string='Partner ' ,
        comodel_name='estate.property',
    )
    
    property_id = fields.Many2one(
        string='Property' ,
        comodel_name='estate.property',
    )
    
    
    
    

    