from odoo import fields, models  # type: ignore


class ModelName(models.Model):
    _name = 'estate.propery.types'
    _description = 'Property Type'

    name = fields.Char(
        required=True,
    )
