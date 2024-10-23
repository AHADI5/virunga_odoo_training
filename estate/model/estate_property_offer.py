from odoo import fields , models

class EstatePropertyOffer(models.Model):
    property_type_id = fields.Many2one(
        string='Property Type',
        related='property_id.propety_type_id'  , 
        store=True
    )
    
    