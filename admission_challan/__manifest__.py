{
    "name": "Admission Challan",
    "version": "1.0.0",
    "author": "Malaika Gohar",
    "sequence": -100,
    "summary": "Create admission challan.",
    "description": "",
    "depends": ["base", "ol_school_account", "ol_school_manager"],
    "data": [
            "security/ir.model.access.csv",
            # "data/server_action_multiple_admission_challan.xml",
            "views/admission_challan_view.xml" ,  
            "views/tuition_template_view.xml" ,  
            "wizard/create_admission_challan.xml",
            
    ],
    "demo": [],
    "auto_install": False,
    "license": "LGPL-3",
    "application": True,
    "installable": True,
}
