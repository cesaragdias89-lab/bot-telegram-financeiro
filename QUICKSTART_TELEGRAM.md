# Quickstart — Bot de Controle Financeiro (Telegram)

## 1) Criar o bot no Telegram
1. Abra o Telegram e fale com **@BotFather**
2. Envie: `/newbot`
3. Dê um nome e um username (termina com `bot`)
4. Copie o **TOKEN** (formato `123456:ABC...`)

## 2) Configurar o projeto
- Na pasta do projeto, copie `.env.example` para `.env` e edite:
  ```
  TELEGRAM_TOKEN=SEU_TOKEN_AQUI
  DATA_DIR=./data
  TZ=America/Sao_Paulo
  LOG_LEVEL=INFO
  ```

## 3) Rodar
**Windows**: clique duas vezes em `rodar_no_windows.bat` (ou rode no Prompt).
**Linux/Mac**:
```bash
chmod +x rodar_no_linux.sh
./rodar_no_linux.sh
```

## 4) Testar
- No Telegram, abra o chat com seu bot e envie:
  - `/entrada 100 teste`
  - `/saida 10`
  - `/saldo`

## 5) Colocar em grupo (saldo compartilhado)
- Crie um grupo e adicione o seu bot
- Envie comandos no grupo; todos verão os lançamentos e o saldo

## Dúvidas comuns
- Se o bot não responder: confira se o token no `.env` está correto e se o terminal mostra "rodando".
- Erro de permissão na pasta `data`: rode o terminal como administrador (Windows) ou `chmod -R 755 data` (Linux/Mac).
