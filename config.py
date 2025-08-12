# Configurações do Bot de Controle Financeiro

import os

# Token do bot do Telegram (deve ser definido como variável de ambiente)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'SEU_TOKEN_AQUI')

# Configurações de armazenamento
DATA_DIR = 'data'
TELEGRAM_DATA_FILE = 'telegram_groups.json'
WHATSAPP_DATA_FILE = 'whatsapp_users.json'

# Configurações de formatação
CURRENCY_SYMBOL = 'R$'
DATE_FORMAT = '%d/%m/%Y'

# Mensagens do bot
WELCOME_MESSAGE = """👋 Olá! Sou seu bot de controle de gastos.

No Telegram:
• /entrada 1500 salário
• /saida 35 mercado
• /saldo
• /listar
• /resumo

No WhatsApp (sem barra):
• entrada 1500 salário
• saida 35 mercado
• saldo
• listar
• resumo

💡 No WhatsApp, use "cadastrar <número>" para adicionar observadores."""

ERROR_INVALID_VALUE = "❗ Valor inválido. Exemplo: /saida 150 mercado"

