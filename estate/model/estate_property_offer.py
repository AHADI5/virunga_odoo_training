from odoo import fields , models

class EstatePropertyOffer(models.Model):
    property_type_id = fields.Char(
        string='Property Type',
        related='property_id.propety_type_id'
    )
    
    