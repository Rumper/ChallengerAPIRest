from rest_framework import serializers
from budget.models import Budget
from user.serializers import UserSerializer
from budget.choices import STATUS, PENDING


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return dict((k,v) for k, v in self._choices)[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('uuid', 'title', 'description', 'category', 'status', 'user', 'created_at', 'modified_at')


class BudgetSerializerShow(BudgetSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    status = ChoicesField(choices=STATUS, default=PENDING)
    user = UserSerializer(many=False, read_only=True)


