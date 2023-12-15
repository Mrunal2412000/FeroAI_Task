from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserResponse,
    ErrorMessage,
    CartProductAddSeriallizer,
    CartProductEditSeriallizer,
    OrderCreateSeriallizer,
    ProductListingresponseSerializer,
    ProductViewResponseSerializer,
    CartProductViewResponseSerializer,
    OrderViewResponseSerializer
    )
from .models import *
from common.helper import error_400, send_response, send_response_validation

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import  IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_spectacular.utils import extend_schema

class RegisterAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = (JSONParser,)

    @extend_schema(
        tags = ["User Authentication"],
        responses = {
            200: UserResponse,
            400: ErrorMessage,
        },
        summary = 'Make the user register'
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data = request.data,context={'lang': request.headers['Accept-Language']})
            if serializer.is_valid(raise_exception=False):
                data=serializer.save()
                response_data = {
                    "id": data['user'].id,
                    "username": data['user'].username,
                    'email' : data['user'].email,
                    'access_token': data['tokens']['access'],
                    'refresh_token': data['tokens']['refresh'], 
                    }
                return send_response(request, message = "You are registered successfully", data = response_data)
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request,message=(error_msg_value[0]))
        except Exception as e:
            return error_400(request,message=str(e))


class LoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    parser_classes = (JSONParser,)

    @extend_schema(
        responses={
            200 : UserResponse, 
            400: ErrorMessage,
        },
        tags = ['User Authentication'],
        summary = 'make the user login'
    )
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid(raise_exception=False):
                data = serializer.save()
                response_data = {
                    "id": data['user'].id,
                    "username": data['user'].username,
                    'email' : data['user'].email,
                    'access_token': data['tokens']['access'],
                    'refresh_token': data['tokens']['refresh'], 
                    }
                return send_response(request, message = "You are logged in successfully", data = response_data)
            else:
                error_msg_value = list(serializer.errors.values())[0]
                return error_400(request, message = error_msg_value[0])
        except Exception as e:
            return error_400(request,message=str(e))


class ProductListingAPIView(generics.GenericAPIView):
    permission_classes=(IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        responses={
            200 : ProductListingresponseSerializer, 
            400: ErrorMessage,
        },
        tags = ['Product'],
        summary = 'Product Listing for authenticated user'
    )
    def get(self, request):
        user=request.user
        if (user != None):
            if user.is_authenticated:
                product_list = []
                queryset = Product.objects.all()
                for product in queryset:
                    data = {
                        "id":product.id,
                        "name":product.name,
                        "description":product.description,
                        "price":product.price,
                        "stock_quantity":product.stock_quantity
                    }
                    product_list.append(data)
                response_data = {
                    "message":'Success',
                    "data":product_list
                }
                return Response(response_data)
            return error_400(request,message="User not authenticated")


class ProductListingAllUserAPIView(generics.GenericAPIView):
    permission_classes=(AllowAny,)

    @extend_schema(
        responses={
            200 : ProductListingresponseSerializer, 
            400: ErrorMessage,
        },
        tags = ['Product'],
        summary = 'Product Listing for all users'
    )
    def get(self, request):
        product_list = []
        queryset = Product.objects.all()
        for product in queryset:
            data = {
                "id":product.id,
                "name":product.name,
                "description":product.description,
                "price":product.price,
                "stock_quantity":product.stock_quantity
            }
            product_list.append(data)
        response_data = {
            "message":'Success',
            "data":product_list
        }
        return Response(response_data)


class ProductDetailAPIVIew(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        responses={
            200 : ProductViewResponseSerializer, 
            400: ErrorMessage,
        },
        tags = ['Product'],
        summary = 'Product Detail'
    )
    def get(self, request, id):
        try:
            user = request.user
            if user!=None:
                if user.is_authenticated:
                    product = get_object_or_404(Product, id=id)
                    data = {
                        "id":product.id,
                        "name":product.name,
                        "description":product.description,
                        "price":product.price,
                        "stock_quantity":product.stock_quantity
                    }
                    return send_response(request, message="Success", data=data)
                return error_400(request,message="User not authenticated")
        except Exception as e:
            return error_400(request,message=str(e))


class ProductDetailAllUserAPIVIew(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200 : ProductViewResponseSerializer, 
            400: ErrorMessage,
        },
        tags = ['Product'],
        summary = 'Product Detail'
    )
    def get(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)
            data = {
                "id":product.id,
                "name":product.name,
                "description":product.description,
                "price":product.price,
                "stock_quantity":product.stock_quantity
            }
            return send_response(request, message="Success", data=data)
        except Exception as e:
            return error_400(request,message=str(e))

class CartProductAddAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductAddSeriallizer

    @extend_schema(
        responses={
            200 : ErrorMessage, 
            400: ErrorMessage,
        },
        tags = ['Cart'],
        summary = 'Cart Product Add'
    )
    def post(self, request):
        try:
            user = request.user
            if user!=None:
                if user.is_authenticated:
                    serializer = self.serializer_class(data = request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        return send_response_validation(request, message = "Product added to cart successfully")
                return error_400(request,message="User not authenticated")

        except Exception as e:
            return error_400(request,message=str(e))


class CartProductViewAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200 : CartProductViewResponseSerializer, 
            400: ErrorMessage,
        },
        tags = ['Cart'],
        summary = 'Cart Product View'
    )
    def get(self, request):
        try:
            user = request.user
            if user!=None:
                if user.is_authenticated:
                    response_data = []
                    user_cart = Cart.objects.filter(user=user, is_ordered = False).order_by('-id')
                    for cart in user_cart:
                        data = {
                            "id":cart.id,
                            "product_id":cart.product.id,
                            "product_name":cart.product.name,
                            "quantity":cart.quantity
                        }
                        response_data.append(data)
                    return send_response(request, message = "Success", data = response_data)
                return error_400(request,message="User not authenticated")

        except Exception as e:
            return error_400(request,message=str(e))

class CartProductEditAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductEditSeriallizer

    @extend_schema(
        responses={
            200 : ErrorMessage, 
            400: ErrorMessage,
        },
        tags = ['Cart'],
        summary = 'Cart Product Edit'
    )
    def put(self, request, id):
        try:
            user = request.user
            if user!=None:
                if user.is_authenticated:
                    cart = get_object_or_404(Cart, id=id)
                    serializer = self.serializer_class(cart, data = request.data, context={"request": request, "id":id})
                    if serializer.is_valid():
                        serializer.save()
                        return send_response_validation(request, message = "Product updated successfully")
                return error_400(request,message="User not authenticated")

        except Exception as e:
            return error_400(request,message=str(e))


class CreateOrderAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSeriallizer

    @extend_schema(
        responses={
            200 : ErrorMessage, 
            400: ErrorMessage,
        },
        tags = ['Order'],
        summary = 'Order create from cart values'
    )
    def post(self, request):
        try:
            user = request.user
            if user!=None:
                if user.is_authenticated:
                    serializer = self.serializer_class(data = request.data, context={"request": request})
                    if serializer.is_valid():
                        serializer.save()
                        return send_response_validation(request, message = "Order created successfully")
                    else:
                        error_msg_value = list(serializer.errors.values())[0]
                        return error_400(request, message = error_msg_value[0])
                return error_400(request,message="User not authenticated")
        except Exception as e:
            return error_400(request,message=str(e))

class OrderDetailAPIView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200 : OrderViewResponseSerializer, 
            400: ErrorMessage,
        },
        tags = ['Order'],
        summary = 'Order Detail'
    )
    def get(self, request,id):
        try:
            user = request.user
            if user!=None:
                if user.is_authenticated:
                    response_data = []
                    order = Order.objects.get(user=user,id=id)
                    order_products = order.products.through.objects.filter(order=order)
                    print(order_products)
                    for order_product in order_products:
                        data = {
                            "id":order_product.product.id,
                            "product_name":order_product.product.name,
                            "quantity":order_product.quantity
                        }
                        response_data.append(data)
                    final_response = {
                        "order_id":order.id,
                        "address":order.address,
                        "total_price":order.total_price,
                        "order_status":order.order_status,
                        "products":response_data
                    }
                    return send_response(request, message = "Success", data = final_response)
        except Exception as e:
            return error_400(request,message=str(e))