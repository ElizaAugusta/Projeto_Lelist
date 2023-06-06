from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Produtos 

class CadastroLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cadastro_get_request(self):
        response = self.client.get('/cadastro/')
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_cadastro_post_request(self):
        response = self.client.post('/cadastro/', {'nome': 'hello', 'email': 'hello@example.com', 'senha': 'hellopassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário cadastrado com sucesso')

    def test_cadastro_post_request_existing_user(self):
        response = self.client.post('/cadastro/', {'nome': 'hello', 'email': 'hello@example.com', 'senha': 'hellopassword'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Já existe um usuário com esse nome')

    def test_login_get_request(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_request(self):
        response = self.client.post('/login/', {'nome': 'hello', 'senha': 'hellopassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Autenticado')

    def test_login_post_request_invalid_credentials(self):
        response = self.client.post('/login/', {'nome': 'testuser', 'senha': 'invalidpassword'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Email ou senha inválidos')


class ProdutoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.produto_data = {
            'nome': 'Produto Teste',
            'tipo': 'Tipo Teste',
            'quantidade': 10,
            'data_validade': '2023-06-01',
            #'foto': ('')
        }

    def test_produto_get(self):
        response = self.client.get('/produto/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produto.html')

    def test_produto_post(self):
        response = self.client.post('/produto/', data=self.produto_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produto.html')
        produto = Produtos.objects.get(nome='Produto Teste')
        self.assertEqual(produto.nome, 'Produto Teste')
        self.assertEqual(produto.tipo, 'Tipo Teste')
        self.assertEqual(produto.quantidade, 10)
        self.assertEqual(str(produto.data_validade), '2023-06-01')
        self.assertIsNone(produto.foto)
