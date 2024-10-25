from odoo import fields, models  # type: ignore


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Property Type'

    name = fields.Char(
        required=True,
    )
