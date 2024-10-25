from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"

    def _default_vailability():

        """
        this function sets the default vailability date in three month counting from the current date
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

    name = fields.Char(
        required=True,
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
        copy=False

    )

    bedRooms = fields.Integer(
        default=2
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

        default=lambda self: self.env.user
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
        if self.date_availability < fields.Date.today():
            return {
                "warning": {
                    "title": 'Value error',
                    "message": 'The date should not be prior to the current Dat'
                }
            }
