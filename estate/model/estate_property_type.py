from odoo import fields, models  # type: ignore


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Property Type'

    # Sql constraints

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name >= 0)", "Tag name must be unique"),
    ]
    name = fields.Char(
        required=True,
    )

    property_ids = fields.One2many("estate.property", "property_type_id")
