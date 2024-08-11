from django.shortcuts import render
from . models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate,login
import base64
from django.core.files.base import ContentFile
from django.core import serializers
from datetime import datetime
from django.db.models import Q
from datetime import date
from datetime import datetime, date
from datetime import datetime, timezone
from datetime import timezone
import secrets
import string

from django.core.mail import send_mail, EmailMessage

# Create your views here.


def travelmate(request):
    APICALL=request.GET['apicall']
    print(APICALL)
    match APICALL:
        case "UserRegister":
            users.objects.create_user(
                    username = request.GET['email'],
                    name=request.GET['name'],
                    email = request.GET["email"],
                    password =request.GET["password"],
                    phone =request.GET["phone"],
                    usertype=0,
                    is_active=1
            )
            return JsonResponse({'status' : '201', 'result': 'true', 'data' : 'User Registeration Successful!'})


        case "BusOwnerRegister":
            image=request.GET['busprofile']
            print(image)
            image_name=request.GET['busprofilename']
            print(image_name)
            image_data=base64.b64decode(image)
            print(image_data)
            image_file=ContentFile(image_data,name=image_name + ".jpg")
            users.objects.create_user(
                    username = request.GET['email'],
                    name=request.GET['name'],
                    email = request.GET["email"],
                    password =request.GET["password"],
                    phone =request.GET["phone"],
                    hoteladdress =request.GET["busaddress"],
                    busprofile=image_file,
                    usertype=2,
                    is_active=0
            )
            return JsonResponse({'status' : '201', 'result': 'true', 'data' : 'User Registeration Successful!'})


        case "HotelOwnerRegister":
            image=request.GET['busprofile']
            print(image)
            image_name=request.GET['busprofilename']
            print(image_name)
            image_data=base64.b64decode(image)
            print(image_data)
            image_file=ContentFile(image_data,name=image_name + ".jpg")
            users.objects.create_user(
                    username = request.GET['email'],
                    name=request.GET['name'],
                    email = request.GET["email"],
                    password =request.GET["password"],
                    hotelname =request.GET["hotelname"],
                    hoteladdress =request.GET["hoteladdress"],
                    phone =request.GET["phone"],
                    busprofile=image_file,
                    usertype=3,
                    is_active=0
            )
            return JsonResponse({'status' : '201', 'result': 'true', 'data' : 'User Registeration Successful!'}) 



        case "Login":
            username = request.GET['email']
            password = request.GET['password']
            user = authenticate(request, username=username, password=password,is_active=1)
            print(username)
            print(password)
            print(user)
            if user is None:
               return JsonResponse({'ResponseCode': '409', 'Result': 'true', 'ResponseMsg': 'Signup with your Account!'}) 
            else:
                login(request, user)
                r = users.objects.get(username=user)
                request.session['unm'] = r.username
                usrn=r.username
                request.session['unme'] = r.name
                usrname=r.name
                request.session['ut'] = r.usertype
                u=r.usertype
                request.session['userid'] = r.id
                i=r.id
                request.session['ph'] = r.phone
                p=r.phone
                k=users.objects.get(id=i)
                return JsonResponse({'status' : '201', 'result': 'true', 'data' :[{"email":usrn,"name":usrname,"id":i,"usertype":u,"phone":p}]}) 


        case "Busrequests":
            row= users.objects.filter(usertype=2,is_active=0,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                dic['busprofile']=str(i.busprofile)
                det.append(dic)
                print(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "Hotelrequests":
            row= users.objects.filter(usertype=3,is_active=0,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                dic['busprofile']=str(i.busprofile)
                dic['hotelname']=i.hotelname
                dic['hoteladdress']=i.hoteladdress
                det.append(dic)
                print(dic)
            print(det)    
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})  


        case "Approval":
            approvalid=request.GET['aid']
            r = users.objects.get(id=approvalid)
            r.is_active=1
            r.save()
            subject = 'You Are Approved!!!!!!!!'
            message = 'Now that you have been approved by the tour and travel administrator, you can proceed to log in and initiate collaborative efforts for our corporate endeavors.'
            project_name = 'Tour And Travel'
            from_email =  'Tour And Travel🚌🏨🌏🌏🌏 <xxxxxxxxx@gmail.com>'
            recipient_list = [r.email]
            send_mail(subject, message, from_email, recipient_list)
            email = EmailMessage(subject, message,from_email=from_email,to=recipient_list)
            email.send()
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'APPROVED!'})

            
        case "Reject":
            approvalid=request.GET['rid']
            r = users.objects.get(id=approvalid)
            r.status=1
            r.save()
            subject = 'Sorry You Are Rejected!!'
            message = 'According to our security credentials, your request has been denied by the Tour and Travel Administrator. You are currently unable to log in. Please attempt to log in again with accurate details.'
            project_name = 'Tour And Travel'
            from_email = 'Tour And Travel🚌🏨🌏🌏🌏 <xxxxxxxxx@gmail.com>'
            recipient_list = [r.email]
            send_mail(subject, message, from_email, recipient_list)
            email = EmailMessage(subject, message, from_email= from_email, to=recipient_list)
            email.send()
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'Rejected!'})  


        case "RejectedBusUsers":
            RejUsers=users.objects.filter(usertype=2,is_active=0,status=1)
            det=[]
            for i in RejUsers:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                dic['busprofile']=str(i.busprofile)
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})


        case "RejectedHotelUsers":
            RejUsers=users.objects.filter(usertype=3,is_active=0,status=1)
            det=[]
            for i in RejUsers:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                dic['busprofile']=str(i.busprofile)
                det.append(dic)
                print(dic)
            print(det)    
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})


        case "deletehistory":
            id=request.GET['id']
            r = users.objects.get(id=id)
            r.delete()
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'Deleted!'})


        case "Busownerlist":
            row= users.objects.filter(usertype=2,is_active=1,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                dic['busprofile']=str(i.busprofile)
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})  


        case "Hotelownerlist":
            row= users.objects.filter(usertype=3,is_active=1,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                dic['busprofile']=str(i.busprofile)
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "Userslist":
            row= users.objects.filter(usertype=0,is_active=1,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['username']=i.username
                dic['name']=i.name
                dic['email']=i.email
                dic['phone']=i.phone
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})  


        case "AddBuses":
            image=request.GET['busprofile']
            image_name=request.GET['busprofilename']
            image_data=base64.b64decode(image)
            image_file=ContentFile(image_data,name=image_name + ".jpg")
            Busdetails.objects.create(
                    busname=request.GET['busname'],
                    seat_no=request.GET['seats'],
                    desc =request.GET["description"],
                    owner_id =users.objects.get(id=request.GET["user_id"]),
                    busprofile=image_file
            )
            return JsonResponse({'status' : '201', 'result': 'true', 'data' : 'User Registeration Successful!'})


        case "Viewbuseslist":
            id = request.GET['user_id']
            row= Busdetails.objects.filter(owner_id=id,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['desc']=i.desc
                dic['seat_no']=i.seat_no
                dic['busname']=i.busname
                dic['busprofile']=str(i.busprofile)
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})  


        case "AddRooms":
            image=request.GET['busprofile']
            image_name=request.GET['busprofilename']
            image_data=base64.b64decode(image)
            Hoteldetails.objects.create(
                    room_no=request.GET['room_no'],
                    room_desc =request.GET["description"],
                    roomname=request.GET["roomname"],
                    owner_id =users.objects.get(id=request.GET["user_id"]),
                    roomprofile=image_file
            )
            return JsonResponse({'status' : '201', 'result': 'true', 'data' : 'User Registeration Successful!'})   


        case "Viewroomslist":
            id = request.GET['user_id']
            row= Hoteldetails.objects.filter(owner_id=id,status=0)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['room_desc']=i.room_desc
                dic['room_no']=i.room_no
                dic['roomname']=i.roomname
                dic['roompic']=str(i.roomprofile)
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})    


        case "getAllBusbyid":
            row= Busdetails.objects.filter(status=0)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['owner_id']=i.owner_id.id
                dic['busname']=i.busname
                det.append(dic) 
            return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'All Buses List', 'ResultData':{'AllBusbyadmin':det}})       


        case "getAllhotelssid":
            row= users.objects.filter(usertype=3,is_active=1)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['hotelname']=i.hotelname
                det.append(dic)
            return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'All Buses List', 'ResultData':{'AllHotelsbyAdmin':det}})   


        case "addTripassign":
            data = json.loads(request.body)
            sday=data['sday']
            eday=data['eday']
            count=data["avls"]
            flag=1
            b_id=Busdetails.objects.get(id=data["bus_id"])
            sday_date = datetime.strptime(data['sday'], "%d-%m-%Y").date()
            eday_date = datetime.strptime(data['eday'], "%d-%m-%Y").date()
            r_id=Hoteldetails.objects.get(id=data["room_id"])
            row=  package.objects.filter(bus_id=b_id)
            for i in row:
                start_date = i.startdate  
                end_date= i.enddate
                if start_date <= eday_date and end_date >= sday_date:
                   flag=0
                   return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'Bus is already alloted '})
            rowhotel=  package.objects.filter(room_id=r_id)
            for j in rowhotel:
                start_dateh = j.startdate  
                roomcount=j.room_id.room_no
                end_dateh= j.enddate
                if (start_dateh <= eday_date and end_dateh >= sday_date) or roomcount==count :
                    flag=0
                    return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'choose another room'})
            if(flag==1): 
                image=data['image']
                image_name=data['imagename']
                image_data=base64.b64decode(image)
                image_file=ContentFile(image_data,name=image_name + ".jpg")
                package.objects.create(
                    fromplace =data['from'],
                    toplace=data['to'],
                    startdate = datetime.strptime(data['sday'], '%d-%m-%Y').strftime('%Y-%m-%d'),
                    enddate = datetime.strptime(data['eday'], '%d-%m-%Y').strftime('%Y-%m-%d'),
                    amount =data["amount"],
                    desc =data["desc"],
                    seats=data["avls"],
                    hotel_id=users.objects.get(id=data["hotelid"]),
                    bus_id=Busdetails.objects.get(id=data["bus_id"]),
                    pkg_image=image_file,
                    room_id=Hoteldetails.objects.get(id=data["room_id"])
                )
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'Package Added Successfully'})    


        case "editTrip":
            data = json.loads(request.body)
            count=data["seats"]
            sday=data['sday']
            eday=data['eday']
            pkgid=data['packageid']
            k=package.objects.get(id=pkgid)
            sday_date = datetime.strptime(data['sday'], "%Y-%m-%d").date()
            eday_date = datetime.strptime(data['eday'], "%Y-%m-%d").date()
            flag=1
            if "bus_id" in data:
                try:
                    b_id=Busdetails.objects.get(id=data["bus_id"])
                    row=  package.objects.filter(bus_id=b_id)
                    for i in row:
                        start_date = i.startdate                          
                        end_date= i.enddate
                        if start_date <= eday_date and end_date >= sday_date:
                            flag=0
                        return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'Bus is already alloted '})
                    
                except Busdetails.DoesNotExist:
                    pass
            if "room_id" in data:
                try:
                    r_id=Hoteldetails.objects.get(id=data["room_id"])
                    rowhotel=  package.objects.filter(room_id=r_id)
                    for j in rowhotel:
                        start_dateh = j.startdate  
                        roomcount=j.room_id.room_no
                        end_dateh= j.enddate                        
                        if (start_dateh <= eday_date and end_dateh >= sday_date) or roomcount<count :
                            flag=0
                            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'choose another room'})
                except Hoteldetails.DoesNotExist:
                    pass
            if flag==1:        
                if "image" in data:
                    image = data['image']
                    print(image)
                    image_name = data['imagename']
                    print(image_name)
                    image_data = base64.b64decode(image)
                    print(image_data)
                    image_file = ContentFile(image_data, name=image_name + ".jpg")
                else:
                    image_file = None

                if "from" in data:
                    k.fromplace = data['from']
                if "to" in data:
                    k.toplace = data['to']
                if "sday" in data:
                    k.startdate = datetime.strptime(data['sday'], '%Y-%m-%d').date()
                if "eday" in data:
                    k.enddate = datetime.strptime(data['eday'], '%Y-%m-%d').date()
                if "amount" in data:
                    k.amount = data["amount"]
                if "desc" in data:
                    k.desc = data["desc"]
                if "room_id" in data:
                    try:
                        k.room_id = Hoteldetails.objects.get(id=data["room_id"])
                    except Hoteldetails.DoesNotExist:
                        pass
                if "seats" in data:
                    k.seats = data["seats"]
                if "hotelid" in data:
                    try:
                        k.hotel_id = users.objects.get(id=data["hotelid"])
                    except users.DoesNotExist:
                        pass
                if "bus_id" in data:
                    try:
                        k.bus_id = Busdetails.objects.get(id=data["bus_id"])
                    except Busdetails.DoesNotExist:
                        pass
                if image_file:
                    k.pkg_image = image_file
                k.save()
                return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'Package Edited Successfully'})
         
          
        case "viewpackagebyadmin":
            row= package.objects.all()
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['busname']=i.bus_id.busname
                dic['hotelname']=i.hotel_id.hotelname
                dic['fromplace']=i.fromplace
                dic['toplace']=i.toplace
                dic['startdate']=i.startdate
                dic['enddate']=i.enddate
                dic['amount']=i.amount
                dic['seats']=i.seats
                dic['desc']=i.desc
                dic['roomname']=i.room_id.roomname
                dic['roomimage']=str(i.room_id.roomprofile)
                dic['busimage']=str(i.bus_id.busprofile)
                dic['img']=str(i.pkg_image)
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "viewpackagebyuser":
            row= package.objects.all()
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['busname']=i.busname
                dic['hotelname']=i.hotelname
                dic['fromplace']=i.fromplace
                dic['toplace']=i.toplace
                dic['startdate']=i.startdate
                dic['enddate']=i.enddate
                dic['amount']=i.amount
                dic['seats']=i.seats
                dic['desc']=i.desc
                dic['rid']=i.room_id.id
                dic['img']=i.pkg_image
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "getPackageById":
            data = json.loads(request.body)
            pkgid=data['packageid']
            row= package.objects.get(id=pkgid)
            det=[]
            dic={}
            dic['id']=row.id
            dic['busname']=row.busname
            dic['hotelname']=row.hotelname
            dic['fromplace']=row.fromplace
            dic['toplace']=row.toplace
            dic['startdate']=row.startdate
            dic['enddate']=row.enddate
            dic['amount']=row.amount
            dic['seats']=row.seats
            dic['desc']=row.desc
            dic['pkgimage']=str(row.pkg_image)
            det.append(dic)
            return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'All Buses List', 'ResultData':{'Packagedatabyid':det}})   
           

        case "Deletepackage":
            dltid=request.GET['rid']
            r = package.objects.get(id=dltid)
            r.delete()
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'APPROVED!'})  


        case "AddBooking":
            data = json.loads(request.body)
            pplcount=data["totalppl"]
            ttl=package.objects.get(id=data["pkgid"])
            bseats=bookings.objects.filter(pkg_id=data["pkgid"])
            avlst=ttl.seats
            bal=avlst-int(pplcount) 
            print(bal)
            if(int(pplcount)>bal):
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'dont have enough seats'}) 
            else:  
                bookings.objects.create(
                    date =data['date'],
                    amount =data["amount"],
                    no_ppl=data["totalppl"],
                    user_id=users.objects.get(id=data["uid"]),
                    pkg_id=package.objects.get(id=data["pkgid"])
                )
                ttl.seats=bal
                ttl.save()
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'success'}) 


        case "mybookings":
            uid=request.GET['request']
            row=bookings.objects.filter(user_id=uid)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['userid']=i.user_id.id
                dic['pkid']=i.pkg_id.id
                dic['busname']=i.pkg_id.bus_id.busname
                dic['hotelname']=i.pkg_id.hotel_id.hotelname
                dic['fromplace']=i.pkg_id.fromplace
                dic['toplace']=i.pkg_id.toplace
                dic['desc']=i.pkg_id.desc
                dic['startdate']=i.pkg_id.startdate
                dic['enddate']=i.pkg_id.enddate
                dic['amount']=i.amount
                dic['no_ppl']=i.no_ppl
                dic['room']=i.pkg_id.room_id.roomname
                dic['profile']=str(i.pkg_id.pkg_image)
                det.append(dic)           
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})


        case "busseats":
            data = json.loads(request.body)
            id=data['busid']
            row= Busdetails.objects.filter(id=id)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['ownerid']=i.owner_id.id
                dic['seats']=i.seat_no
                det.append(dic)
            return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'All Buses List', 'ResultData':{'getseats':det}})    
        

        case "getAllroomsbyid":
            data = json.loads(request.body)
            id=data['hid'] 
            row= Hoteldetails.objects.filter(owner_id=id,status=0)            
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['owner_id']=i.owner_id.id
                dic['roomname']=i.roomname
                det.append(dic)
            return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'All Buses List', 'ResultData':{'allroomsbyowner':det}})


        case "AdminvwBookings":
            id=request.GET['packageid']
            row= bookings.objects.filter(pkg_id=id)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['name']=i.user_id.name
                dic['email']=i.user_id.email
                dic['phone']=i.user_id.phone
                dic['amount']=i.amount              
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})  


        case "Busbookingsbyid":
            uid=request.GET['user_id']
            row=bookings.objects.filter(pkg_id__bus_id__owner_id = uid)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['userid']=i.user_id.id
                dic['uname']=i.user_id.name
                dic['pkid']=i.pkg_id.id
                dic['busname']=i.pkg_id.bus_id.busname
                dic['fromplace']=i.pkg_id.fromplace
                dic['toplace']=i.pkg_id.toplace
                dic['desc']=i.pkg_id.desc
                dic['startdate']=i.pkg_id.startdate
                dic['enddate']=i.pkg_id.enddate
                dic['amount']=i.amount
                dic['seats']=i.pkg_id.seats
                dic['image']=str(i.pkg_id.bus_id.busprofile)
                det.append(dic)  
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "getreviw":
            row= review.objects.all()
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['uid']=i.user_id.id
                dic['uname']=i.user_id.email
                dic['review']=i.review
                det.append(dic)
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})


        case "insertreviw":           
            review.objects.create(
                 review=request.GET['title'],
                user_id =users.objects.get(id=request.GET["user_id"])  
            )
            return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'success'}) 


        case "deletereviw":
            dltid=request.GET['id']
            r = review.objects.get(id=dltid)
            r.delete()
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'deleted!'})


        case "Hotelroombookingsbyid":
            uid=request.GET['id']
            row=bookings.objects.filter(pkg_id__hotel_id = uid)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['userid']=i.user_id.id
                dic['uname']=i.user_id.name
                dic['pkid']=i.pkg_id.id
                dic['fromplace']=i.pkg_id.fromplace
                dic['toplace']=i.pkg_id.toplace
                dic['desc']=i.pkg_id.desc
                dic['startdate']=i.pkg_id.startdate
                dic['enddate']=i.pkg_id.enddate
                dic['amount']=i.amount
                dic['seats']=i.pkg_id.seats
                dic['roomname'] = i.pkg_id.room_id.roomname
                dic['image']=str(i.pkg_id.room_id.roomprofile)
                det.append(dic)         
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})
       

        case "Editbusbyid":
                data = json.loads(request.body)
                image=data['image']
                image_name=data['imagename']
                image_data=base64.b64decode(image)
                image_file=ContentFile(image_data,name=image_name + ".jpg")
                data = json.loads(request.body)
                busid=data['id']
                row= Busdetails.objects.get(id=busid)
                row.busname=data['busname']
                row.seat_no= data['seats']
                row.desc=data['desc']
                row.busprofile=image_file 
                row.save()  
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'Bus Edited Successfully'}) 


        case "Editroomsbyid":
                data = json.loads(request.body)
                image=data['image']
                print(image)
                image_name=data['imagename']
                print(image_name)
                image_data=base64.b64decode(image)
                print(image_data)
                image_file=ContentFile(image_data,name=image_name + ".jpg")
                data = json.loads(request.body)
                roomid=data['id']
                i= Hoteldetails.objects.get(id=roomid)
                i.roomname= data['roomname']
                i.room_no= data['roomno']
                i.room_desc= data['desc']
                i.roomprofile=image_file
                i.save()
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'Hotel Edited Successfully'})
        

        case "edituserprofile":
                uid=request.GET['id']
                k=users.objects.get(id=uid)
                k.name= request.GET['name']
                k.email= request.GET['email']
                k.phone =request.GET['phone']
                k.save()
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'Profile edited successfully'})


        case "viewprofile":
                data = json.loads(request.body)
                uid=data['id']
                row= users.objects.get(id=uid)
                det=[]
                dic={}
                dic['name']=row.name
                dic['email']=row.email
                dic['phone']=row.phone
                dic['hotel']=row.hotelname
                det.append(dic) 
                return JsonResponse({'ResponseCode' : '200', 'Result': 'true','ResponseMsg':'All Buses List', 'ResultData':{'profile':det}})

                         
        case "ViewBusesByAdmin":
            id=request.GET['id']
            row=Busdetails.objects.filter( owner_id=id)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['seat']=i.seat_no
                dic['desc']=i.desc
                dic['name']=i.busname
                dic['image']=str(i.busprofile)    
                det.append(dic)       
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "ViewRoomsByAdmin":
            id=request.GET['id']
            row=Hoteldetails.objects.filter( owner_id=id)
            print(row)
            det=[]
            for i in row:
                dic={}
                dic['id']=i.id
                dic['roomno']=i.room_no
                dic['desc']=i.room_desc
                dic['roomname']=i.roomname
                dic['image']=str(i.roomprofile)    
                det.append(dic)       
            return JsonResponse({'status' : '201', 'result': 'true', 'data' :det}) 


        case "cancelbooking":
            dltid=request.GET['id']
            r = bookings.objects.get(id=dltid)
            refill=r.pkg_id.seats
            numseats=r.no_ppl
            pkg = package.objects.get(id=r.pkg_id.id)
            pkg.seats=refill+numseats
            pkg.save()
            r.delete()
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'canceled!'})


        case "getbus":
                uid=request.GET['id']
                row=package.objects.filter(bus_id__owner_id=uid)
                det=[]
                for i in row:
                    dic={}
                    dic['id']=i.id
                    dic['busname']=i.bus_id.busname
                    dic['fromplace']=i.fromplace
                    dic['toplace']=i.toplace
                    dic['desc']=i.desc
                    dic['startdate']=i.startdate
                    dic['enddate']=i.enddate
                    dic['amount']=i.amount
                    dic['avls']=i.seats
                    dic['image']=str(i.bus_id.busprofile)
                    det.append(dic)         
                return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})


        case "gethotel":
                uid=request.GET['id']
                row=package.objects.filter(hotel_id=uid)
                det=[]
                for i in row:
                    dic={}
                    dic['id']=i.id
                    dic['hotelname']=i.room_id.roomname
                    dic['fromplace']=i.fromplace
                    dic['toplace']=i.toplace
                    dic['desc']=i.desc
                    dic['startdate']=i.startdate
                    dic['enddate']=i.enddate
                    dic['amount']=i.amount
                    dic['avls']=i.seats
                    dic['image']=str(i.room_id.roomprofile)
                    det.append(dic)         
                return JsonResponse({'status' : '201', 'result': 'true', 'data' :det})
        case "deletebus":
                bid=request.GET['id']
                b=Busdetails.objects.get(id=bid)
                b.status=1
                b.save()                
                return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'deleted!'})
  
        case "deleteroom":
                hid=request.GET['id']
                h=Hoteldetails.objects.get(id=hid)
                h.status=1
                h.save()
                return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'deleted'})
                            
             
        case "deleteaccount":
            accid=request.GET['user_id']
            try:
                user = users.objects.get(id=accid)
                user.delete()
            except Exception as err:
                pass
            return JsonResponse({'ResponseCode': '200', 'Result': 'true', 'ResponseMsg': 'deleted'})                 
               

                  

                


            

