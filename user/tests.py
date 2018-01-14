from django.test import TestCase
from user.models import User
from user.serializers import UserSerializer
# Create your tests here.


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(phone="+34666666666", address="España", email="prueba@gmail.com")
        User.objects.create(phone="+34999999999", address="España, sevilla", email="prueba2@gmail.com")

    def test_unitary_model(self):
        """Correct saved in the User DB"""

        user_1 = User.objects.get(email="prueba@gmail.com")
        user_2 = User.objects.get(email="prueba2@gmail.com")
        self.assertEqual(user_1.phone, '+34666666666')
        self.assertEqual(user_2.phone, '+34999999999')
        self.assertEqual(user_1.address, 'España')
        self.assertEqual(user_2.address, 'España, sevilla')

    def test_unitary_serializer_instance_user(self):
        """Correct instance serializer by a User"""
        user = User.objects.get(email="prueba@gmail.com")
        serializer_test = UserSerializer(user)
        data_test = serializer_test.data
        self.assertEqual(data_test['phone'], user.phone)
        self.assertEqual(data_test['address'], user.address)
        self.assertEqual(data_test['email'], user.email)

    def test_unitary_create_serializer(self):
        """Correct created user by a serializer"""
        data = {
            'email': "prueba3@gmail.com",
            'phone': "+34655555555",
            'address': "España",
        }
        serializer_test = UserSerializer(data=data)
        if serializer_test.is_valid():
            serializer_test.save()
            self.assertEqual(User.objects.get(email="prueba3@gmail.com").email, "prueba3@gmail.com")
        else:
            raise AttributeError(serializer_test.error_messages)

    def test_unitary_update_serializer(self):
        """Correct update user by a serializer"""

        data = {
            'phone': "+34678324125",
        }
        user = User.objects.get(email="prueba@gmail.com")
        serializer_test = UserSerializer(user, data=data, partial=True)
        if serializer_test.is_valid():
            serializer_test.save()
            self.assertEqual(serializer_test.data['phone'], user.phone)
            self.assertEqual(user.phone, "+34678324125")
        else:
            raise AttributeError(serializer_test.error_messages)