from .models import User, Cart, Product, Order, CartOrder

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.core.validators import validate_email
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.db import transaction


import re, random

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        write_only = True, 
        validators = [UniqueValidator(
            queryset = User.objects.all(), 
            message = "Email address already exists."
        )]
    )
    password = serializers.CharField(
        max_length = 16, 
        min_length = 8, 
        error_messages = {
            'min_length': 'Password must be between 8-16 characters and contain at least 1 upper case letter, at least 1 upper case letter, 1 lower case letter, special characters and 1 numeric character.', 
            'max_length': 'Password must be between 8-16 characters and contain at least 1 upper case letter, at least 1 upper case letter, 1 lower case letter, special characters and 1 numeric character.'
        }, 
        write_only=True
    )


    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegisterSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = u'Email address cannot be blank'
        self.fields['email'].error_messages['required'] = u'Email address is required'
        self.fields['password'].error_messages['required'] = u'Password is required'
        self.fields['password'].error_messages['blank'] = u'Password cannot be blank'
        

    def validate(self, data):
        try:
            validate_email(data['email'].lower())
        except:
            raise serializers.ValidationError("Please enter a valid Email address")
        
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not (re.fullmatch(regex, data['password'])):
            raise serializers.ValidationError("Password must be between 8-16 characters and contain at least 1 upper case letter, at least 1 upper case letter, 1 lower case letter, special characters and 1 numeric character.")
        
        return data

    def create(self, validated_data):
        email = validated_data.pop('email').lower()
        username = "".join(email.split('@')[0]).lower()
        if not User.objects.filter(username=username).exists():
            random_username = username
        else:
            random_username = username + str(random.randint(0, 10000))

        user = User.objects.create(
            username=random_username,
            email = email,
        )
        user.set_password(validated_data['password'])
        user.save()
        tokens = user.tokens()
        return {'user': user, 'tokens': tokens}
    
class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    access_token = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)

class UserResponse(serializers.Serializer):
    message = serializers.CharField(required=False)
    data = UserDetailSerializer(required=False)

class ErrorMessage(serializers.Serializer):
    message = serializers.CharField(required=False)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        write_only = True, 
        help_text = "Enter Your Email",
        required = True
    )
    password = serializers.CharField(
        max_length = 16, 
        error_messages = {
            'max_length': ('Password must be between 8-16 characters.')
        },
        write_only = True, 
        required = True
    )

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['blank'] = u'Email address cannot be blank'
        self.fields['email'].error_messages['required'] = u'Email address cannot be blank'
        self.fields['password'].error_messages['required'] = u'Password field is required'
        self.fields['password'].error_messages['blank'] = u'Password cannot be blank'

    def validate(self, data):
        try:
            validate_email(data['email'])
        except:
            raise serializers.ValidationError("Please enter a valid Email address")

        user = auth.authenticate(
            email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Incorrect Email address or Password")
                

        return data

    def create(self, validated_data):

        user = auth.authenticate(
            email = validated_data.pop('email'), 
            password = validated_data.pop('password')
        )
        tokens = user.tokens()
        return {'user': user, 'tokens': tokens}

class CartProductAddSeriallizer(serializers.ModelSerializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

    def validate(self, data):
        if self.context.get('request').data['quantity'] <= 0:
            raise Exception("Add valid Quantity")

        return data
    
    def create(self, validated_data):
        user = get_object_or_404(User, id=self.context.get('request').user.id)
        product = get_object_or_404(Product, id=validated_data['product'])
        if user and product:
            cart = Cart.objects.filter(user=user, product=product, is_ordered = False)
            if cart:
                cart.update(quantity=cart[0].quantity+validated_data['quantity'])
            else:
                cart = Cart.objects.create(
                    user=user, 
                    product=product, 
                    quantity=validated_data['quantity']
                )
            return cart


class CartProductEditSeriallizer(serializers.ModelSerializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ['product', 'quantity']
    
    def update(self, instance, validated_data):
        user = get_object_or_404(User, id=self.context.get('request').user.id)
        product = get_object_or_404(Product, id=validated_data['product'])
        if user and product:
            cart = Cart.objects.filter(id = self.context.get('id'), user=user, is_ordered = False)
            if cart:
                carts = Cart.objects.filter(id = self.context.get('id'), user=user, product=product, is_ordered = False)
                if carts:
                    cart.update(quantity=validated_data['quantity'])
                    return cart
                cart.update(quantity=validated_data['quantity'], product=product)
                return cart
            else:
                raise Exception("Cart Not Found")

class OrderCreateSeriallizer(serializers.Serializer):
    address = serializers.CharField()


    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get('request').user
        cart = Cart.objects.filter(user = user, is_ordered = False)
        if cart:
            total_price = 0
            order = Order.objects.create(user=user, order_status="placed", address=validated_data['address'], total_price=total_price)
            for cart_instance in cart:
                product = Product.objects.get(id = cart_instance.product.id)
                stock = product.stock_quantity - cart_instance.quantity

                if stock<0:
                    raise Exception(f"Product {product.name} has only {product.stock_quantity} in stock an you are ordering {cart_instance.quantity}")
                
                cart_order = CartOrder.objects.create(
                    cart = cart_instance,
                    order = order,
                    product = product, 
                    quantity = cart_instance.quantity
                )
                total_price = total_price + product.price * cart_order.quantity
                product.stock_quantity = stock #Quantity deducted from stock
                product.save()
            order.total_price = total_price
            order.save()
            cart.update(is_ordered = True)
            return order
        else:
            raise Exception("Your cart is Empty")
    transaction.commit()


class ProductDetailSeriallizer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    stock_quantity = serializers.IntegerField()

class ProductListingresponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ProductDetailSeriallizer(many=True)

class ProductViewResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ProductDetailSeriallizer()

class CartProductViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()


class CartProductViewResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = CartProductViewSerializer(many=True)

class OrderProductDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()

class OrderDetailSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    address = serializers.CharField()
    total_price = serializers.CharField()
    order_status = serializers.CharField()
    products = OrderProductDetailSerializer(many=True)

class OrderViewResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = OrderDetailSerializer()