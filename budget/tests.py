from django.test import TestCase
from budget.models import Categories, Budget
from budget.choices import PUBLISHED, PENDING, DISCARDED
from budget.content_based import ContentBased
from budget.serializers import BudgetSerializer
from user.models import User
from rest_framework import status


# Create your tests here.


class BudgetTest(TestCase):
    UUID = Budget.get_new_uuid()
    UUID2 = Budget.get_new_uuid()

    def setUp(self):
        user = User.objects.create(phone="+34666666666", address="España", email="prueba5@gmail.com")
        user_1 = User.objects.create(phone="+34999999999", address="España, sevilla", email="prueba6@gmail.com")

        category = Categories.objects.create(name="construcción casas")
        category_1 = Categories.objects.create(name="reformas baños")

        Budget.objects.create(uuid=self.UUID, title="Contrución de casa",
                              description='Necesito presupuesto para construir una casa de dos plantas en churriana de la vega (Granada). Tengo la parcela de 220 metros cuadrados en propiedad. Se trataría de una casa de 3 plantas con 5 o más habitaciones. Estoy pendiente de adquirir el proyecto.',
                              category=category, status=PENDING,
                              user=user)
        Budget.objects.create(uuid=self.UUID2, title="Contrución de casa",
                              description='Necesito presupuesto para construir una casa de dos plantas en churriana de la vega (Granada). Tengo la parcela de 220 metros cuadrados en propiedad. Se trataría de una casa de 3 plantas con 5 o más habitaciones. Estoy pendiente de adquirir el proyecto.',
                              category=category_1, status=PENDING,
                              user=user_1)

    def test_unitary_create_budget(self):
        """ Correct created budget """
        uuid = Budget.get_new_uuid()
        budget = Budget.objects.create(uuid=uuid, title="Contrución de casa",
                                       description='Necesito presupuesto para construir una casa de dos plantas en churriana de la vega (Granada). Tengo la parcela de 220 metros cuadrados en propiedad. Se trataría de una casa de 3 plantas con 5 o más habitaciones. Estoy pendiente de adquirir el proyecto.',
                                       category=Categories.objects.get(name="reformas baños"), status=PENDING,
                                       user=User.objects.get(email="prueba6@gmail.com"))

        self.assertEqual(budget.status, PENDING)
        self.assertEqual(budget.title, "Contrución de casa")
        self.assertEqual(budget.uuid, uuid)

    def test_unitary_serializer_instance_user(self):
        """Correct instance serializer by a User"""
        budget = Budget.objects.get(uuid=self.UUID)
        serializer_test = BudgetSerializer(budget)
        data_test = serializer_test.data
        self.assertEqual(data_test['title'], budget.title)

    def test_unitary_create_serializer(self):
        """Correct create user by serializer"""
        data = {
            'uuid': Budget.get_new_uuid(),
            'user': User.objects.get(email="prueba5@gmail.com").pk,
            'title': "Nueva Mampara",
            'category': Categories.objects.get(name="reformas baños").pk,
            'description': "Una mampara de ducha de una puerta abatible de 70 no me importaria que fuera barata de expocicion."
        }
        serializer_test = BudgetSerializer(data=data)
        if serializer_test.is_valid():
            serializer_test.save()
            self.assertEqual(Budget.objects.get(uuid=data['uuid']).title, data['title'])
        else:
            raise AttributeError(serializer_test.error_messages)

    def test_unitary_update_serializer(self):
        """Correct update user by serializerr"""

        data = {
            'title': "Construción de casa precio asequible",
        }
        budget = Budget.objects.get(uuid=self.UUID)
        serializer_test = BudgetSerializer(budget, data=data, partial=True)
        if serializer_test.is_valid():
            serializer_test.save()
            self.assertEqual(serializer_test.data['title'], budget.title)
        else:
            raise AttributeError(serializer_test.error_messages)

    def test_unitary_api_get_budgets(self):
        """ Correct operation for the request of the entire budget """
        response = self.client.get('/api/1.0/budgets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unitary_api_get_budgets_by_email(self):
        """ Correct operation for the request of all the budget according to the user's email """
        response = self.client.get('/api/1.0/budgets/prueba5@gmail.com/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unitary_api_post_budgets_create(self):
        """ Correct operation of the api when creating a new budget,
         in addition the user will be updated or modified according to whether the email exists or not """
        url = '/api/1.0/budgets/'
        data = {
            'email': 'prueba10@gmail.com',
            'phone': '+34666666666',
            'address': 'España',
            'title': "Nueva Mampara",
            'category': "reformas baños",
            'description': "Una mampara de ducha de una puerta "
                           "abatible de 70 no me importaria que fuera barata de expocicion."
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='prueba10@gmail.com')
        self.assertEqual(user.email, data['email'])
        budget = Budget.objects.get(uuid=response.data['uuid'])
        self.assertEqual(budget.title, data['title'])

    def test_unitary_api_post_budget(self):
        """ Correct operation of the api when we want to modify the title,
         the description or the category of a budget """
        url = '/api/1.0/budget/'
        data = {
            'uuid': self.UUID2,
            'title': 'Contrución de casa griega'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget = Budget.objects.get(uuid=self.UUID2)
        self.assertEqual(budget.title, data['title'])

    def test_unitary_api_put_budget(self):
        """ Correct operation of the api when we want to publish a budget """
        response = self.client.put('/api/1.0/budget/%s/' % self.UUID2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        budget = Budget.objects.get(uuid=self.UUID2)
        self.assertEqual(budget.status, PUBLISHED)

    def test_unitary_api_delete_budget(self):
        """ Correct operation of the api when we want to discard a budget given an identifier """
        url = '/api/1.0/budget/%s/' % self.UUID
        data = {}
        response = self.client.delete(url, data, format='json')
        budget = Budget.objects.get(uuid=self.UUID)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(budget.status, DISCARDED)

    def test_unitary_api_suggest_category_budget(self):
        """ Correct functioning of the api when we want to request a category suggestion for an identifier"""
        contentbase = ContentBased()
        category_suggest = contentbase.predict("quiero quitar la bañera y poner una mampara con un plato de ducha")
        self.assertIn("reformas baños", category_suggest)

        response = self.client.get('/api/1.0/suggest_categories/%s/' % self.UUID2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn( "construcción casas", response.data['categories_suggest'])
