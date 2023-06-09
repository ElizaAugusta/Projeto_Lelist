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
        response = self.client.post('/cadastro/', {'nome': 'elizaa', 'email': 'elizaaugusta71@gmail.com', 'senha': '96536479'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário cadastrado com sucesso')

    def test_cadastro_post_request_existing_user(self):
        response = self.client.post('/cadastro/', {'nome': 'elizaa', 'email': 'elizaaugusta71@gmail.com', 'senha': '96536479'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Já existe um usuário com esse nome')

    def test_login_get_request(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_request(self):
        response = self.client.post('/login/', {'nome': 'elizaa', 'senha': '96536479'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Autenticado')

    def test_login_post_request_invalid_credentials(self):
        response = self.client.post('/login/', {'nome': 'elizaa', 'senha': '96536479'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Email ou senha inválidos')


class ProdutoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='elizaa', password='96536479')
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

class ProdutoDetalheTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='elizaa', password='96536479')
        self.produto = Produtos.objects.create(active=True, id=1)

    def test_produto_detalhe_login_required(self):
        response = self.client.get(reverse('produto_detalhe', args=[self.produto.id]))
        self.assertEqual(response.status_code, 302)  

    def test_produto_detalhe_authenticated_user(self):
        self.client.login(username='elizaaa', password='96536479')
        response = self.client.get(reverse('produto_detalhe', args=[self.produto.id]))
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'dados_produto.html')  
        self.assertEqual(response.context['produto'], self.produto)  

class ExcluirProdutoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='elizaa', password='96536479')
        self.produto = Produtos.objects.create(id=1)

    def test_excluir_produto_login_required(self):
        response = self.client.get(reverse('excluir_produto', args=[self.produto.id]))
        self.assertEqual(response.status_code, 302)  

    def test_excluir_produto_authenticated_user(self):
        self.client.login(username='elizaa', password='96536479')
        response = self.client.get(reverse('excluir_produto', args=[self.produto.id]))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, '/home/')  
        self.assertFalse(Produtos.objects.filter(id=self.produto.id).exists())  

