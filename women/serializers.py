import io
import datetime

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from  rest_framework.parsers import JSONParser
from .models import *


# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content
#         #self.photo = photo

# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     #photo = serializers.ImageField()

# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     slug = serializers.SlugField(max_length=255)
#     content = serializers.CharField()
#     photo = serializers.ImageField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     cat_id = serializers.IntegerField()
#
#     def create(self, validated_data):
#         #print(validated_data)
#         return Women.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.slug = validated_data.get("slug", instance.slug)
#         instance.content = validated_data.get("content", instance.content)
#         instance.photo = validated_data.get("photo", instance.photo)
#         instance.time_update = validated_data.get("time_update", instance.time_update)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         instance.save()
#         return instance



# def encode():
#     model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
#     model_sr = WomenSerializer(model)
#     print(model_sr, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json, sep='\n')
#
# def decode():
#     stream = io.BytesIO(b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}')
#     data = JSONParser().parse(stream)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data,sep='\n')

class WomenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Women
        # fields = ('title', 'slug', 'content', 'photo', 'cat')
        fields = "__all__"