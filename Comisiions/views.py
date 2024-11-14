from django.shortcuts import redirect, render
import requests
from dsaSLN.models import *

from dsaSLN.views import *
from datetime import datetime

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum

def dsaManualId(request):
   return dsamanualId(request)


def getDSA(request):
    return DSA.objects.get(dsa_registerid=dsaManualId(request))

import uuid

def generateUUID(request):
   generated_uuid = uuid.uuid4()
   return generated_uuid


@csrf_exempt
def disbursementRecords(request):
    print("disbursementRecords")
    
    if request.GET.get('showall'):
      if request.session.get('datefilter1'):
         del request.session['datefilter1']
    
    if request.GET.get('datefilter'):
       request.session['datefilter1']=request.GET.get('datefilter')
       
    response=requests.get(f'{settings.ACCOUNTS_SOURCE_URL}/getFranchiseClaimed/{dsaManualId(request)}')
    res=None

    objects,start_index,result=None,None,None
    if response.status_code==200:
        res=response.json()
    dsa=getDSA(request)

    
    if res:
        print("Res...............")
        request.session['comission']=True
        loans=allLOans(request)
        request.session['comission']=False
        # print(loans)
        if loans:
            # print("loans")
            for i in loans:
                for j in res:
                    if i['application_id'] == j.get('application_id'):
                        # print(i['application_id'])
                        # print(j.get('application_id'))
                        try:
                          comObj=Comission(con=dsa,application_id=i['application_id'],name=i['name'],loan_amount=i['required_loan_amount'],loan_type=i['application_loan_type'],comissionPercentage=None,comissionAmount=j.get('branch_payout_slab_in_Rs'),disbursedAmount=j.get('disbursedAmount'),date=j.get('date'))
                          comObj.save()
                          print("SUcess")
                        except:
                            print("Except Block333")
    
    
   #  disbrsedResult=Comission.objects.filter(con=dsa)
    
     


# Claim one By One Logic
    if request.GET.get('id'):
        
        # print("GET ID>>>>>>>>>")
        reqId=request.GET.get('id')
    else:
        reqId=None

    if reqId:
         # generated_uuid = uuid.uuid4()
         
         # print(generateUUID(request))
         ids=[]
         ids.append(reqId)
         context={
         'ids':ids,
         'referenceId':str(generateUUID(request)),
         'franCode':request.session.get('franchCode'),
        }
         try:
          # print(reqId)
          comObj=Comission.objects.get(application_id=reqId)
          dsaPayoutObj=DSAPayOut(payouts=dsa,application_id=comObj.application_id,name=comObj.name,loan_amount=comObj.loan_amount,loan_type=comObj.loan_type,comissionPercentage=comObj.comissionPercentage,comissionAmount=comObj.comissionAmount,disbursedAmount=comObj.disbursedAmount,date=comObj.date)
          dsaPayoutObj.save()
         except:
             print("except")
  
         
         response2=requests.post(f"{settings.ACCOUNTS_SOURCE_URL}/postAcnt",json=context)
        #  print("inside  Request.....")
         if response2.status_code==200:
           secondResponse=requests.get(f'{settings.ACCOUNTS_SOURCE_URL}/getFranchiseClaimed/{dsaManualId(request)}')
        #    print("inside post Request.....")
           if secondResponse.status_code==200:
            #   print("inside get Request.....")
              res=secondResponse.json()
            #   return render(request,"DataTables.html",{'res':secondRes})
           elif secondResponse.status_code==404:
               return render(request,"DataTables.html",{'objects':[]})
         else:
             return HttpResponse("Problem")
         
    if request.GET.get('applicationid'):
       if request.session.get('datefilter1'):
         del request.session['datefilter1']
      #  print("Application ID>>>>>>>>>>>>><<<<<<<<<")
      #  print(request.GET.get('applicationid'))
       for i in res:
          # print("inside1")
          if i.get('application_id')==request.GET.get('applicationid'):
            #  print("inside1")
             result=i
       if result:
          # print("Yyyyyyyyyyy999..")
          # print(result)
          res=result
       else:
          print("ELse None")
          res=None
          
    if request.session.get('datefilter1'):
            date=request.session.get('datefilter1')
            # print("po09765../")
            dateResult=[]
            print(date)
            date_format = "%Y-%m-%d"
            # print(date)
            date1=date.split(' to ')[0]
            date2=date.split(' to ')[1]
            
            for i in res:
              if i.get('date')>=date1 and i.get('date')<=date2:
               dateResult.append(i)
            res=dateResult
    

# Claim All Logic..............
    if request.method=="POST":
        allIds=[]
        
        if not request.POST.get('datefilter'):
         if res:
            for ids in res:
                allIds.append(ids.get('application_id'))
            context={
            'ids':allIds,
            'referenceId':str(generateUUID(request)),
            'refCode':request.session.get('franchCode'),
             }
            # print(allIds)

            
            for reqid in allIds:
             try:
              comObj=Comission.objects.get(application_id=reqid)
              dsaPayoutObj=DSAPayOut(payouts=dsa,application_id=comObj.application_id,name=comObj.name,loan_amount=comObj.loan_amount,loan_type=comObj.loan_type,comissionPercentage=comObj.comissionPercentage,comissionAmount=comObj.comissionAmount,disbursedAmount=comObj.disbursedAmount,date=comObj.date)
              dsaPayoutObj.save()
             except:
               print("Posst except")

            responses=requests.post(f"{settings.ACCOUNTS_SOURCE_URL}/postAcnt",json=context)
            if responses.status_code==200:
                res2=requests.get(f'{settings.ACCOUNTS_SOURCE_URL}/getFranchiseClaimed/{dsaManualId(request)}')
                if res2.status_code==404:
                    res=None
                    return redirect('is-claim')
                else:
                 res=res2.json()
                 

        
    

    if res:
      if isinstance(res, dict):
        res = [res]
        
      
      paginator = Paginator(res, 10)
      print("3")
      page = request.GET.get('page', 1)
      print("4")
    
      try:
        objects = paginator.page(page)
      except PageNotAnInteger:
        objects = paginator.page(1)
      except EmptyPage:
        objects = paginator.page(1)
        
      # print("5")
      start_index = (objects.number - 1) * paginator.per_page + 1
      print(f"{objects.number}---{paginator.per_page}")

    if result:
      #  print("result....")
       return render(request,"DataTables.html",{'objects':objects,'start_index':start_index,'claimpage':True})
    
    # print("Method Ends.............")
    return render(request,"claim.html",{'objects':objects,'start_index':start_index,'claimpage':True})


def postToAccounts(request):
    context={
    'ids':['SLNBUSI1003']
    }
    response=requests.post(f"{settings.ACCOUNTS_SOURCE_URL}/postAcnt",json=context)
    if response.status_code==200:

     return HttpResponse("sucess")
    else:
       print()
       return HttpResponse("failed")
    

def commonComissions(request):
   totalAmount=0

   response=requests.get(f'{settings.ACCOUNTS_SOURCE_URL}/getFranchiseDisbursedRecords/{dsaManualId(request)}')
   if response.status_code==200:
      print("commonCommisons")
      res=response.json()
      print(res)
   else:
      res=None
   
   if request.session.get('disbursedTotalAmount'):
      print("loan Amout")
      if res:
       for i in res:
         totalAmount+=int(i['disbursedAmount'])
       return totalAmount
   
   if request.session.get('disbursedTotalLoans'):
      if res:
       return len(res)
      
   print("returned.........")
   return res
  
      
         
    

@csrf_exempt
def viewComissions(request):
   from dsaSLN.views import allLOans
   
   if request.GET.get('showall'):
      showAll=True
      if request.session.get('datefilter'):
         del request.session['datefilter']
   
   if request.GET.get('datefilter'):
      request.session['datefilter']=request.GET.get('datefilter')
      
   result=None
   print("My comisoons trigered......")
   dsa=getDSA(request)
   res=commonComissions(request)
   print(res,"FRM VIEWCOMISOONS..................---------")
   if res:
        
        # print("Res...............")
       
       
        request.session['comission']=True
        loans=allLOans(request)
        print("started////////////////////////")
        print(loans)
        request.session['comission']=False
        # print(loans)
        if loans:
            # print("loans")
           
            for i in loans:
                for j in res:
                    if i['application_id'] == j.get('application_id'):
                        print(i['application_id'])
                        print(j.get('application_id'))
                        print(i['name'])
                        # print(i['application_loan_type'])
                        try:
                          comObj=Comission(con=dsa,application_id=i['application_id'],name=i['name'],loan_amount=i['required_loan_amount'],loan_type=i['application_loan_type'],comissionPercentage=None,comissionAmount=j.get('branch_payout_slab_in_Rs'),disbursedAmount=j.get('disbursedAmount'),date=j.get('date'))
                          print(comObj.date)
                          comObj.save()
                          # print("SUcess")
                        except Exception as e:
                            print("Except Block333",e)

   
   
   try:
      resu=DSA.objects.prefetch_related('comission').get(dsa_registerid=dsaManualId(request))
      re=resu.comission.all()
   except:
       re=None
   
  #  if  request.session.get('disbursedTotalAmount'):
  #     request.session['disbursedTotalAmount']=re.aggregate(Sum('loan_amount'))['loan_amount__sum']
  #     return
  #  if request.session.get('disbursedTotalLoans'):
  #     request.session['disbursedTotalLoans']=re.count()
  #     return 
   
   
  #  print(totalAmount)

      
    
   if request.GET.get('applicationid'):
       if request.session.get('datefilter'):
         del request.session['datefilter']
      #  print("Application ID>>>>>>>>>>>>><<<<<<<<<")
      #  print(request.GET.get('applicationid'))
       for i in re:
          # print("inside1")
          # print(i.application_id)
          if i.application_id == request.GET.get('applicationid'):
            #  print("inside1")
             result=i
       if result:
          # print("Yyyyyyyyyyy999..")
          # print(result)
          re=[result]
       else:
          # print("ELse None")
          re=None

   if request.session.get('datefilter'):
         # print(request.session.get('datefilter'))
      # if request.POST.get('datefilter'):
         date=request.session.get('datefilter')
         print("po09765../")
         dateResult=[]
         # print(date)
         date_format = "%Y-%m-%d"
         date1=date.split(' to ')[0]
         date2=date.split(' to ')[1]
         date1 = datetime.strptime(date1, date_format).date()
         date2 = datetime.strptime(date2, date_format).date()
         for i in re:
            if i.date>=date1 and i.date<=date2:
               dateResult.append(i)
         re=dateResult
              



          
   if re:
        
      paginator = Paginator(re, 10)
      # print("3")
      page = request.GET.get('page', 1)
      # print("4")
    
      try:
        objects = paginator.page(page)

      except PageNotAnInteger:
        objects = paginator.page(1)

      except EmptyPage:
        objects = paginator.page(1)
        
      
      start_index = (objects.number - 1) * paginator.per_page + 1
      # print(f"{objects.number}---{paginator.per_page}")
      
      if result:
       return render(request,"DataTables.html",{'objects':objects,'start_index':start_index,'isactive':True})

      return render(request,"Comission.html",{'objects':objects,'isactive':True,'start_index':start_index})
   else:
      return render(request,"Comission.html",{'objects':[],'isactive':True})
   

def payOuts(request):
   
    
    if request.GET.get('showall'):
      showAll=True
      if request.session.get('datefilter2'):
         del request.session['datefilter2']
   
    if request.GET.get('datefilter'):
      request.session['datefilter2']=request.GET.get('datefilter')
      
    result=None
    try:
      resu=DSA.objects.prefetch_related('payout').get(dsa_registerid=dsaManualId(request))
      re=resu.payout.all()
    except:
       re=None

    if request.GET.get('applicationid'):
       if request.session.get('datefilter2'):
         del request.session['datefilter2']
       print("Application ID>>>>>>>>>>>>><<<<<<<<<")
       print(request.GET.get('applicationid'))
       for i in re:
          print("inside1")
          print(i.application_id)
          if i.application_id == request.GET.get('applicationid'):
             print("inside1")
             result=i
       if result:
          print("Yyyyyyyyyyy999..")
          print(result)
          re=[result]
       else:
          print("ELse None")
          re=None


    if request.session.get('datefilter2'):
         print('jpost payouts/...................')
      # if request.POST.get('datefilter'):
      
         date=request.session.get('datefilter2')
         print("po09765../")
         dateResult=[]
         print(date)
         date_format = "%Y-%m-%d"
            # print(date)
         date1=date.split(' to ')[0]
         date2=date.split(' to ')[1]
         date1 = datetime.strptime(date1, date_format).date()
         date2 = datetime.strptime(date2, date_format).date()
         for i in re:
            if i.date>=date1 and i.date<=date2:
               dateResult.append(i)
         re=dateResult

    if re:
      paginator = Paginator(re, 10)
      print("3")
      page = request.GET.get('page', 1)
      print("4")
    
      try:
        objects = paginator.page(page)

      except PageNotAnInteger:
        objects = paginator.page(1)

      except EmptyPage:
        objects = paginator.page(1)
        
      
      start_index = (objects.number - 1) * paginator.per_page + 1
      print(f"{objects.number}---{paginator.per_page}")
      
      if result:
       return render(request,"DataTables.html",{'objects':objects,'start_index':start_index,'isactive':True})

      return render(request,"Comission.html",{'objects':objects,'isactive':True,'start_index':start_index})
    else:
      return render(request,"Comission.html",{'objects':[],'isactive':True})





def myEarnings(request):
   
    if request.GET.get('showall'):
      showAll=True
      if request.session.get('datefilter4'):
         del request.session['datefilter4']
   
    if request.GET.get('datefilter'):
      request.session['datefilter4']=request.GET.get('datefilter')
      
    result=None
    
    respo=requests.get(f"{settings.ACCOUNTS_SOURCE_URL}/SettlementWindowViewSet/{dsaManualId(request)}/getEarningRecordsOfFranchise/")
    if respo.status_code==200: re=respo.json()
    else: re=[]
    
    totalEarnings = sum(i.get('franch_Amount_in_Rs', 0) for i in re)

   #  print(totalEarnings,"jjjjjjjjjj---===")
    if request.GET.get('applicationid'):
       if request.session.get('datefilter4'):
         del request.session['datefilter4']
       
       print("Application ID>>>>>>>>>>>>><<<<<<<<<")
       print(request.GET.get('applicationid'))
       for i in re:
          print("inside1")
          print(i.get('application_id'))
          if i.get('application_id') == request.GET.get('applicationid'):
             print("inside1")
             result=i
             break;
       if result:
          print("Yyyyyyyyyyy999..")
         #  print(result)
          re=[result]
       else:
          print("ELse None")
          re=[]


    if request.session.get('datefilter4'):
         print('jpost payouts/...................')
      # if request.POST.get('datefilter'):
         date=request.session.get('datefilter4')
         print("po09765../")
         dateResult=[]
         print(date)
         date_format = "%Y-%m-%d"
            # print(date)
         date1=date.split(' to ')[0]
         date2=date.split(' to ')[1]
         print(date2,date1)
         # date1 = datetime.strptime(date1, date_format).date()
         # date2 = datetime.strptime(date2, date_format).date()
         for i in re:
            if i.get('Settlement_Date')>=date1 and i.get('Settlement_Date')<=date2:
               dateResult.append(i)
         re=dateResult

    if re:
      paginator = Paginator(re, 10)
      print("3")
      page = request.GET.get('page', 1)
      print("4")
    
      try:
        objects = paginator.page(page)

      except PageNotAnInteger:
        objects = paginator.page(1)

      except EmptyPage:
        objects = paginator.page(1)
        
      
      start_index = (objects.number - 1) * paginator.per_page + 1
      print(f"{objects.number}---{paginator.per_page}")
      
      if result:
       return render(request,"DataTables.html",{'objects':objects,'start_index':start_index,'myEarnings':True})

      return render(request,"Comission.html",{'objects':objects,'myEarnings':True,'start_index':start_index,'totalEarnings':intcomma(totalEarnings)})
    else:
      return render(request,"Comission.html",{'objects':[],'myEarnings':True})
      