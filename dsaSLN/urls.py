from django.urls import path,include

from rest_framework.routers import DefaultRouter
from .views import *
from dsaSLN.DSARestApiviews import DSAViewsets,DSA_AppliViewsets


from .views import *


router=DefaultRouter()
router.register('DSAViewsets',DSAViewsets,basename='dsa-view-sets')
router.register('DSA_Appli_Viewsets',DSA_AppliViewsets,basename='dsa-Appli-view-sets')



urlpatterns = [
    #  path('chat',chat,name='chat'),
     
    path('dsaAllInsurancesCount',dsaAllInsurancesCount,name="dsaAllInsurancesCount"),

    path('dashboard',dsaDashboard,name="dashboard"),

# Apply Loans
    path('apply-business',apply_business,name="apply-business"),
    path('applyEducation',apply_Education,name='applyEducation'),
    path('apply-home',home_loan,name='apply-home'),
    path('creditapply',credit_card,name='creditapply'),
    path('applycar',car_loan,name='applyCar'),
    path('lap',lap,name='lap'),
    path('apply-personal',apply_personal,name='apply-personal'),
    path('applyGold',apply_gold,name='applyGold'),
    path('applyotherLoan',apply_otherLoan,name='applyotherLoan'),
# Apply Loans

    path('index',dsaIndex,name='dsa-index'),
    path('dsaAll',dsaTotalAllApplications,name="dsa-all"),
    path('busiLoanApi',businessLoanApi,name='busiLoan'),
    path("approved",approvedLoans,name='approved'),
    path('rejected',rejectedLoans,name='rejected-loans'),
    path('showGraph',showAllLoansGraph,name='shoGraph'),
    path("AllLoans",allLOans,name="AllLoans"),
    path('disbursedAmount',disbursedTotalAmount,name='disbursedAmount'),
    path('disbursmentIds',disbursedTotalLoanIds,name='disbursmentIds'),
    path('disbursedTotalLoans',disbursedTotalLoans,name='disbursedTotalLoans'),
    path('jsondatadsa',get_all_dataAsJson,name='jsonDtaa'),
    path('profile',dsaProfile,name='profile'),
    path('alldsaids',getAllDsaIds,name='getAllDsaIds'),
    path('api/totalLoansCount',totalLoansCount,name='totalLoansCount'),
    
    path('api/SalestotalLoansCount',SalestotalLoansCount,name='SalestotalLoansCount'),
    path('api/creditCardCount',creditCardCount,name='creditCardCount'),
    
    
    path('Support',dsaSupport,name='dsaSupport'),

     
    #  CheckEligiblity.........
     path('educheckEligible',educheckEligible,name='educheckEligible'),
     path('busicheckEligible',busicheckEligible,name='busicheckEligible'),
     path('lapcheckEligible',lapcheckEligible,name='lapcheckEligible'),
     path('homecheckEligible',homecheckEligible,name='homecheckEligible'),
     path('personalcheckEligible',personalcheckEligible,name='personalcheckEligible'),
     path('carcheckEligible',carcheckEligible,name='carcheckEligible'),
     path('creditcheckEligible',creditcheckEligible,name='creditcheckEligible'),
     path('goldcheckEligible',goldcheckEligible,name='goldcheckEligible'),
     path('othercheckEligible',othercheckEligible,name='othercheckEligible'),
     

     
    #  Insurance.........
     path('lifeInsurance',lifeInsurance,name='lifeInsurance'),
     path('generalInsurance',generalInsurance,name='generalInsurance'),
     path('healthInsurance',healthInsurance,name='healthInsurance'),
     path('allInsurance',allInsurance,name='allInsurance'),
     

    # DSA LOGINS...............
    path('Login',dsaLogin,name='dsalogin'),
    path('Logout',dsaLogout,name='dsalogout'),
    # DSA LOGINS................
   

# DisbursementAmount

path('allTotalDisbursedAmountCalculator',allTotalDSADisbursedAmountCalculator,name='allTotalDisbursedAmountCalculator'),


    path("api/getDsa/<str:register_id>",DSAViewsets.as_view({"get":"getByRegisterId"}),name="get-dsa"),
    
    # DSA Track
   path('dsaTrack',dsaTrack,name='dsaTrack'),
   
   path('salesTrack',salesTrack,name='salesTrack'),
   path('salesregister',salesRegisterPage,name='salesRegisterPage'),
   
   path('franchiseOwnerClosedLoansData',franchiseOwnerClosedLoansData,name='franchiseOwnerClosedLoansData'),
   
   





    path("api/",include(router.urls)),
]
