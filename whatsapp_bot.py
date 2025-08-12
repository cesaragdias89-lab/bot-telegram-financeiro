# Bot do WhatsApp para Controle Financeiro
# NOTA: Este é um módulo de estrutura para implementação futura
# Para funcionar completamente, seria necessário integração com APIs do WhatsApp Business
# ou soluções de terceiros como whatsapp-web.js

import re
from datetime import datetime
from typing import List, Dict, Any, Optional

from config import WELCOME_MESSAGE, ERROR_INVALID_VALUE, WHATSAPP_DATA_FILE
from utils import (
    parse_value, parse_date, format_currency, load_json_data, save_json_data,
    calculate_balance, get_month_summary, format_lancamento
)


class WhatsAppFinanceBot:
    """Bot do WhatsApp para controle financeiro."""
    
    def __init__(self):
        self.data = load_json_data(WHATSAPP_DATA_FILE)
    
    def save_data(self):
        """Salva os dados do bot."""
        save_json_data(WHATSAPP_DATA_FILE, self.data)
    
    def get_user_data(self, numero: str) -> Dict[str, Any]:
        """Obtém dados do usuário."""
        if numero not in self.data:
            self.data[numero] = {
                'numero': numero,
                'lancamentos': [],
                'observadores': []
            }
        return self.data[numero]
    
    def add_lancamento(self, numero: str, tipo: str, valor: float, descricao: str, data: str):
        """Adiciona um lançamento."""
        user_data = self.get_user_data(numero)
        
        lancamento = {
            'tipo': tipo,
            'valor': valor,
            'descricao': descricao,
            'data': data
        }
        
        user_data['lancamentos'].append(lancamento)
        self.save_data()
        
        return lancamento
    
    def add_observador(self, numero: str, observador: str) -> bool:
        """Adiciona um observador."""
        user_data = self.get_user_data(numero)
        
        if observador not in user_data['observadores']:
            user_data['observadores'].append(observador)
            self.save_data()
            return True
        
        return False
    
    def remove_observador(self, numero: str, observador: str) -> bool:
        """Remove um observador."""
        user_data = self.get_user_data(numero)
        
        if observador in user_data['observadores']:
            user_data['observadores'].remove(observador)
            self.save_data()
            return True
        
        return False
    
    def parse_command(self, message: str) -> Dict[str, Any]:
        """
        Parse de comando do WhatsApp (sem barra inicial).
        
        Args:
            message: Mensagem recebida
            
        Returns:
            Dicionário com comando e argumentos
        """
        parts = message.strip().split()
        if not parts:
            return {'command': None, 'args': []}
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return {'command': command, 'args': args}
    
    def process_entrada(self, numero: str, args: List[str]) -> str:
        """Processa comando de entrada."""
        if not args:
            return ERROR_INVALID_VALUE
        
        # Parse dos argumentos
        valor_str = args[0]
        descricao = ' '.join(args[1:]) if len(args) > 1 else ''
        
        # Verifica se o último argumento é uma data
        data_str = None
        if len(args) > 1:
            possible_date = args[-1]
            if '/' in possible_date or '-' in possible_date:
                data_str = possible_date
                descricao = ' '.join(args[1:-1])
        
        # Valida o valor
        valor = parse_value(valor_str)
        if valor is None:
            return ERROR_INVALID_VALUE
        
        # Parse da data
        data = parse_date(data_str)
        
        # Adiciona o lançamento
        lancamento = self.add_lancamento(numero, 'entrada', valor, descricao, data)
        
        # Calcula novo saldo
        user_data = self.get_user_data(numero)
        saldo = calculate_balance(user_data['lancamentos'])
        
        # Formata resposta
        lancamento_str = format_lancamento(lancamento)
        saldo_str = format_currency(saldo)
        
        response = f"{lancamento_str}\n💰 Seu saldo: {saldo_str}"
        
        # TODO: Enviar para observadores
        self._notify_observers(numero, response)
        
        return response
    
    def process_saida(self, numero: str, args: List[str]) -> str:
        """Processa comando de saída."""
        if not args:
            return ERROR_INVALID_VALUE
        
        # Parse dos argumentos (mesmo processo da entrada)
        valor_str = args[0]
        descricao = ' '.join(args[1:]) if len(args) > 1 else ''
        
        # Verifica se o último argumento é uma data
        data_str = None
        if len(args) > 1:
            possible_date = args[-1]
            if '/' in possible_date or '-' in possible_date:
                data_str = possible_date
                descricao = ' '.join(args[1:-1])
        
        # Valida o valor
        valor = parse_value(valor_str)
        if valor is None:
            return ERROR_INVALID_VALUE
        
        # Parse da data
        data = parse_date(data_str)
        
        # Adiciona o lançamento
        lancamento = self.add_lancamento(numero, 'saida', valor, descricao, data)
        
        # Calcula novo saldo
        user_data = self.get_user_data(numero)
        saldo = calculate_balance(user_data['lancamentos'])
        
        # Formata resposta
        lancamento_str = format_lancamento(lancamento)
        saldo_str = format_currency(saldo)
        
        response = f"{lancamento_str}\n💰 Seu saldo: {saldo_str}"
        
        # TODO: Enviar para observadores
        self._notify_observers(numero, response)
        
        return response
    
    def process_saldo(self, numero: str) -> str:
        """Processa comando de saldo."""
        user_data = self.get_user_data(numero)
        
        saldo = calculate_balance(user_data['lancamentos'])
        
        # Conta lançamentos do mês atual
        month = datetime.now().strftime("%m/%Y")
        lancamentos_mes = sum(1 for l in user_data['lancamentos'] 
                             if l.get('data', '').endswith(month))
        
        saldo_str = format_currency(saldo)
        return f"💰 Seu saldo: {saldo_str} ({lancamentos_mes} lançamentos no mês)"
    
    def process_listar(self, numero: str, args: List[str]) -> str:
        """Processa comando de listar."""
        user_data = self.get_user_data(numero)
        
        # Determina quantos lançamentos mostrar
        limit = 5  # padrão
        if args and args[0].isdigit():
            limit = min(int(args[0]), 20)  # máximo 20
        
        lancamentos = user_data['lancamentos'][-limit:]
        
        if not lancamentos:
            return "📄 Nenhum lançamento encontrado."
        
        response = "📄 Últimos lançamentos:\n"
        for i, lancamento in enumerate(reversed(lancamentos), 1):
            lancamento_str = format_lancamento(lancamento)
            response += f"{i}) {lancamento_str}\n"
        
        return response
    
    def process_resumo(self, numero: str) -> str:
        """Processa comando de resumo."""
        user_data = self.get_user_data(numero)
        
        month = datetime.now().strftime("%m/%Y")
        summary = get_month_summary(user_data['lancamentos'], month)
        
        entradas_str = format_currency(summary['entradas'])
        saidas_str = format_currency(summary['saidas'])
        saldo_str = format_currency(summary['saldo'])
        
        return f"""📅 Resumo {month}
Entradas: {entradas_str}
Saídas:   {saidas_str}
Saldo:    {saldo_str}"""
    
    def process_desfazer(self, numero: str) -> str:
        """Processa comando de desfazer."""
        user_data = self.get_user_data(numero)
        
        if not user_data['lancamentos']:
            return "❌ Nenhum lançamento para desfazer."
        
        # Remove último lançamento
        ultimo_lancamento = user_data['lancamentos'].pop()
        self.save_data()
        
        # Calcula novo saldo
        saldo = calculate_balance(user_data['lancamentos'])
        
        # Formata resposta
        lancamento_str = format_lancamento(ultimo_lancamento)
        saldo_str = format_currency(saldo)
        
        response = f"❌ Lançamento removido:\n{lancamento_str}\n💰 Saldo atualizado: {saldo_str}"
        
        # TODO: Enviar para observadores
        self._notify_observers(numero, response)
        
        return response
    
    def process_cadastrar(self, numero: str, args: List[str]) -> str:
        """Processa comando de cadastrar observador."""
        if not args:
            return "❗ Informe o número do observador. Exemplo: cadastrar +551199999999"
        
        observador = args[0]
        
        # Validação básica do número
        if not re.match(r'^\+\d{10,15}$', observador):
            return "❗ Formato de número inválido. Use: +551199999999"
        
        if self.add_observador(numero, observador):
            # Formata número para exibição
            formatted_number = self._format_phone_number(observador)
            return f"✅ Observador adicionado: {formatted_number}"
        else:
            return "❗ Este número já está na lista de observadores."
    
    def process_remover(self, numero: str, args: List[str]) -> str:
        """Processa comando de remover observador."""
        if not args:
            return "❗ Informe o número do observador. Exemplo: remover +551199999999"
        
        observador = args[0]
        
        if self.remove_observador(numero, observador):
            formatted_number = self._format_phone_number(observador)
            return f"❌ Observador removido: {formatted_number}"
        else:
            return "❗ Este número não está na lista de observadores."
    
    def process_message(self, numero: str, message: str) -> str:
        """
        Processa uma mensagem recebida do WhatsApp.
        
        Args:
            numero: Número do remetente
            message: Mensagem recebida
            
        Returns:
            Resposta para enviar
        """
        parsed = self.parse_command(message)
        command = parsed['command']
        args = parsed['args']
        
        if command == 'entrada':
            return self.process_entrada(numero, args)
        elif command == 'saida':
            return self.process_saida(numero, args)
        elif command == 'saldo':
            return self.process_saldo(numero)
        elif command == 'listar':
            return self.process_listar(numero, args)
        elif command == 'resumo':
            return self.process_resumo(numero)
        elif command == 'desfazer':
            return self.process_desfazer(numero)
        elif command == 'cadastrar':
            return self.process_cadastrar(numero, args)
        elif command == 'remover':
            return self.process_remover(numero, args)
        elif command in ['start', 'help', 'ajuda']:
            return WELCOME_MESSAGE
        else:
            return "❗ Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."
    
    def _notify_observers(self, numero: str, message: str):
        """
        Notifica observadores sobre uma movimentação.
        
        NOTA: Esta função é um placeholder. Para implementação real,
        seria necessário integração com API do WhatsApp.
        """
        user_data = self.get_user_data(numero)
        
        for observador in user_data['observadores']:
            # TODO: Enviar mensagem para o observador
            # Exemplo: send_whatsapp_message(observador, message)
            print(f"[OBSERVER] Para {observador}: {message}")
    
    def _format_phone_number(self, number: str) -> str:
        """Formata número de telefone para exibição."""
        # Remove o + e formata como +55 11 99999-9999
        if number.startswith('+55'):
            digits = number[3:]
            if len(digits) == 11:
                return f"+55 {digits[:2]} {digits[2:7]}-{digits[7:]}"
        
        return number


# Exemplo de uso (para testes)
if __name__ == '__main__':
    bot = WhatsAppFinanceBot()
    
    # Simula algumas interações
    numero = "+5511999999999"
    
    print("Bot WhatsApp - Teste")
    print("=" * 30)
    
    # Teste de comandos
    commands = [
        "entrada 1500 salário",
        "saida 89,90 mercado",
        "saldo",
        "listar",
        "resumo",
        "cadastrar +5511888888888",
        "desfazer"
    ]
    
    for cmd in commands:
        print(f"\n> {cmd}")
        response = bot.process_message(numero, cmd)
        print(response)

