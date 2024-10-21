from odoo import fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"
    
    name = fields.Char(
        required=True,
    )
    
    description = fields.Text()
    
    postcode = fields.Char()

    date_availability = fields.Date(
        required=True,
    )

    expected_price = fields.Float()

    selling_price = fields.Float(
        required=True,
    )
    
    bedRooms = fields.Integer()
    
    living_area = fields.Integer()
    
    facades = fields.Integer()
    
    garage = fields.Boolean()
    
    gardern = fields.Boolean()
    
    garden_area = fields.Integer()
    
    gardern_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "West"),
        ]
    )
