{
    "name": "Estate",
    "version": "17.0.1.0.0",
    "license": "OEEL-1",
    "depends": ["base"],

     
     """data"""  
     
     #demo data
     "demo" : [
       "demo/demo.xml"  
     ],
     
     
     "data" : [
         #Security data 
        "security/res_groups.xml" ,
        "security/ir.model.access.csv" ,
        
        #views data 
        "views/estate_property_views.xml" ,
        "views/estate_menu.xml" , 
        
     ] , 

    
  
    
    "application": True,
    "data" :  [ 
        "views/estate_menu.xml" , 
        "views/estate_property_views.xml"
        
    ]
}
