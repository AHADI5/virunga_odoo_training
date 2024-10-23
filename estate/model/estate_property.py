from odoo import fields, models , api  


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
    
    property_type_id  = fields.Many2one(
        string='Type',
        comodel_name='estate.property.types',
    )
    
    partner_id  = fields.Many2one(
        string='Buyer',
        comodel_name='res.partner',
        copy=False
    )
    
    sales_person_id =  fields.Many2one(
        string='Sales Person',
        comodel_name='res.users',
        
        default=lambda self: self.env.user
    )
    
    offer_ids  =   fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_id',
    )
    
    tag_ids  = fields.Many2many(
        string='Tegs',
        comodel_name='estate.property.tag',
    )
    
    #Computed field
    
    best_price  =  fields.Float(compute = '_best_price')
    
    
    @api.depends('offer_ids.price')
    def _best_price(self) :  
        for record in self :
            record.best_price = max(offer.price for offer in record.offer_ids ) 
            
    
    
    
    
    
