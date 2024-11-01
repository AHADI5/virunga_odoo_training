from odoo import fields, models  , _   , api # type: ignore


class EstatePropertyType(models.Model):
    _name = 'estate.property.types'
    _description = 'Property Type'

    #Ordering
    #_order = 'name'

    _order = 'sequence desc'


    # Sql constraints

    _sql_constraints = [
        ("unique_type_name", "UNIQUE(name >= 0)", "Tag name must be unique"),
    ]
    name = fields.Char(
        required=True,
    )

    offer_ids =  fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_type_id',
        string='Offers',
        required=False
    )

    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer()
    count_properties = fields.Integer(compute='_count_properties')
    count_offers  =  fields.Integer(compute='_count_offers')

    @api.depends('property_ids')
    def _count_properties(self):
        self.count_properties = len(self.property_ids)

    @api.depends('offer_ids')
    def _count_offers(self):
        self.count_offers = len(self.offer_ids)

    def open_property_house_form(self) :
        return {
            "name" : _("Property House") ,
            "type" :  "ir.actions.act_window",
            "view_mode"  : "tree,form"  ,
            "res_model" : "estate.property" ,
            "target" : "current" ,
            "domain" : [("property_type_id" , "=" , self.id)],
            "context" : {
                "default_property_type_id" : self.id
            }
        }

    def open_offer_form(self) :
        return {
            "name" : _("Property Offers") ,
            "type" :  "ir.actions.act_window",
            "view_mode"  : "tree,form"  ,
            "res_model" : "estate.property.offer" ,
            "target" : "current" ,
            "domain" : [("property_type_id" , "=" , self.id)],
            "context" : {
                "default_property_type_id" : self.id
            }
        }
