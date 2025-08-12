# Bot de Controle Financeiro

Um bot simples para Telegram e WhatsApp que permite registrar entradas, saídas e visualizar saldo para controle financeiro pessoal.

## 📋 Funcionalidades

### Telegram (Grupo)
- Saldo compartilhado entre todos os membros do grupo
- Qualquer membro pode registrar lançamentos
- Respostas mostram quem fez a ação e o saldo do grupo

### WhatsApp (Individual)
- Cada usuário tem seu próprio controle
- Pode cadastrar observadores que recebem cópia das movimentações
- Observadores recebem a mesma mensagem que o autor

## 🚀 Comandos Disponíveis

### Comandos Principais

#### Entrada de Dinheiro
- **Telegram:** `/entrada <valor> [descrição] [data opcional]`
- **WhatsApp:** `entrada <valor> [descrição] [data opcional]`

Exemplo:
```
/entrada 1500 salário
entrada 89,90 freelance 11/08/2025
```

#### Saída de Dinheiro
- **Telegram:** `/saida <valor> [descrição] [data opcional]`
- **WhatsApp:** `saida <valor> [descrição] [data opcional]`

Exemplo:
```
/saida 89,90 mercado
saida 150 combustível 10/08/2025
```

#### Consultar Saldo
- **Telegram:** `/saldo`
- **WhatsApp:** `saldo`

#### Listar Últimos Lançamentos
- **Telegram:** `/listar [quantidade]`
- **WhatsApp:** `listar [quantidade]`

Exemplo:
```
/listar 10
```

#### Resumo do Mês
- **Telegram:** `/resumo`
- **WhatsApp:** `resumo`

#### Desfazer Último Lançamento
- **Telegram:** `/desfazer`
- **WhatsApp:** `desfazer`

### Comandos Extras (WhatsApp)

#### Cadastrar Observador
```
cadastrar +551199999999
```

#### Remover Observador
```
remover +551199999999
```

## 📦 Estrutura do Projeto

```
bot_financeiro/
├── config.py              # Configurações do bot
├── utils.py               # Funções utilitárias
├── telegram_bot.py        # Bot do Telegram
├── whatsapp_bot.py        # Bot do WhatsApp (estrutura)
├── test_bot.py           # Testes unitários
├── README.md             # Esta documentação
└── data/                 # Diretório de dados (criado automaticamente)
    ├── telegram_groups.json
    └── whatsapp_users.json
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.7+
- pip

### 1. Instalar Dependências
```bash
pip install python-telegram-bot
```

### 2. Configurar Token do Telegram

#### Obter Token do Bot
1. Abra o Telegram e procure por `@BotFather`
2. Digite `/newbot` e siga as instruções
3. Copie o token fornecido

#### Configurar Token
Defina a variável de ambiente com seu token:

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="SEU_TOKEN_AQUI"
```

**Windows:**
```cmd
set TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI
```

Ou edite o arquivo `config.py` e substitua `'SEU_TOKEN_AQUI'` pelo seu token.

### 3. Executar o Bot do Telegram
```bash
python3 telegram_bot.py
```

### 4. Testar o Bot do WhatsApp (Simulação)
```bash
python3 whatsapp_bot.py
```

## 🧪 Executar Testes
```bash
python3 test_bot.py
```

## 📱 Como Usar

### No Telegram
1. Adicione o bot ao seu grupo
2. Digite `/start` para ver a mensagem de boas-vindas
3. Use os comandos com `/` (ex: `/entrada 1500 salário`)

### No WhatsApp (Implementação Futura)
O módulo do WhatsApp está estruturado, mas requer integração com:
- API oficial do WhatsApp Business
- Ou soluções de terceiros como `whatsapp-web.js`

## 💾 Armazenamento de Dados

Os dados são armazenados em arquivos JSON no diretório `data/`:

### Telegram (telegram_groups.json)
```json
{
  "CHAT_ID_DO_GRUPO": {
    "chat_id": "CHAT_ID_DO_GRUPO",
    "lancamentos": [
      {
        "tipo": "entrada",
        "valor": 1500.0,
        "descricao": "salário",
        "data": "12/08/2025",
        "autor": "João"
      }
    ]
  }
}
```

### WhatsApp (whatsapp_users.json)
```json
{
  "+5511999999999": {
    "numero": "+5511999999999",
    "lancamentos": [
      {
        "tipo": "saida",
        "valor": 89.90,
        "descricao": "mercado",
        "data": "12/08/2025"
      }
    ],
    "observadores": ["+5511888888888"]
  }
}
```

## ⚙️ Regras de UX

- **Valores:** Formatados em R$ com vírgula decimal (ex: R$ 1.234,56)
- **Entrada:** Aceita vírgula ou ponto nos valores digitados
- **Data:** Se não informada, usa data atual
- **Validação:** Valores inválidos retornam mensagem de erro
- **Telegram:** Respostas prefixadas com nome do autor
- **WhatsApp:** Respostas diretas (individual)

## 🚧 Status de Implementação

### ✅ Implementado
- [x] Bot do Telegram completo
- [x] Estrutura do bot do WhatsApp
- [x] Todos os comandos financeiros
- [x] Sistema de armazenamento JSON
- [x] Testes unitários
- [x] Validação de entrada
- [x] Formatação de moeda brasileira

### 🔄 Para Implementação Futura
- [ ] Integração real com WhatsApp (requer API Business)
- [ ] Interface web para visualização
- [ ] Relatórios em PDF
- [ ] Backup automático
- [ ] Múltiplas moedas

## 🐛 Solução de Problemas

### Erro: "Token do Telegram não configurado"
- Verifique se definiu a variável `TELEGRAM_BOT_TOKEN`
- Ou edite `config.py` com seu token

### Bot não responde no Telegram
- Verifique se o token está correto
- Certifique-se de que o bot foi adicionado ao grupo
- Verifique a conexão com a internet

### Dados não são salvos
- Verifique permissões de escrita no diretório
- Certifique-se de que o diretório `data/` pode ser criado

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação acima
2. Execute os testes: `python3 test_bot.py`
3. Verifique os logs de erro no console

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente para fins pessoais e educacionais.

---

**Desenvolvido com ❤️ para controle financeiro pessoal**

