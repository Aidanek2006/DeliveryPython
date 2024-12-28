from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password',
                  'user_role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username']


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['contact_info']


class ProductComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCombo
        fields = ['combo_name', 'combo_image', 'price', 'description' ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'price', 'description']


class StoreListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    avg_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    count_good_grade = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'category', 'avg_rating',
                  'count_people', 'count_good_grade']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_count_good_grade(self, obj):
        return obj.get_count_good_grade()


class OrderSerializer(serializers.ModelSerializer):
    order_client = UserProfileSimpleSerializer()

    class Meta:
        model = Order
        fields = ['order_client', 'courier', 'delivery_address']


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class CourierReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    courier = UserProfileSimpleSerializer()
    client = UserProfileSimpleSerializer()

    class Meta:
        model = CourierReview
        fields = ['courier', 'client', 'rating', 'created_date',]


class StoreReviewSerializer(serializers.ModelSerializer):
    client = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = StoreReview
        fields = ['store', 'comment',  'client', 'rating']


class StoreDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    products = ProductSerializer(many=True, read_only=True)
    combos = ProductComboSerializer(many=True, read_only=True)
    contact_info = ContactInfoSerializer(many=True, read_only=True)
    store_reviews = StoreReviewSerializer(many=True, read_only=True)
    owner = UserProfileSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'category', 'description',
                  'address', 'owner', 'products', 'combos', 'contact_info', 'store_reviews']


class StoreCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = UserProfileSimpleSerializer()

    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'category', 'description', 'address', 'owner']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')
    total_price = serializers.SerializerMethodField()


    class Meta:
        model = CarItem
        fields = ['product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'items']
