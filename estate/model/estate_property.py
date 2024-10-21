from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"
    
    def _default_vailability() :
        
        """
        this function sets the default vailability date in three month counting from the current date
        """
         
        #Get today's date
        today = fields.Date.today() 
        
        #Add three months to the current date  
        avail_date  = today + relativedelta(months = 3)
         
        return avail_date
    
    
    name = fields.Char(
        required=True,
    )
    
    active  =  fields.Boolean(
        default= True
        
    )
    
    state  =  fields.Selection(

        [
            ('new', 'New'),
            ('offer_received', 'Offer Received') , 
            ('offer_accepted', 'Offer Accepted') , 
            ('sold' , 'Sold') , 
            ('canceled' , 'Canceled')
            
        ] , 
        required=True  , 
        copy=False  , 
        default  = 'new'
    )
    
    
    
    description = fields.Text()
    
    postcode = fields.Char()

    date_availability = fields.Date(
        copy = False , 
        default  = _default_vailability()
    )

    expected_price = fields.Float()

    selling_price = fields.Float(
        readonly=True , 
        copy= False
        
    )
    
    bedRooms = fields.Integer(
        default  = 2
    )
    
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
