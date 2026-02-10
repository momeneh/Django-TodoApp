from rest_framework import serializers
from ...models import Task

class TaskSerializer(serializers.ModelSerializer):
    # snippet = serializers.ReadOnlyField(source='get_snippet') # get_snippet function is in Post Class Model
    # relative_url = serializers.URLField(source='get_absolute_api_url',read_only=True) # get_absolute_api_url function is in Post Class Model
    # absolute_url = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ['id','title','user']
        read_only_fields = ['user']

   
    # def get_absolute_url(self,obj):
    #     request = self.context.get('request')
    #     return request.build_absolute_uri(obj.pk) 
    
    # def to_representation(self,instance):
    #     rep = super().to_representation(instance)

    #     request = self.context.get('request')
    #     if request.parser_context['kwargs'].get('pk'): 
    #         rep.pop('snippet',None)
    #         rep.pop('relative_url',None)
    #         rep.pop('absolute_url',None)
    #     else :
    #         rep.pop('content',None)
            
    #     rep['category'] = CategorySerializer(instance.category).data
    #     return rep
    
    def create(self,validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)   


