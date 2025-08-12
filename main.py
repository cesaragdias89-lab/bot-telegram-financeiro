#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot de Controle Financeiro - Arquivo Principal

Este arquivo permite executar o bot do Telegram ou testar o módulo do WhatsApp.

Uso:
    python3 main.py telegram    # Executa bot do Telegram
    python3 main.py whatsapp    # Testa bot do WhatsApp
    python3 main.py test        # Executa testes
"""

import sys
import os

def run_telegram_bot():
    """Executa o bot do Telegram."""
    try:
        from telegram_bot import create_telegram_bot
        
        print("🤖 Iniciando Bot do Telegram...")
        print("📱 Para parar, pressione Ctrl+C")
        print("-" * 40)
        
        app = create_telegram_bot()
        app.run_polling()
        
    except ValueError as e:
        print(f"❌ Erro de configuração: {e}")
        print("\n💡 Dicas:")
        print("1. Defina a variável TELEGRAM_BOT_TOKEN")
        print("2. Ou edite config.py com seu token")
        print("\nPara obter um token:")
        print("1. Abra o Telegram")
        print("2. Procure por @BotFather")
        print("3. Digite /newbot e siga as instruções")
        
    except KeyboardInterrupt:
        print("\n👋 Bot do Telegram finalizado.")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


def run_whatsapp_test():
    """Executa teste do bot do WhatsApp."""
    try:
        from whatsapp_bot import WhatsAppFinanceBot
        
        print("🤖 Testando Bot do WhatsApp...")
        print("📱 Simulação de comandos")
        print("-" * 40)
        
        bot = WhatsAppFinanceBot()
        numero = "+5511999999999"
        
        # Comandos de teste
        commands = [
            ("entrada 1500 salário", "💰 Registrando entrada"),
            ("saida 89,90 mercado 11/08/2025", "💸 Registrando saída"),
            ("saldo", "📊 Consultando saldo"),
            ("listar 3", "📄 Listando lançamentos"),
            ("resumo", "📅 Resumo do mês"),
            ("cadastrar +5511888888888", "👥 Adicionando observador"),
            ("desfazer", "↩️ Desfazendo último lançamento")
        ]
        
        for cmd, desc in commands:
            print(f"\n{desc}")
            print(f"👤 Usuário: {cmd}")
            response = bot.process_message(numero, cmd)
            print(f"🤖 Bot: {response}")
        
        print("\n✅ Teste do WhatsApp concluído!")
        print("⚠️  Nota: Para usar no WhatsApp real, é necessário integração com API Business")
        
    except Exception as e:
        print(f"❌ Erro no teste do WhatsApp: {e}")


def run_tests():
    """Executa os testes unitários."""
    try:
        from test_bot import run_tests
        
        print("🧪 Executando Testes Unitários...")
        print("-" * 40)
        
        success = run_tests()
        
        if success:
            print("\n🎉 Todos os testes passaram!")
        else:
            print("\n⚠️  Alguns testes falharam. Verifique os detalhes acima.")
            
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")


def show_help():
    """Mostra ajuda de uso."""
    print("🤖 Bot de Controle Financeiro")
    print("=" * 40)
    print("\nUso:")
    print("  python3 main.py telegram    # Executa bot do Telegram")
    print("  python3 main.py whatsapp    # Testa bot do WhatsApp")
    print("  python3 main.py test        # Executa testes")
    print("  python3 main.py help        # Mostra esta ajuda")
    print("\nPara mais informações, consulte o README.md")


def main():
    """Função principal."""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'telegram':
        run_telegram_bot()
    elif command == 'whatsapp':
        run_whatsapp_test()
    elif command == 'test':
        run_tests()
    elif command in ['help', '-h', '--help']:
        show_help()
    else:
        print(f"❌ Comando desconhecido: {command}")
        show_help()


if __name__ == '__main__':
    main()

