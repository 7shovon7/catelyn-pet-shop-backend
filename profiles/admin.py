from django.contrib import admin
from .models import Customer, CustomerAddress, CustomerContact, WholesalerCompany, WholesalerBranch, WholesalerAddress, WholesalerContact


admin.site.register([WholesalerCompany, WholesalerBranch, WholesalerAddress, WholesalerContact, Customer, CustomerAddress, CustomerContact])
