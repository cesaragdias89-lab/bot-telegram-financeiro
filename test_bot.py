# Testes para o Bot de Controle Financeiro

import unittest
import os
import json
from datetime import datetime

# Importa os módulos do bot
from utils import (
    parse_value, parse_date, format_currency, calculate_balance, 
    get_month_summary, format_lancamento
)
from whatsapp_bot import WhatsAppFinanceBot


class TestUtils(unittest.TestCase):
    """Testes para as funções utilitárias."""
    
    def test_parse_value(self):
        """Testa parsing de valores."""
        # Valores válidos
        self.assertEqual(parse_value("150"), 150.0)
        self.assertEqual(parse_value("150.50"), 150.50)
        self.assertEqual(parse_value("150,50"), 150.50)
        self.assertEqual(parse_value("1500"), 1500.0)
        
        # Valores inválidos
        self.assertIsNone(parse_value("abc"))
        self.assertIsNone(parse_value(""))
        self.assertIsNone(parse_value("150.50.25"))
        self.assertIsNone(parse_value("150,50,25"))
    
    def test_parse_date(self):
        """Testa parsing de datas."""
        # Data válida
        self.assertEqual(parse_date("12/08/2025"), "12/08/2025")
        self.assertEqual(parse_date("12-08-2025"), "12/08/2025")
        
        # Data inválida ou vazia (deve retornar data atual)
        today = datetime.now().strftime("%d/%m/%Y")
        self.assertEqual(parse_date(""), today)
        self.assertEqual(parse_date("data_invalida"), today)
    
    def test_format_currency(self):
        """Testa formatação de moeda."""
        self.assertEqual(format_currency(1500.00), "R$ 1.500,00")
        self.assertEqual(format_currency(150.50), "R$ 150,50")
        self.assertEqual(format_currency(0.99), "R$ 0,99")
    
    def test_calculate_balance(self):
        """Testa cálculo de saldo."""
        lancamentos = [
            {'tipo': 'entrada', 'valor': 1000.0},
            {'tipo': 'saida', 'valor': 250.0},
            {'tipo': 'entrada', 'valor': 500.0},
            {'tipo': 'saida', 'valor': 100.0}
        ]
        
        expected_balance = 1000.0 - 250.0 + 500.0 - 100.0
        self.assertEqual(calculate_balance(lancamentos), expected_balance)
    
    def test_get_month_summary(self):
        """Testa resumo mensal."""
        lancamentos = [
            {'tipo': 'entrada', 'valor': 1000.0, 'data': '01/08/2025'},
            {'tipo': 'saida', 'valor': 250.0, 'data': '02/08/2025'},
            {'tipo': 'entrada', 'valor': 500.0, 'data': '03/07/2025'},  # mês diferente
        ]
        
        summary = get_month_summary(lancamentos, "08/2025")
        self.assertEqual(summary['entradas'], 1000.0)
        self.assertEqual(summary['saidas'], 250.0)
        self.assertEqual(summary['saldo'], 750.0)
    
    def test_format_lancamento(self):
        """Testa formatação de lançamento."""
        lancamento = {
            'tipo': 'entrada',
            'valor': 1500.0,
            'descricao': 'salário',
            'data': '12/08/2025',
            'autor': 'João'
        }
        
        # Sem autor
        result = format_lancamento(lancamento, include_author=False)
        expected = "➕ R$ 1.500,00 — salário (12/08/2025)"
        self.assertEqual(result, expected)
        
        # Com autor
        result = format_lancamento(lancamento, include_author=True)
        expected = "João ➕ R$ 1.500,00 — salário (12/08/2025)"
        self.assertEqual(result, expected)


class TestWhatsAppBot(unittest.TestCase):
    """Testes para o bot do WhatsApp."""
    
    def setUp(self):
        """Configuração antes de cada teste."""
        self.bot = WhatsAppFinanceBot()
        self.test_number = "+5511999999999"
        
        # Limpa dados de teste
        if self.test_number in self.bot.data:
            del self.bot.data[self.test_number]
    
    def test_parse_command(self):
        """Testa parsing de comandos."""
        # Comando simples
        result = self.bot.parse_command("saldo")
        self.assertEqual(result['command'], 'saldo')
        self.assertEqual(result['args'], [])
        
        # Comando com argumentos
        result = self.bot.parse_command("entrada 1500 salário")
        self.assertEqual(result['command'], 'entrada')
        self.assertEqual(result['args'], ['1500', 'salário'])
        
        # Mensagem vazia
        result = self.bot.parse_command("")
        self.assertIsNone(result['command'])
        self.assertEqual(result['args'], [])
    
    def test_entrada_command(self):
        """Testa comando de entrada."""
        # Entrada válida
        response = self.bot.process_entrada(self.test_number, ['1500', 'salário'])
        self.assertIn('➕', response)
        self.assertIn('R$ 1.500,00', response)
        self.assertIn('salário', response)
        
        # Verifica se foi salvo
        user_data = self.bot.get_user_data(self.test_number)
        self.assertEqual(len(user_data['lancamentos']), 1)
        self.assertEqual(user_data['lancamentos'][0]['tipo'], 'entrada')
        self.assertEqual(user_data['lancamentos'][0]['valor'], 1500.0)
    
    def test_saida_command(self):
        """Testa comando de saída."""
        # Saída válida
        response = self.bot.process_saida(self.test_number, ['89,90', 'mercado'])
        self.assertIn('➖', response)
        self.assertIn('R$ 89,90', response)
        self.assertIn('mercado', response)
        
        # Verifica se foi salvo
        user_data = self.bot.get_user_data(self.test_number)
        self.assertEqual(len(user_data['lancamentos']), 1)
        self.assertEqual(user_data['lancamentos'][0]['tipo'], 'saida')
        self.assertEqual(user_data['lancamentos'][0]['valor'], 89.9)
    
    def test_saldo_command(self):
        """Testa comando de saldo."""
        # Adiciona alguns lançamentos
        self.bot.add_lancamento(self.test_number, 'entrada', 1000.0, 'teste', '12/08/2025')
        self.bot.add_lancamento(self.test_number, 'saida', 250.0, 'teste', '12/08/2025')
        
        response = self.bot.process_saldo(self.test_number)
        self.assertIn('💰', response)
        self.assertIn('R$ 750,00', response)  # 1000 - 250
    
    def test_observadores(self):
        """Testa funcionalidade de observadores."""
        observador = "+5511888888888"
        
        # Adiciona observador
        response = self.bot.process_cadastrar(self.test_number, [observador])
        self.assertIn('✅', response)
        self.assertIn('adicionado', response)
        
        # Verifica se foi adicionado
        user_data = self.bot.get_user_data(self.test_number)
        self.assertIn(observador, user_data['observadores'])
        
        # Remove observador
        response = self.bot.process_remover(self.test_number, [observador])
        self.assertIn('❌', response)
        self.assertIn('removido', response)
        
        # Verifica se foi removido
        user_data = self.bot.get_user_data(self.test_number)
        self.assertNotIn(observador, user_data['observadores'])
    
    def test_desfazer_command(self):
        """Testa comando de desfazer."""
        # Adiciona um lançamento
        self.bot.add_lancamento(self.test_number, 'entrada', 1000.0, 'teste', '12/08/2025')
        
        # Verifica que existe
        user_data = self.bot.get_user_data(self.test_number)
        self.assertEqual(len(user_data['lancamentos']), 1)
        
        # Desfaz
        response = self.bot.process_desfazer(self.test_number)
        self.assertIn('❌', response)
        self.assertIn('removido', response)
        
        # Verifica que foi removido
        user_data = self.bot.get_user_data(self.test_number)
        self.assertEqual(len(user_data['lancamentos']), 0)


def run_tests():
    """Executa todos os testes."""
    print("Executando testes do Bot de Controle Financeiro...")
    print("=" * 50)
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestWhatsAppBot))
    
    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resultado
    if result.wasSuccessful():
        print("\n✅ Todos os testes passaram!")
        return True
    else:
        print(f"\n❌ {len(result.failures)} falha(s), {len(result.errors)} erro(s)")
        return False


if __name__ == '__main__':
    run_tests()

