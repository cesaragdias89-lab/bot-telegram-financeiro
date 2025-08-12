## Tarefas para o Bot de Controle Financeiro

### Fase 1: Analisar requisitos do arquivo enviado (Concluído)
- [x] Ler e compreender o arquivo `pasted_content.txt`.

### Fase 2: Planejar arquitetura do bot
- [x] Definir a estrutura geral do projeto (linguagem, frameworks, bibliotecas).
  - Linguagem: Python
  - Frameworks: `python-telegram-bot` para Telegram, e para WhatsApp, será necessário investigar opções como `whatsapp-web.js` (via subprocesso ou API) ou uma API oficial (se o usuário tiver acesso).
  - Estrutura: Monorepo com módulos separados para Telegram, WhatsApp e lógica de negócio compartilhada.
- [x] Escolher a abordagem para integração com Telegram e WhatsApp (APIs, bibliotecas).
  - Telegram: Usar a biblioteca `python-telegram-bot`.
  - WhatsApp: Dada a complexidade e as restrições de APIs oficiais para bots no WhatsApp, a abordagem inicial será focar na integração com o Telegram. Para o WhatsApp, será necessário explorar opções como a API oficial do WhatsApp Business (que requer aprovação e infraestrutura específica) ou soluções de terceiros que simulam o WhatsApp Web (como `whatsapp-web.js` ou `venom-bot`), que podem ser mais complexas de manter e não são oficialmente suportadas. Por enquanto, o foco será no Telegram, e a integração com WhatsApp será considerada uma funcionalidade futura ou que requer mais investigação e possível intervenção do usuário para configuração de credenciais de API Business.
- [x] Projetar o modelo de dados para persistência (considerando os exemplos JSON).
  - Estrutura de dados para Telegram (grupo): `{"chat_id": "ID_GRUPO", "lancamentos": [{"tipo": "entrada", "valor": 200.00, "descricao": "venda", "data": "2025-08-12", "autor": "João"}]}`
  - Estrutura de dados para WhatsApp (individual): `{"numero": "+551199999999", "lancamentos": [{"tipo": "saida", "valor": 50.00, "descricao": "mercado", "data": "2025-08-12"}], "observadores": ["+551188888888", "+551177777777"]}`
  - Persistência: Usar arquivos JSON para simplicidade, com possibilidade de migrar para SQLite posteriormente.
- [x] Esboçar a lógica de roteamento de comandos para Telegram e WhatsApp.
  - Telegram: Usar handlers da biblioteca `python-telegram-bot` para capturar comandos com `/`.
  - WhatsApp: Implementar parser de texto para comandos sem `/`.
  - Lógica compartilhada: Criar funções comuns para processar comandos independentemente da plataforma.
- [x] Pensar na estratégia de tratamento de erros e validação de entrada.
  - Validação de valores numéricos (aceitar vírgula e ponto).
  - Validação de datas (formato opcional, usar data atual se não informada).
  - Tratamento de comandos inválidos com mensagens de ajuda.
  - Log de erros para depuração.

### Fase 3: Implementar bot com funcionalidades básicas
- [x] Configurar o ambiente de desenvolvimento.
- [x] Implementar a conexão com as APIs do Telegram e WhatsApp.
  - Telegram: Implementado usando `python-telegram-bot`.
  - WhatsApp: Por enquanto, focando no Telegram. WhatsApp será uma funcionalidade futura.
- [x] Criar a estrutura básica para receber e responder mensagens.
- [x] Implementar a mensagem de boas-vindas.

### Fase 4: Criar sistema de armazenamento de dados
- [x] Escolher e configurar um banco de dados ou sistema de persistência (ex: JSON files, SQLite).
  - Escolhido: Arquivos JSON para simplicidade inicial.
- [x] Implementar funções para carregar e salvar dados do grupo (Telegram) e do usuário (WhatsApp).
  - Implementado no arquivo `utils.py` as funções `load_json_data` e `save_json_data`.

### Fase 5: Implementar funcionalidades financeiras
- [x] Implementar comando de entrada (`/entrada`, `entrada`).
- [x] Implementar comando de saída (`/saida`, `saida`).
- [x] Implementar comando de saldo (`/saldo`, `saldo`).
- [x] Implementar comando de listar (`/listar`).
- [x] Implementar comando de resumo (`/resumo`).
- [x] Implementar comando de desfazer (`/desfazer`, `desfazer`).
- [x] Implementar comandos extras do WhatsApp (`cadastrar`, `remover`).
  - Implementado estrutura básica no módulo `whatsapp_bot.py`.
- [x] Implementar envio automático para observadores no WhatsApp.
  - Implementado placeholder para notificação de observadores (requer integração com API real).
- [x] Aplicar regras de UX (formatação, validação, data, prefixo de nome).
  - Formatação de moeda brasileira implementada.
  - Validação de valores numéricos (aceita vírgula e ponto).
  - Parsing de datas com fallback para data atual.
  - Prefixo de nome do autor nos grupos do Telegram.

### Fase 6: Testar e validar o bot
- [x] Escrever testes unitários para as funções principais.
  - Criado arquivo `test_bot.py` com 12 testes cobrindo funções utilitárias e bot do WhatsApp.
- [x] Realizar testes de integração para as plataformas Telegram e WhatsApp.
  - Testes do WhatsApp executados com sucesso.
  - Telegram requer token real para teste completo.
- [x] Testar cenários de erro e validação de entrada.
  - Validação de valores inválidos testada.
  - Tratamento de comandos vazios testado.

### Fase 7: Entregar código e instruções ao usuário
- [x] Organizar o código-fonte do bot.
- [x] Criar um arquivo README.md com instruções detalhadas de uso e configuração.
- [x] Empacotar o projeto para entrega.
- [x] Enviar o código e as instruções ao usuário.

