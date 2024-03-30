from .models import Contact, BusinessInfo

def footer(request):
    contact = Contact.objects.first()
    businessInfo =BusinessInfo.objects.first()
    
    footer_info = {
        'address'    : contact.address,
        'sub_address': contact.sub_address,
        'phone'      : contact.phone,
        'sub_phone'  : contact.sub_phone,

        'rep'        : businessInfo.rep,
        'email'      : businessInfo.email,
        'CRN'        : businessInfo.CRN,
    }

    return {'footer_info': footer_info}
