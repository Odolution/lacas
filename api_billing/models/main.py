from odoo import http, _
from odoo.osv import expression
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
import json
from werkzeug.wrappers import Response
from datetime import datetime, date, timedelta
import string
import random
import os 
# from werkzeug.wrappers import Request, Response



class Billing(http.Controller):

    def __init__(self):
        self.token_length=25
        self.refresh_token_length=20

        #read all configurations
        # config=json.load(open("config.json"))
        # self.token_length=config["length"]
        # self.refresh_token_length=config["length_2"]

    def generate_token(self,token_length):
        characterList = ""
        characterList += string.ascii_letters
        characterList += string.digits
        for i in string.punctuation:
            if i in ['!','@','#','%','^','&','*','(',')','-','=']:
                characterList += i

        password_1=[]
        for i in range(token_length):
            randomchar = random.choice(characterList)
            password_1.append(randomchar)
        generated_token=''.join(password_1)
        return generated_token

    @http.route(['/get_user'], type='http', auth="public")

    def get_user(self):

        return Response(json.dumps({'user':request.env.user.name}), content_type="application/json", status=200)
        
    @http.route(['/get_voucher_info'], type='http', auth="public", website=True, sitemap=False)

    def get_voucher_info(self):

        voucher_id = request.params.get('billId')
        headers = request.httprequest.headers

        # Retrieve the "Authorization" header
        auth = headers.get('Authorization', '')

        is_invalid_auth=False
        try:
            if not auth or auth[0:7] != "Bearer ":
                is_invalid_auth=True
        except:
            is_invalid_auth=True

        if is_invalid_auth:    
            return Response(json.dumps({
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Invalid Authentication Method", "Description": "Authentication Error : Invalid Authentication method used. Only Bearer Token method is supported.", "Errors": [

                            "invalid.authentication.method"],

                        "Error": [

                            {

                                "errorCode": "invalid.authentication.method",

                                "errorContext": "Authentication Error : Invalid Authentication method used. Only Bearer Token method is supported."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                            }
                    }), content_type="application/json", status=401)

    
        try:
            #verify_token=models.execute_kw(db, uid, password, 'api.users', 'search', [[['token', '=',auth[7:]]]])
            verify_token= request.env['api.users'].sudo().search([('token', '=',auth[7:])],limit=1)
            if not verify_token:
                return Response(json.dumps({
                    "Status": {
                        "StatusCode": 5000,
                        "Message": "Invalid Token Provided", "Description": "Authentication Error : Invalid Token Provided.", "Errors": [
                            "invalid.token.provided"],
                        "Error": [
                            {
                                "errorCode": "invalid.token.provided",
                                "errorContext": "Authentication Error : Invalid Token Provided."
                            }
                        ]
                    },
                    "Data": None,
                    "Navigation": {"prevLink": None,
                                "nextLink": None,
                                "totalPages": 0,
                                "totalCount": 0,
                                "filteredCount": 0
                                }
                }), content_type="application/json", status=401)    ##extract voucher info
            move_ids= request.env['account.move'].sudo().search([('name', '=', str(voucher_id)),('state', '=', 'posted')],limit=1)
            if not move_ids:
                move_ids= request.env['account.move'].sudo().search([('name', '=','0'+str(voucher_id)),('state', '=', 'posted')],limit=1)


            if not move_ids:
                return Response(json.dumps({'move_id':move_ids,'voucher_no':voucher_id}), content_type="application/json", status=200)
            
                return Response(json.dumps({
                    "Status": {
                        "StatusCode": 5000,
                        "Message": "Invalid billId", "Description": "Resource Not Found Error : Provided bill id does not exist.", "Errors": [
                            "invalid.bill.id"],
                        "Error": [
                            {
                                "errorCode": "invalid.bill.id",
                                "errorContext": "Resource Not Found Error : Provided bill id does not exist."
                            }
                        ]
                    },
                    "Data": None,
                    "Navigation": {"prevLink": None,
                                "nextLink": None,
                                "totalPages": 0,
                                "totalCount": 0,
                                "filteredCount": 0
                                }
                }), content_type="application/json", status=200)

            if move_ids['payment_state']=='paid':
            
                return Response(json.dumps({
                        "Status": {
                                        "StatusCode": 700,
                                        # "BillStatusCode": 700,
                                        "Message": "Bill already paid.",
                                        "Description": "Bill is already in it's paid state. No charges remaining.",
                                        "Errors": [],
                                        "Error": []
                        },
                        "Data":'' ,
                        "Navigation": {
                                        "prevLink": None,
                                        "nextLink": None,
                                        "totalPages": 0,
                                        "totalCount": 0,
                                        "filteredCount": 0
                        }
                    }),content_type="application/json", status=200)
            

            mov= move_ids
            obj={}
            obj["billId"]=str(mov["name"]) 
            obj["BillingMonth"]=str(mov["bill_date"]) 
            obj["dueDate"]=str(mov["invoice_date_due"]) if "invoice_date_due" in mov else None
            # obj["dueAmount"]=str(mov["amount_residual"]+mov['late_fee_compute']) 
            obj["currency"]="PKR" 
            obj["accountIdentifier"]=str(mov["account_identifier"]) if "account_identifier" in mov else None
            obj["applicantMobileNo"]=mov['x_studio_contact_no'] if "x_studio_contact_no" in mov else None
            late_fee= move_ids.get_late_fee_charges()
            # obj["dueAmount"]=move_ids['amount_residual']+late_fee
            obj["amountBeforeDue"]=move_ids['amount_residual']
            obj["amountAfterDue"]=move_ids['amount_residual']+late_fee 
            voucher_status= mov['payment_state'] if "payment_state" in mov else None
            if voucher_status=='paid':
                voucher_code= 'P'
            else:
                voucher_code= 'U'
            obj["Voucher_Status"]=voucher_code
            obj["billedDate"]=str(mov['invoice_date']) if "invoice_date" in mov else None

            obj["DynamicMembers"]={}


            student=False
            if not mov["student_ids"]:
                student= request.env['school.student'].sudo().search([('id', 'in',[mov['x_student_id_cred']['id']])],limit=1)
            else:
                student= request.env['school.student'].sudo().search([('id', 'in',[mov["student_ids"][0]['id']])],limit=1)



            if not student:
                return Response(json.dumps({'status': 'Error',"message": "Validation Error : Provided billId has no student tagged. This voucher cannot be payed.","code":204}),content_type="application/json", status=200)

            ths_student=student


            # obj["applicantName"]=str(ths_student["name"])
            # obj["applicantId"]=str(ths_student["olf_id"])
            # obj["Student_Father_Name"]=mov['partner_id']['name']
        # extra condition
            if mov['x_studio_is_manual_record']==False:
                obj["applicantName"]=str(ths_student["name"])
                obj["applicantId"]=str(ths_student["olf_id"])
                obj["Student_Father_Name"]=mov['partner_id']['name']
            else:
                obj["applicantName"]=str(mov["x_studio_current_student_name"])
                obj["applicantId"]=str(mov['x_studio_current_fid'])
                obj["Student_Father_Name"]=str(mov["x_studio_father"]) 
        # extra condition
        
            obj["billedDate"]=str(mov["invoice_date"])
            #end test
            return Response(json.dumps({
                    "Status": {
                                    "StatusCode": 600,
                                    # "BillStatus": 600,
                                    "Message": "Success",
                                    "Description": "Success",
                                    "Errors": [],
                                    "Error": []
                    },
                    "Data": dict(obj),
                    "Navigation": {
                                    "prevLink": None,
                                    "nextLink": None,
                                    "totalPages": 0,
                                    "totalCount": 0,
                                    "filteredCount": 0
                    }
                }),content_type="application/json", status=200)


        except Exception as e:
            return Response(json.dumps({
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Unknown Error", "Description": "Unknown Error Occurred: Please try again or contact administrators.", "Errors": [

                            "unknown.error"],

                        "Error": [

                            {

                                "errorCode": "unknown.error",

                                "errorContext": "Unknown Error Occurred: Please try again or contact administrators."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }), content_type="application/json", status=200)
        





    @http.route(['/mark_voucher_as_payed'], type='json',csrf=False, auth='public', methods=['POST'])
    def mark_voucher_as_payed(self,**post_data):

        ##validate Authentication by checking API key.
        headers = request.httprequest.headers
        # Retrieve the "Authorization" header
        auth = headers.get('Authorization', '')
        is_invalid_auth=False
        try:
            if not auth or auth[0:7] != "Bearer ":
                is_invalid_auth=True
        except:
            is_invalid_auth=True
            
        if is_invalid_auth:
            return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Invalid Authentication Method", "Description": "Authentication Error : Invalid Authentication method used. Only Bearer Token method is supported.", "Errors": [

                            "invalid.authentication.method"],

                        "Error": [

                            {

                                "errorCode": "invalid.authentication.method",

                                "errorContext": "Authentication Error : Invalid Authentication method used. Only Bearer Token method is supported."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }


        verify_token= request.env['api.users'].sudo().search([('token', '=',auth[7:])],limit=1)

        if not verify_token or not auth:
            return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Invalid Token Provided", "Description": "Authentication Error : Invalid Token Provided.", "Errors": [

                            "invalid.token.provided"],

                        "Error": [

                            {

                                "errorCode": "invalid.token.provided",

                                "errorContext": "Authentication Error : Invalid Token Provided."

                            }
                        ]
                    },
                    "Data": None,
                    "Navigation": {"prevLink": None,
                                "nextLink": None,
                                "totalPages": 0,
                                "totalCount": 0,
                                "filteredCount": 0
                                }
                }
                
        ##reading posted data
        request_body = http.request.httprequest.data

        # Parse the JSON data from the request body
        try:
            data = json.loads(request_body)
        except json.JSONDecodeError as e:
            return {'error': 'Invalid JSON data', 'message': str(e)}



        ##validate if all required fields have been provided. if not, return an appropriate error message.
        params={}
        param_keys=["accountIdentifier","billId","bankId","amountReceived"]

        for key in param_keys:
            params[key]=str(data.get(key,""))
            if params[key]=="":

                return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Mandatory Key Missing", "Description": "Validation error : No "+key+" provided. Please provide correct "+key+".", "Errors": [

                            "mandatory.key.missing"],

                        "Error": [

                            {

                                "errorCode": "mandatory.key.missing",

                                "errorContext": "Validation error : No "+key+" provided. Please provide correct "+key+"."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }
                
        ##validate if all required integer fields are actually integers. if not, return an appropriate error message.
        for key in ["amountReceived"]:
            try:
                params[key]=float(params[key])
                params[key]=int(params[key])
            except:
                # return {'check',params[key]}

                return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Mandatory Key Invalid", "Description": "Validation error : Invalid "+ key+" "+params[key]+" provided.", "Errors": [

                            "mandatory.key.invalid"],

                        "Error": [

                            {

                                "errorCode": "mandatory.key.invalid",

                                "errorContext": "Validation error : Invalid "+ key+" "+params[key]+" provided."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }
                
                
        ##retrieve moves for this voucher. If no move, return appropriate error message.
        # move_ids=models.execute_kw(db, uid, password, 'account.move', 'search', [[['name', '=',params["billId"]]]])
        move_ids= request.env['account.move'].sudo().search([('name', '=', params["billId"])],limit=1)

        if not move_ids:
            return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Invalid billId", "Description": "Resource Not Found Error : Provided bill id does not exist.", "Errors": [

                            "invalid.bill.id"],

                        "Error": [

                            {

                                "errorCode": "invalid.bill.id",

                                "errorContext": "Resource Not Found Error : Provided bill id does not exist."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }
        mov=move_ids


        ##validate if invoice has been posted. if not, payment cannot be made. so returning appropriate error message.
        if mov["state"]!="posted":
            return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Invalid billId", "Description": "Validation error : Provided voucher is "+mov["state"]+".Cannot add payment for this invoice.", "Errors": [

                            "invalid.bill.id"],

                        "Error": [

                            {

                                "errorCode": "invalid.bill.id",

                                "errorContext": "Validation error : Provided voucher is "+mov["state"]+".Cannot add payment for this invoice."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }

            
        ##validate if invoice has is yet to be paid. if not, payment cannot be made. so returning appropriate error message.
        if mov["payment_state"] not in ["not_paid","partial","reversed"]:

            return {
                    "Status": {

                        # "StatusCode": 5000,
                        "StatusCode": 700,

                        "Message": "Invalid billId", "Description": "Validation error : Provided voucher is "+mov["payment_state"]+".Cannot add payment for this invoice.", "Errors": [

                            "invalid.bill.id"],

                        "Error": [

                            {

                                "errorCode": "invalid.bill.id",

                                "errorContext": "Validation error : Provided voucher is "+mov["payment_state"]+".Cannot add payment for this invoice."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }

        late_fee= mov.get_late_fee_charges()
        if params['amountReceived'] != mov['amount_residual']+late_fee:
            return {
                    "Status": {

                        "StatusCode": 5000,

                        "Message": "Invalid amount recieved", "Description": "Validation error : Provided amount is not equal to the actual bill amount.", "Errors": [

                            "invalid.amount.received"],

                        "Error": [

                            {

                                "errorCode": "invalid.amount.received",

                                "errorContext": "Validation error : Provided amount is not equal to the actual bill amount."

                            }
                        ]
                    },
                    "Data": None,

                    "Navigation": {"prevLink": None,

                                "nextLink": None,

                                "totalPages": 0,

                                "totalCount": 0,

                                "filteredCount": 0
                                }
                }
        user_id=  request.env['res.users'].sudo().search([('name','ilike','API')],limit=1)
        data={
                                                            'ref': mov["name"],
                                                            'user_id': user_id.id,
                                                            'payment_type':'inbound',
                                                            'partner_type': "customer",
                                                            'amount': params["amountReceived"],
                                                            #'date' : params["paymentDate"],
                                                            "partner_id":mov["partner_id"]['id'],

                                                            # 'date' :data['business_date'][counter]
                                                }

        
        create_payment= request.env['account.payment'].sudo().create(data)
        #Reconcile payment, automated action on live, but create in it directly
        if create_payment:

            # if create_payment['user_id']['id'] in [user_id.id,]: ##if payment creator is not API. then just continue
            try:
                invoice=request.env['account.move'].sudo().search([('name','=',create_payment['ref'])])
                
                if invoice:                        
                    if create_payment['state']=="draft":
                        create_payment.sudo().action_post()
                        # return {'chek':'ho','payment_sta':create_payment['state']}
                    invoice.sudo().apply_late_fee_policy()
                    if invoice.amount_total >= invoice.amount_residual:
                        line_id = request.env['account.move.line'].sudo().search([('debit','=',0),('move_id','=',create_payment.move_id.id)])
                        invoice.sudo().js_assign_outstanding_line(line_id.id)
            except:
                pass

        # Reconcile end
        
        update_data = request.env['account.move'].sudo().browse(int(move_ids['id']))
        update_data.write({
                            'account_identifier':params["accountIdentifier"],

                                })
        if update_data['payment_state']=='paid':
            status_code= 700
        else:
            status_code= 600




        # return json.dumps({
        return {

                    "Status": {

                                    "StatusCode": 201,
                                    # "StatusCode": status_code,

                                    # "BillStatus": status_code,

                                    "Voucher_Status": "Paid",

                                    "Message": "Success",

                                    "Description": "Success",

                                    "Errors": [],

                                    "Error": []

                    },

                    "Data": {"requestId":str(create_payment)},

                    "Navigation": {

                                    "prevLink": None,

                                    "nextLink": None,

                                    "totalPages": 0,

                                    "totalCount": 0,

                                    "filteredCount": 0

                    }

                }
    



    @http.route(['/get_token_info'], type='json', auth='public', methods=['POST'])
    def get_token_info(self,**post_data):

        try:
            request_body = http.request.httprequest.data
            

            # Parse the JSON data from the request body
            try:
                data = json.loads(request_body)
            except json.JSONDecodeError as e:
                return json.dumps({'error': 'Invalid JSON data', 'message': str(e)})
            type_grant= data.get("grant_type","")
            user_name= data.get("username","")
            # generate a token for user
            if type_grant=="password":
                params={}
                param_keys=["grant_type","username","password"]
                for key in param_keys:
                    params[key]=str(data.get(key,""))
                    if params[key]=="":
                        return json.dumps({'status': 'Error',"message": "Validation error : No "+key+" provided. Please provide correct "+key+".","code":204,"object":"obj"})
                # Username and password verification
                username_search= request.env['api.users'].sudo().search([('username', '=', params["username"]),('password', '=',params["password"])],limit=1)
                if not username_search :
                    return json.dumps({'status': 'Error',"message": "Validation error : wrong "+key+" provided. Please provide correct "+key+".","code":204,"object":"obj"})
                idss=username_search['id']

                
                #expirydate a month
                
                
                unexpired_token= request.env['api.users'].sudo().search([('username', '=', params["username"]),('password', '=',params["password"])],limit=1)
                obj={}
                today = datetime.now().date()

                
                if not unexpired_token['token'] or not unexpired_token['token_refresh'] or unexpired_token['token_expiry']<today:
                    expire_date=today + timedelta(days=30)
                    days_after=expire_date
                    diff = expire_date -today
                    diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)

                    #generate token on odoo
                    token=self.generate_token(self.token_length)
                    refreshtoken=self.generate_token(self.refresh_token_length)
                    update_data = request.env['api.users'].sudo().search([('id','=',int(idss))],limit=1)
                    update_data.write({
                                'token':token,
                                'token_expiry':days_after,
                                'token_refresh':refreshtoken,

                                            })                       

                                       
                    mov=username_search
                    obj["access_token"]=str(token)
                    obj["token_type"]="bearer"
                    obj["expires_in"]=str(diff_minutes)
                    obj["refrest_token"]=str(refreshtoken)
                    obj[".issued"]=(str(mov["write_date"]))
                    obj[".expires"]=(str(mov["token_expiry"]))
                    

                else:
                    rec=unexpired_token
                    obj["access_token"]=str(rec['token'])
                    obj["token_type"]="bearer"
                    expire_date=rec['token_expiry']
                    diff = expire_date -today
                    diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
                    obj["expires_in"]=str(diff_minutes)


                    obj["refrest_token"]=rec['token_refresh']
                    obj[".issued"]=str(rec["write_date"])
                    obj[".expires"]=str(rec["token_expiry"])

                return json.dumps(dict(obj))

            #if existing user want to change/refresh token
            elif type_grant=="refresh_token":
                params={}
                param_keys=["grant_type","refresh_token"]
                old_token= data.get("refresh_token",False)

                #parameter criteria
                for key in param_keys:
                    params[key]=str(data.get(key,""))
                    if params[key]=="":

                        return json.dumps({'status': 'Error',"message": "Validation error : No "+key+" provided. Please provide required "+key+".","code":204,"object":"obj"})


                #check that token if exists in odd
                token_check= request.env['api.users'].sudo().search([('token_refresh', '=', old_token)],limit=1)

                #if exists create new tokens
                if token_check:
                    #expirydate a month
                    today = datetime.today().date()
                    expire_date=today + timedelta(days=30)
                    days_after=expire_date
                    diff = expire_date -today
                    diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
                    #refresh token in odoo
                    ids=token_check['id']
                    token=self.generate_token(self.token_length)
                    refreshtoken=self.generate_token(self.refresh_token_length)
                    update_token = request.env['api.users'].sudo().browse(int(ids))
                    update_token.write({
                                'token':token,
                                'token_expiry':days_after,
                                'token_refresh':refreshtoken,
                                            })

                    obj={}
                    movs= request.env['api.users'].sudo().search([('id', '=', int(ids))],limit=1)

                    mov=movs
                    obj["access_token"]=str(token)
                    obj["token_type"]="bearer"
                    obj["expires_in"]=str(diff_minutes)
                    obj["refrest_token"]=str(refreshtoken)
                    obj[".issued"]=str(mov["write_date"])
                    obj[".expires"]=str(mov["token_expiry"])
                    return json.dumps(dict(obj))
                else:
                    return json.dumps({'status': 'failed',"message": "No Such Token exists.","code":204,"object":{}})
            else:
                return json.dumps({'status': 'failed',"message": "Missing Grant type or invalid Grant type","code":200,"object":{}})


        except Exception as e:
             return json.dumps({'status': 'Error',"message": "Unknown Error Occurred.","code":201})



