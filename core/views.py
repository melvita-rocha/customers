from django.shortcuts import render, HttpResponse
from .models import Customer, Profession, DataSheet, Document 
from .serializers import (
    CustomerSerializer, 
    ProfessionSerializer,
    DataSheetSerializer,
    DocumentSerializer,
)
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser, 
    DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly )


# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [ 'name', 'address', 'data_sheet__description' ]
    filterset_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['id']        # default ordering can be done using `ordering`
    lookup_field = 'name'    # this should be unique field
    authentication_classes = [ TokenAuthentication, ]

    def get_queryset(self):
        # import pdb; pdb.set_trace()   # here the break point was put just to check in the console
        address = self.request.query_params.get('address', None) 
        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True

        if address:
            customers = Customer.objects.filter(address__icontains=address, active=status)
        else:
            customers = Customer.objects.filter(active=status)
        return customers

        
        

    # def list(self, request, *args, **kwargs):
    #     """The `list` function is actually an inbuilt of ModelViewset which we have modified based on our requirement"""
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
        # return Response({'message': 'Not allowed'})

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     customer = Customer.objects.create(
    #         name=data['name'], address=data['address'], data_sheet_id =data['data_sheet'], 
    #     )
    #     profession_data = Profession.objects.get(id=data['professions'])
    #     customer.professions.add(profession_data)
    #     customer.save()

    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)


    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession_data = Profession.objects.get(id=data['professions'])

        for p in customer.professions.all():
            customer.professions.remove(p)
        
        customer.professions.add(profession_data)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)

        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()
        return Response('Object removed')

    @action(detail=True)  # detail=True means this action is performed on a single object with the url having the primary key
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)  # detail=False means this action is performed on a collection of objects with no primary key in the url 
    def deactivate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_status(self, request, **kwargs):
        status = True if request.data['active'] == 'True' else False

        customers = self.get_queryset()
        customers.update(active=status)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes = [ TokenAuthentication, ]
    permission_classes = [IsAdminUser, ]


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny, ]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [ TokenAuthentication, ]
    permission_classes = [ DjangoModelPermissionsOrAnonReadOnly, ]