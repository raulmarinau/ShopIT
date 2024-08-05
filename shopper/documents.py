from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django.contrib.auth.models import User
from .models import Saved_Product, Saved_Product_Info, CustomUser_NestedField

@registry.register_document
class Saved_Product_Document(Document):
    infos = fields.NestedField(properties={
        'price': fields.FloatField(),
        'old_price': fields.FloatField(),
        'date': fields.DateField(),
        'pk': fields.IntegerField()
    })

    users = fields.NestedField(properties={
        'user': fields.TextField(),
        'pk': fields.IntegerField()
    })

    class Index:
        name = 'saved_products'

        settings =  {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Saved_Product

        fields = [
            'name',
            'link',
            'retailer'
        ]

        related_models = [Saved_Product_Info, CustomUser_NestedField]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Saved_Product_Info):
            return related_instance.product_base
        if isinstance(related_instance, CustomUser_NestedField):
            return related_instance.product_base
