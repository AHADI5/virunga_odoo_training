from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'

    #Ordering
    _order = 'name'

    # Sql constraints

    _sql_constraints = [
        ("excepted_unique_name", "UNIQUE(name)", "A tag name must be unique"),
    ]
    name = fields.Char(required=True)
    color = fields.Integer()
