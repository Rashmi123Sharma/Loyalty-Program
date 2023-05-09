"""
WSGI config for loyalty project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loyalty.settings')

application = get_wsgi_application()








# def create(self, request):
#         try:
#             #check for new loyalty
#             details = Loyalty.objects.all()
#             if details.count()==0:
#                 data=request.data
#                 serializer = Loyaltyserializer(data=data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
                    
#                 data={
#                     'status':True,
#                     'message':'Saved successfully'
#                 }
#                 return Response(data)
#             else:
#                 loyalty=Loyalty.objects.get(id=1)
#                 loyalty=Loyaltyserializer(loyalty,data=request.data,partial=True)
#                 loyalty.is_valid(raise_exception=True)
#                 loyalty.save()
                
#                 data={
#                     'status':True,
#                     'message':'Updated successfully'
#                 }
#                 return Response(data)
#         except Exception as e:
#             data={
#                 'status':False,
#                 'message':'Failed to save',
#                 'error':e,
#                 'line':e.__traceback__.tb_lineno
#             }
#             return Response(data)
        

#     def list(self, request):
#         #check for new loyalty
#         details = Loyalty.objects.all()
#         if details.count()==0:
#             data={
#                 'status':True,
#                 'loyalty_available':False,
#                 'message':'No loyalty points available'
#             }
#             return Response(data)
        
#         details=Loyalty.objects.get(id=1)
#         serializer = Loyaltyserializer(details,context={'request': request})
#         return Response(serializer.data)
        
        
    

    
        
        


    

