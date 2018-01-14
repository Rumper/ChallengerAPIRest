from rest_framework.response import Response
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from budget.serializers import BudgetSerializer, BudgetSerializerShow
from budget.choices import PENDING, PUBLISHED, DISCARDED
from user.models import User
from user.serializers import UserSerializer
from budget.models import Budget, Categories
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from budget.content_based import ContentBased


class Utils:

    @staticmethod
    def check_parameters_required(parameters_required, data):
        for key, value in data.items():
            if key not in parameters_required:
                return Response({'error': _("Parameter no permit: <<%s>>") % key}, status=status.HTTP_400_BAD_REQUEST)


class BudgetsAPI(generics.ListAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, Utils):

    queryset = Budget.objects.all()
    serializer_class = BudgetSerializerShow
    pagination_class = PageNumberPagination

    def check_user(self, data):
        """
            Check if there is a user with that email, otherwise it creates it
            
        :param data: Information of the user
        :return: User
        """
        email = data.get('email', '')
        user_data = {
            'email': email,
            'phone': data.get('phone', ''),
            'address': data.get('address', '')
        }
        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(user, data=user_data) if user else UserSerializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            return user, serializer.data
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, email=None, page=None):
        """
            If an email is sent to you, return a list of all budget requests submitted by that user,
             otherwise return all system requests
             
        :param request: Data dictionary of the request 
        :param email: Email of the user
        :param page: Number de page
        :return: list of budget requests
        """
        if email:
            user = get_object_or_404(User, email=email)
            budgets = Budget.objects.filter(user=user.pk)
        else:
            budgets = Budget.objects.all()

        page = self.paginate_queryset(budgets)

        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ 
            Create a new budget request, if there isn't user with that email, create a new user
            
        :param request: Data dictionary of the request with the information of a new budget request
        :return: Data dictionary with a message, status 200 and identification of the budget request created
        """
        request_data = request.data
        parameters_required = ['description', 'email', 'phone', 'address']
        self.check_parameters_required(parameters_required, request_data)
        user, data = self.check_user(request_data)
        data['uuid'] = Budget.get_new_uuid()
        data['user'] = user.pk
        data['title'] = request_data.get('title', '')
        data['description'] = request_data.get('description')
        if 'category' in data:
            category_name = data.get('category', '').lower()
            category = Categories.objects.filter(name=category_name).first()
            if not category:
                category = Categories.objects.create(name=category_name)
            data['category'] = category.pk
        serializer = BudgetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'uuid': data['uuid'],
                'message': _("The budget has been created")
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status.HTTP_400_BAD_REQUEST)

    def paginate_queryset(self, queryset):
        """
            Return a single page of results, 
            or `None` if pagination is disabled.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        if self._paginator is None:
            return None
        return self._paginator.paginate_queryset(
            queryset,
            self.request,
            view=self
        )

    def get_paginated_response(self, data):
        """
            Return a paginated style `Response` object 
            for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class BudgetAPI(APIView, Utils):

    def check_status(self, current_status, error):
        is_error = False
        if current_status != PENDING:
            is_error = True
            if current_status == PUBLISHED:
                error['message'] = _("The budget already is published")
            if current_status == DISCARDED:
                error['message'] = _("The budget already is discarded")
            return Response(error['message'], status=status.HTTP_304_NOT_MODIFIED)
        return is_error, error

    def put(self, request, uuid):
        """
            Change the status to the published budget request with the uuid obtained by the request
            
        :param request:  None
        :param uuid: Identification of the budget request to be modified
        :return:  Data dictionary with a message and status 200
        """
        budget = get_object_or_404(Budget, uuid=uuid)
        is_error, error = self.check_status(budget.status, {
            'message': _("The '%s' is empty, you should modify your budget"),
        })
        if not budget.title:
            is_error = True
            error['message'] = error['message'] % _("title")
        elif not budget.category:
            is_error = True
            error['message'] = error['message'] % _("category")

        if is_error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        serializer = BudgetSerializer(budget, data={"status": PUBLISHED}, partial=True)
        if serializer.is_valid():
            budget = serializer.save()
            return Response({'message': _("The budget has been published")})
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
            Modify the title, description or category fields the budget request with the uuid obtained by the request
            
        :param request: Data dictionary of the request with uuid the budget request
        :return: Data dictionary with a message and status 200
        """
        request_data = request.data
        parameters_required = ['uuid']
        self.check_parameters_required(parameters_required, request_data)

        if len(request_data) == 1:
            return Response({'message':_("You need at least one parameter: title category descripcion")},
                            status=status.HTTP_400_BAD_REQUEST)

        budget = get_object_or_404(Budget, uuid=request_data['uuid'])
        self.check_status(budget.status, {})
        serializer = BudgetSerializer(budget, data=request.data, partial=True)
        if serializer.is_valid():
            budget = serializer.save()
            return Response({'message': _("The budget has been modify")})
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        """
          Modify the status to discarded the budget request with the uuid obtained by the request
          
        :param request: Data dictionary of the request 
        :param uuid: Identification of the budget request to be modified
        :param format: None
        :return: Data dictionary with a message and status 200
        """
        budget = get_object_or_404(Budget, uuid=uuid)

        if budget.status == DISCARDED:
            return Response({'message': _("The budget has already been discarded")}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = BudgetSerializer(budget, data={'status': DISCARDED}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': _("The budget has been discarded")},
                                status=status.HTTP_200_OK)
            else:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class BudgetSuggest(APIView, Utils):

    def get(self, request, uuid=None):
        """
            Suggest a category according to the description of the budget request with the uuid obtained by the request
            
        :param request: Data dictionary of the request with uuid the budget request
        :return: Data dictionary with status 200, the uuid gone through the request and the suggest category
        """
        Response({}, status=status.HTTP_200_OK)
        budget = get_object_or_404(Budget, uuid=uuid)
        all_budgets = Budget.objects.all()

        Recommendation = ContentBased()
        if all_budgets:
            dict_info = [{'Categoría':k, 'Descripción': v}
                         for k, v in all_budgets.values('category__name', 'description') if k]
            Recommendation.append(dict_info)
        category_suggest = Recommendation.predict(budget.description)

        if category_suggest:
            context = {
                'categories_suggest': category_suggest
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response({'message': _("No found recommendation category by this description")},
                            status=status.HTTP_403_FORBIDDEN)
