# 참고자료 : https://dev-navill.tistory.com/15
from rest_framework import serializers
from .models import Comment

# 모델 인스턴스를 파이썬 기본 데이터 유형으로 변환
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance,context = self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    created_at = serializers.DateTimeField(format="%Y.%m.%d")
    updated_at = serializers.DateTimeField(format="%Y.%m.%d")

    class Meta:
        model = Comment
        fields = '__all__'
        
    def get_reply(self,instance):
        # recursive
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('',self)
        return serializer.data
        

