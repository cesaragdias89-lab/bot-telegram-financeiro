# Bot do Telegram para Controle Financeiro

import logging
from datetime import datetime
from typing import List, Dict, Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import TELEGRAM_BOT_TOKEN, WELCOME_MESSAGE, ERROR_INVALID_VALUE, TELEGRAM_DATA_FILE
from utils import (
    parse_value, parse_date, format_currency, load_json_data, save_json_data,
    calculate_balance, get_month_summary, format_lancamento
)

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class TelegramFinanceBot:
    """Bot do Telegram para controle financeiro."""
    
    def __init__(self):
        self.data = load_json_data(TELEGRAM_DATA_FILE)
    
    def save_data(self):
        """Salva os dados do bot."""
        save_json_data(TELEGRAM_DATA_FILE, self.data)
    
    def get_group_data(self, chat_id: str) -> Dict[str, Any]:
        """Obtém dados do grupo."""
        if chat_id not in self.data:
            self.data[chat_id] = {
                'chat_id': chat_id,
                'lancamentos': []
            }
        return self.data[chat_id]
    
    def add_lancamento(self, chat_id: str, tipo: str, valor: float, descricao: str, data: str, autor: str):
        """Adiciona um lançamento."""
        group_data = self.get_group_data(chat_id)
        
        lancamento = {
            'tipo': tipo,
            'valor': valor,
            'descricao': descricao,
            'data': data,
            'autor': autor
        }
        
        group_data['lancamentos'].append(lancamento)
        self.save_data()
        
        return lancamento
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - mensagem de boas-vindas."""
        await update.message.reply_text(WELCOME_MESSAGE)
    
    async def entrada_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /entrada - registra entrada de dinheiro."""
        if not context.args:
            await update.message.reply_text(ERROR_INVALID_VALUE)
            return
        
        # Parse dos argumentos
        valor_str = context.args[0]
        descricao = ' '.join(context.args[1:]) if len(context.args) > 1 else ''
        
        # Verifica se o último argumento é uma data
        data_str = None
        if len(context.args) > 1:
            possible_date = context.args[-1]
            if '/' in possible_date or '-' in possible_date:
                data_str = possible_date
                # Remove a data da descrição
                descricao = ' '.join(context.args[1:-1])
        
        # Valida o valor
        valor = parse_value(valor_str)
        if valor is None:
            await update.message.reply_text(ERROR_INVALID_VALUE)
            return
        
        # Parse da data
        data = parse_date(data_str)
        
        # Obtém informações do usuário
        user = update.effective_user
        autor = user.first_name or user.username or "Usuário"
        chat_id = str(update.effective_chat.id)
        
        # Adiciona o lançamento
        lancamento = self.add_lancamento(chat_id, 'entrada', valor, descricao, data, autor)
        
        # Calcula novo saldo
        group_data = self.get_group_data(chat_id)
        saldo = calculate_balance(group_data['lancamentos'])
        
        # Formata resposta
        lancamento_str = format_lancamento(lancamento, include_author=True)
        saldo_str = format_currency(saldo)
        
        response = f"{lancamento_str}\n💰 Saldo do grupo: {saldo_str}"
        await update.message.reply_text(response)
    
    async def saida_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /saida - registra saída de dinheiro."""
        if not context.args:
            await update.message.reply_text(ERROR_INVALID_VALUE)
            return
        
        # Parse dos argumentos (mesmo processo da entrada)
        valor_str = context.args[0]
        descricao = ' '.join(context.args[1:]) if len(context.args) > 1 else ''
        
        # Verifica se o último argumento é uma data
        data_str = None
        if len(context.args) > 1:
            possible_date = context.args[-1]
            if '/' in possible_date or '-' in possible_date:
                data_str = possible_date
                descricao = ' '.join(context.args[1:-1])
        
        # Valida o valor
        valor = parse_value(valor_str)
        if valor is None:
            await update.message.reply_text(ERROR_INVALID_VALUE)
            return
        
        # Parse da data
        data = parse_date(data_str)
        
        # Obtém informações do usuário
        user = update.effective_user
        autor = user.first_name or user.username or "Usuário"
        chat_id = str(update.effective_chat.id)
        
        # Adiciona o lançamento
        lancamento = self.add_lancamento(chat_id, 'saida', valor, descricao, data, autor)
        
        # Calcula novo saldo
        group_data = self.get_group_data(chat_id)
        saldo = calculate_balance(group_data['lancamentos'])
        
        # Formata resposta
        lancamento_str = format_lancamento(lancamento, include_author=True)
        saldo_str = format_currency(saldo)
        
        response = f"{lancamento_str}\n💰 Saldo do grupo: {saldo_str}"
        await update.message.reply_text(response)
    
    async def saldo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /saldo - mostra saldo atual."""
        chat_id = str(update.effective_chat.id)
        group_data = self.get_group_data(chat_id)
        
        saldo = calculate_balance(group_data['lancamentos'])
        total_lancamentos = len(group_data['lancamentos'])
        
        # Conta lançamentos do mês atual
        month = datetime.now().strftime("%m/%Y")
        lancamentos_mes = sum(1 for l in group_data['lancamentos'] 
                             if l.get('data', '').endswith(month))
        
        saldo_str = format_currency(saldo)
        response = f"💰 Saldo atual do grupo: {saldo_str} ({lancamentos_mes} lançamentos no mês)"
        
        await update.message.reply_text(response)
    
    async def listar_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /listar - lista últimos lançamentos."""
        chat_id = str(update.effective_chat.id)
        group_data = self.get_group_data(chat_id)
        
        # Determina quantos lançamentos mostrar
        limit = 5  # padrão
        if context.args and context.args[0].isdigit():
            limit = min(int(context.args[0]), 20)  # máximo 20
        
        lancamentos = group_data['lancamentos'][-limit:]
        
        if not lancamentos:
            await update.message.reply_text("📄 Nenhum lançamento encontrado.")
            return
        
        response = "📄 Últimos lançamentos:\n"
        for i, lancamento in enumerate(reversed(lancamentos), 1):
            lancamento_str = format_lancamento(lancamento, include_author=True)
            response += f"{i}) {lancamento_str}\n"
        
        await update.message.reply_text(response)
    
    async def resumo_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /resumo - mostra resumo do mês."""
        chat_id = str(update.effective_chat.id)
        group_data = self.get_group_data(chat_id)
        
        month = datetime.now().strftime("%m/%Y")
        summary = get_month_summary(group_data['lancamentos'], month)
        
        entradas_str = format_currency(summary['entradas'])
        saidas_str = format_currency(summary['saidas'])
        saldo_str = format_currency(summary['saldo'])
        
        response = f"""📅 Resumo {month}
Entradas: {entradas_str}
Saídas:   {saidas_str}
Saldo:    {saldo_str}"""
        
        await update.message.reply_text(response)
    
    async def desfazer_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /desfazer - remove último lançamento."""
        chat_id = str(update.effective_chat.id)
        group_data = self.get_group_data(chat_id)
        
        if not group_data['lancamentos']:
            await update.message.reply_text("❌ Nenhum lançamento para desfazer.")
            return
        
        # Remove último lançamento
        ultimo_lancamento = group_data['lancamentos'].pop()
        self.save_data()
        
        # Calcula novo saldo
        saldo = calculate_balance(group_data['lancamentos'])
        
        # Formata resposta
        lancamento_str = format_lancamento(ultimo_lancamento, include_author=True)
        saldo_str = format_currency(saldo)
        
        response = f"❌ Lançamento removido:\n{lancamento_str}\n💰 Saldo atualizado: {saldo_str}"
        await update.message.reply_text(response)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manipulador de erros."""
        logger.error(f"Erro: {context.error}")
        if update and update.message:
            await update.message.reply_text("❌ Ocorreu um erro. Tente novamente.")


def create_telegram_bot() -> Application:
    """Cria e configura o bot do Telegram."""
    if TELEGRAM_BOT_TOKEN == 'SEU_TOKEN_AQUI':
        raise ValueError("Token do Telegram não configurado. Defina a variável TELEGRAM_BOT_TOKEN.")
    
    # Cria a aplicação
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Instancia o bot
    bot = TelegramFinanceBot()
    
    # Adiciona handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("entrada", bot.entrada_command))
    application.add_handler(CommandHandler("saida", bot.saida_command))
    application.add_handler(CommandHandler("saldo", bot.saldo_command))
    application.add_handler(CommandHandler("listar", bot.listar_command))
    application.add_handler(CommandHandler("resumo", bot.resumo_command))
    application.add_handler(CommandHandler("desfazer", bot.desfazer_command))
    
    # Handler de erro
    application.add_error_handler(bot.error_handler)
    
    return application


if __name__ == '__main__':
    # Executa o bot
    try:
        app = create_telegram_bot()
        print("Bot do Telegram iniciado. Pressione Ctrl+C para parar.")
        app.run_polling()
    except ValueError as e:
        print(f"Erro de configuração: {e}")
    except Exception as e:
        print(f"Erro ao iniciar bot: {e}")

