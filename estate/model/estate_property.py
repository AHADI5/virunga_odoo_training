from email.policy import default

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError ,  ValidationError

class Property(models.Model):
    _name = "estate.property"
    _description = "Property"

    #Sql constraints

    _sql_constraints = [
        ("positive_expected_price", "CHECK(expected_price > 0)", "The Expected price must be strictly  positive"),
        ("positive_selling_price", "CHECK(selling_price >= 0)", "The Expected price must be strictly  positive"),
        ("property_unique_name" , "UNIQUE(name)", "The property name must be unique")

    ]

    def _default_vailability():

        """
        this function sets the default availability date in three month counting from the current date
        """

        # Get today's date
        today = fields.Date.today()

        # Add three months to the current date
        avail_date = today + relativedelta(months=3)

        return avail_date

    name = fields.Char(
        required=True,
    )

    active = fields.Boolean(
        default=True

    )

    state = fields.Selection(

        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')

        ],
        required=True,
        copy=False,
        default='new'
    )

    description = fields.Text()

    postcode = fields.Char()

    date_availability = fields.Date(
        copy=False,
        default=_default_vailability()
    )

    expected_price = fields.Float()

    selling_price = fields.Float(
        readonly=True,
        copy=False ,
        default = 0
    )

    bed_rooms = fields.Integer(
        default=2
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

    property_type_id = fields.Many2one(
        string='Type',
        comodel_name='estate.property.types',
    )

    partner_id = fields.Many2one(
        string='Buyer',
        comodel_name='res.partner',
        copy=False
    )

    sales_person_id = fields.Many2one(
        string='Sales Person',
        comodel_name='res.users',
        default=lambda self: self.env.user,
    )

    offer_ids = fields.One2many(
        string='Offers',
        comodel_name='estate.property.offer',
        inverse_name='property_id',
    )

    tag_ids = fields.Many2many(
        string='Tags',
        comodel_name='estate.property.tag',
    )

    # Computed field

    best_price = fields.Float(compute='_best_price')
    total_area = fields.Integer(compute='_compute_total_area')

    @api.depends('offer_ids.price')
    def _best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):

        for record in self:
            # Handling null values
            record.total_area = record.living_area + record.garden_area

    @api.onchange('gardern')
    def _onchange_garden(self):
            if self.gardern:
                self.garden_area = 10
                self.gardern_orientation = 'north'
            else:
                self.garden_area = 0
                self.gardern_orientation = ''

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                return {
                    "warning": {
                        "title": 'Value error',
                        "message": 'The date should not be prior to the current Dat'
                    }
                }

    # actions method
    def sell_property(self):

        """this method sets a property state to sold , if it's not cancelled"""

        if self.state == 'canceled':
            raise UserError("A canceled property cannot be sell.")
        else:
            self.state = 'sold'

    def cancel_sold_property(self):

        """this method sets a property state to cancel , if it's not sold"""

        if self.state == 'sold':
            raise UserError("A sold property cannot be canceled.")
        else:
            self.state = 'canceled'
 

    @api.onchange('gardern')
    def _onchange_garden(self):

        if self.gardern:
            self.garden_area = 10
            self.gardern_orientation = 'north'
        else:
            self.garden_area = 0
            self.gardern_orientation = ''

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        if self.date_availability < fields.Date.today():
            return {
                "warning": {
                    "title": 'Value error',
                    "message": 'The date should not be prior to the current Dat'
                }
            }
    #Selling price constraint
    @api.constrains('selling_price')
    def _selling_price_validation(self):
        #Check whether there is no offer yet validated
        isOrderAccepted = [offer for offer in self.offer_ids if offer.status == 'accepted']

        if self.selling_price < ((90 * self.expected_price) / 100) and len(isOrderAccepted)  != 0 :
            raise ValidationError (
                "The selling price cannot be lower than 90% of the expected price"
            )












    

