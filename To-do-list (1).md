---

# Documento de Contexto — Projeto To-do List

## Objetivo do projeto

Construir uma To-do list usando **Python + Flask + MySQL**, com autenticação completa (login, cadastro, 2FA via TOTP), focado em aprendizado, arquitetura limpa e construção de portfólio para estágio.

O objetivo não é criar um produto completo, mas um sistema pequeno, funcional e bem estruturado.

---

# Progresso de Implementação

Construção seguindo ordem "de baixo para cima": banco → database → repository → utils → service → routes → templates.

```text
✅ Banco de dados criado (tabelas users e tasks)
✅ database/connection.py
✅ repository/user_repository.py (inclui find_user_by_id)
✅ repository/task_repository.py
✅ utils/auth_utils.py
✅ utils/totp_utils.py
✅ exceptions.py (classe BusinessError)
✅ service/auth_service.py — completo (cadastro, login, 2FA setup e verificação)
✅ service/task_service.py — completo (create, list c/ filtro, update, delete, update_task_status)
✅ service/user_service.py — completo (avatar, troca de senha)
✅ CAMADA DE SERVICE 100% COMPLETA E TESTADA MANUALMENTE
✅ Testes manuais (manual_test.py, na raiz do projeto, fora de src/) — cobertura completa:
   auth (cadastro, login, política de senha), tasks (CRUD + filtro + status),
   perfil (avatar, troca de senha), 2FA (setup, confirmação, login) — tudo validado
   contra o banco real, incluindo casos de erro
◻ routes/ — próximo passo
◻ templates/ — nenhum template escrito ainda
```

## Bug encontrado e corrigido em teste manual

`check_password()` estourava `TypeError` no login — o MySQL/pymysql devolve `password_hash` como `str`, não `bytes`, mesmo o hash tendo sido gerado e salvo originalmente como bytes. Corrigido convertendo com `isinstance(password_hash, str)` antes de chamar `checkpw()`. Lição: sempre testar o caminho completo (banco real) antes de assumir que os tipos se mantêm — o tipo do dado pode mudar ao ir e voltar do banco.

Nenhum dos dois bugs reais do projeto (esse, e a lacuna de `update_task_status`) teria sido percebido só lendo o código — só apareceram testando contra o banco de verdade, com dados reais. Testes manuais valeram o esforço.

---

# Escopo Atual

## Funcionalidades que existirão

* Cadastro de usuário com validação de email duplicado
* Login com email e senha
* Autenticação em dois fatores (2FA) via TOTP (Google Authenticator, Authy)
* Sessão do Flask para manter o usuário logado
* Proteção de rotas — usuário sem login não acessa páginas internas
* Troca de senha na aba de perfil
* Avatar fixo escolhido pelo usuário (lista de opções pré-definidas)
* Criação de tarefas com título e descrição
* CRUD completo das tarefas (criar, ler, editar, deletar)
* Filtro de tarefas por status: pendente e concluído

---

## Funcionalidades que NÃO existirão agora

Esses itens foram removidos do escopo para manter simplicidade:

* Upload de imagem de perfil pelo usuário
* Data limite nas tarefas
* Prioridade nas tarefas
* Categorias ou listas de tarefas
* Cache
* Analytics
* Alteração de username
* Gamificação de XP
* Histórico de tarefas deletadas

Podem existir futuramente.

---

# Stack

## Backend

* Python

## Framework

* Flask

## Banco

* MySQL

## ORM

* Não usar ORM — SQL puro

## Autenticação

* Sessão do Flask (`flask-session` nativo)
* bcrypt para hash de senha
* pyotp para geração e validação de TOTP (2FA)
* qrcode para gerar o QR code de configuração do 2FA

## Configuração

* python-dotenv para variáveis de ambiente (.env)

---

# Variáveis de Ambiente

Arquivo `.env` na raiz do projeto. Nunca subir para o repositório (adicionar no `.gitignore`).

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=todolist
DB_USER=root
DB_PASSWORD=sua_senha_aqui
SECRET_KEY=chave_secreta_para_sessao
```

---

# Arquitetura

Projeto dividido em camadas.

Fluxo:

```text
Route
↓
Service
↓
Repository
↓
Database
```

Utilitários separados.

---

# Estrutura de Pastas

```text
src/
└── app/
    ├── templates/
    │   └── # páginas HTML (Jinja2)
    ├── static/
    │   ├── css/
    │   │   └── # arquivos CSS
    │   └── avatars/
    │       └── # imagens de avatar pré-definidas
    ├── routes/
    │   ├── auth_routes.py      # cadastro, login, logout, 2FA
    │   ├── user_routes.py      # perfil, troca de senha, avatar
    │   └── task_routes.py      # CRUD de tarefas
    ├── service/
    │   ├── auth_service.py     # regras de autenticação
    │   ├── user_service.py     # regras de perfil
    │   └── task_service.py     # regras de tarefas
    ├── repository/
    │   ├── user_repository.py  # SQL de usuários
    │   └── task_repository.py  # SQL de tarefas
    ├── database/
    │   └── connection.py       # conexão com MySQL
    ├── utils/
    │   ├── auth_utils.py       # validação de email/senha, hash de senha
    │   └── totp_utils.py       # geração e validação de TOTP
    └── exceptions.py           # classe BusinessError (erros de regra de negócio)

└── main.py
└── .env
└── .gitignore
└── requirements.txt
```

---

# Responsabilidades

## routes/

Responsável por:

* Receber requisição HTTP
* Validar formato básico dos dados do formulário
* Chamar o service correspondente
* Redirecionar ou retornar resposta HTTP

Não contém regra de negócio.

---

## service/

Responsável por:

* Coordenar o fluxo da funcionalidade
* Aplicar regras de negócio (ex: email já existe, senha incorreta)
* Chamar o repository para persistência
* Chamar utils quando necessário

Não executa SQL.

---

## repository/

Responsável por:

* Executar SQL diretamente
* Inserir, buscar, atualizar e deletar registros
* Retornar dados para o service

Não contém regra de negócio.

---

## database/

Responsável por:

* Criar e retornar conexão com o MySQL
* Ler credenciais do arquivo .env

---

## utils/

### auth_utils.py

* Validar formato de email (regex)
* Validar se string está vazia (com defesa contra None)
* Validar política de senha (tamanho, maiúscula, número) — retorna mensagem de erro específica ou `None`, sem lançar `BusinessError` diretamente (mantém utils "puro"; é o service que decide lançar a exceção)
* Gerar hash de senha com bcrypt
* Verificar senha contra hash

### totp_utils.py

* Gerar secret TOTP para o usuário
* Gerar URI para QR code
* Validar código TOTP informado pelo usuário

Sem acesso ao banco.

## Política de senha

```text
- Entre 8 e 14 caracteres
- Pelo menos 1 letra maiúscula
- Pelo menos 1 número
```

Implementada em `is_valid_password(password)` no `auth_utils.py`. Retorna a mensagem da primeira regra violada, ou `None` se a senha for válida. Reaproveitada tanto em `register_user()` (auth_service) quanto em `update_password_service()` (user_service), evitando duplicação de regra.

---

## exceptions.py

Define `BusinessError(Exception)` — usada em todo o `service/` para sinalizar violação de regra de negócio (ex: email já existe, senha incorreta, código 2FA inválido).

Separação de tipos de erro no projeto:

```text
BusinessError → erro esperado de regra de negócio → vira HTTP 400 na route
RuntimeError  → erro técnico inesperado (banco fora do ar, etc) → vira HTTP 500 na route
TypeError     → tipo de dado errado passado para uma função utilitária (ex: None em vez de string)
```

Isso permite que a route diferencie um erro que deve mostrar mensagem amigável ao usuário de um erro que deve ser logado como falha do sistema.

---

# Banco de Dados

```sql
users
(
    id            INTEGER PRIMARY KEY AUTO_INCREMENT,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    avatar        VARCHAR(50)  NOT NULL DEFAULT 'avatar_01',
    totp_secret   VARCHAR(64),
    totp_enabled  BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
)

tasks
(
    id          INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id     INTEGER      NOT NULL,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    status      ENUM('pending', 'done') NOT NULL DEFAULT 'pending',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

---

# Fluxo — Cadastro de Usuário

```text
Receber email e senha
↓
Validar campos (vazios, formato de email)
↓
Verificar se email já existe no banco
↓
Se existir → retornar erro 400
↓
Gerar hash da senha com bcrypt
↓
Salvar usuário no banco
↓
Redirecionar para login
```

---

# Fluxo — Login

```text
Receber email e senha
↓
Validar campos
↓
Buscar usuário pelo email
↓
Se não existir → retornar erro 400
↓
Verificar senha com bcrypt
↓
Se senha errada → retornar erro 400
↓
Verificar se 2FA está ativo
↓
Se 2FA ativo → redirecionar para tela de código TOTP
Se 2FA inativo → criar sessão e redirecionar para dashboard
```

## Decisão de segurança — mensagens genéricas no login

Para evitar **user enumeration** (um atacante descobrir quais emails existem no sistema por diferença de mensagem de erro), o login usa a **mesma mensagem genérica** tanto para "email não encontrado" quanto para "senha incorreta": `"Email ou senha inválido"`.

No **cadastro**, foi decidido manter a mensagem específica `"email já existente"` — decisão consciente que prioriza clareza de UX sobre a mitigação total de enumeração, já que o projeto não tem rate limiting/CAPTCHA no escopo atual (ver Melhorias Futuras).

`login_user()` retorna o **usuário completo** (dicionário) em vez de um booleano, para que a route tenha acesso a `user['id']` (criar sessão) e `user['totp_enabled']` (decidir se pede 2FA) sem precisar consultar o banco de novo.

---

# Fluxo — Verificação 2FA

```text
Receber código TOTP de 6 dígitos
↓
Validar código com pyotp
↓
Se inválido → retornar erro
↓
Se válido → criar sessão e redirecionar para dashboard
```

---

# Fluxo — Ativação do 2FA

```text
Usuário acessa aba de perfil
↓
Clica em "Ativar 2FA"
↓
Servidor gera totp_secret e salva no usuário
↓
Servidor gera QR code com a URI do secret
↓
Usuário escaneia com o app autenticador
↓
Usuário digita o primeiro código para confirmar
↓
Servidor valida o código
↓
Se válido → totp_enabled = TRUE
```

## Implementação em duas funções separadas

Este fluxo foi dividido em duas funções distintas no `auth_service.py`, porque são dois momentos diferentes no tempo (o usuário pode escanear o QR code e nunca voltar para confirmar):

```text
start_totp_setup(user_id)
  → busca o usuário, gera secret, salva no banco (totp_enabled continua FALSE)
  → retorna a URI do QR code

confirm_totp_setup(user_id, code)
  → busca o usuário, valida o código contra o secret salvo
  → se válido, chama enable_totp() (totp_enabled = TRUE)
```

Existe ainda uma terceira função, usada durante o **login** (não durante a ativação):

```text
verify_totp_login(user_id, code)
  → estrutura quase idêntica à confirm_totp_setup(), mas NÃO chama enable_totp()
  → o 2FA já está ativo nesse ponto; só valida o código para permitir a criação da sessão
```

Essas duas últimas funções têm lógica parecida mas foram mantidas separadas de propósito — representam intenções diferentes (confirmar configuração vs. autenticar login), seguindo o princípio de responsabilidade única. Pequena duplicação aceita conscientemente em vez de forçar reuso prematuro.

---

# Fluxo — Criação de Tarefa

```text
Receber título e descrição
↓
Validar campos (título obrigatório)
↓
Salvar no banco com user_id da sessão e status 'pending'
↓
Redirecionar para lista de tarefas
```

## Decisão de UX — criação via caixa única

O banco continua com `title` (obrigatório) e `description` (opcional) — isso não muda. Mas a **tela de criação** vai usar uma caixa única de texto (estilo Google Keep / Apple Reminders): o usuário digita e aperta Enter, e esse texto vira o `title` da tarefa automaticamente. A `description` fica escondida por padrão e só é preenchida se o usuário clicar para expandir a tarefa depois de criada (editar). Essa é uma decisão de frontend/template — o service e o repository continuam recebendo `title` e `description` normalmente, sem alteração de assinatura.

---

# Fluxo — Filtro de Tarefas

```text
Receber parâmetro de filtro (pending | done | all)
↓
Buscar tarefas do user_id da sessão com o filtro
↓
Retornar lista filtrada para o template
```

## Implementação — filtro feito no SQL, não em Python

O filtro é aplicado diretamente na query SQL (não busca tudo e filtra depois em Python), por eficiência — evita trazer dados desnecessários do banco:

```sql
SELECT title, description, status FROM tasks
WHERE user_id = %s AND (%s = 'all' OR status = %s)
```

O valor do filtro é passado duas vezes como parâmetro (uma para comparar com `'all'`, outra para comparar com a coluna `status`). Quando o filtro é `'all'`, a condição `%s = 'all'` já resolve o `OR` como verdadeiro, então todas as tarefas do usuário são retornadas independente do status.

No `task_service.py`, `list_tasks()` valida que o filtro recebido é um dos três valores permitidos (`'all'`, `'pending'`, `'done'`) usando um `set` antes de consultar o banco.

## Decisão de segurança — proteção contra IDOR

`update_task_repository()` e `delete_task_repository()` exigem **tanto `id` quanto `user_id`** no `WHERE` da query SQL (`WHERE id = %s AND user_id = %s`). Isso impede que um usuário autenticado edite ou apague uma tarefa pertencente a outro usuário, mesmo manipulando o `task_id` diretamente na URL/requisição (ataque conhecido como IDOR — Insecure Direct Object Reference).

---

# Fluxo — Marcar Tarefa como Concluída

```text
Receber user_id, task_id, status ('pending' ou 'done')
↓
Validar que status é um dos dois valores permitidos
↓
Atualizar apenas a coluna status no banco (title/description não são tocados)
```

Lacuna encontrada durante testes manuais: `update_task()` original só altera `title`/`description`, nunca `status` — mas marcar uma tarefa como concluída é uma ação isolada (clique de checkbox), diferente de editar o conteúdo da tarefa. Por isso, função separada:

```text
update_status_repository(connection, task_id, user_id, status)  → repository, protegido contra IDOR
update_task_status(user_id, task_id, status)                     → service, valida status contra {'pending', 'done'}
```

Confirmado em teste manual que `updated_at` é atualizado automaticamente pelo MySQL ao marcar como concluída — validando a decisão tomada no início do projeto de incluir essa coluna.

---

# Fluxo — Troca de Avatar

```text
Usuário escolhe um avatar de uma lista pré-definida
↓
Validar que o avatar escolhido está entre os permitidos
↓
Salvar no banco
```

Lista de avatares válidos definida como constante `VALID_AVATARS` no `user_service.py`, alinhada com o padrão de nome usado no banco (`avatar_01`, `avatar_02`, ...). Validação contra lista fechada é defesa em profundidade — mesmo com SQL Injection já impossível via `%s`, evita salvar valores fora do domínio esperado.

---

# Fluxo — Troca de Senha

```text
Receber senha atual e senha nova
↓
Validar que a senha nova não está vazia
↓
Buscar o usuário pelo id da sessão
↓
Verificar se a senha ATUAL confere com o hash salvo
↓
Se não conferir → erro (reautenticação falhou)
↓
Gerar hash da senha nova
↓
Salvar novo hash no banco
```

## Decisão de segurança — exigir senha atual

Trocar de senha exige que o usuário informe a **senha atual**, além da nova — mesmo já estando logado. Isso evita que alguém com acesso físico/temporário à sessão ativa (navegador destravado, sessão sequestrada) consiga sequestrar a conta trocando a senha sem saber a original. Alternativa mais robusta (confirmação por email) ficou fora do escopo por exigir infraestrutura de envio de email não prevista no projeto.

---

# Proteção de Rotas

Todas as rotas internas (dashboard, tarefas, perfil) serão protegidas com um decorator `login_required`.

```text
Requisição chega na rota
↓
Decorator verifica session['user_id']
↓
Se não existir → redirecionar para login
Se existir → executar a rota normalmente
```

---

# Tratamento de Erros

```text
400 → entrada inválida (campos vazios, email já existe, senha errada)
401 → não autenticado (sessão ausente ou expirada)
403 → acesso negado
404 → recurso não encontrado
500 → erro interno do servidor
```

---

# Possíveis Melhorias Futuras

* Upload de imagem de perfil pelo usuário
* Data limite nas tarefas
* Prioridade nas tarefas (baixa, média, alta)
* Categorias ou listas de tarefas
* Soft delete (lixeira de tarefas)
* Histórico de atividades
* Contagem de tarefas concluídas
* Cache
* Analytics
* Alteração de username
* Gamificação de XP
* Validação de email mais robusta com a lib `email-validator` (checagem de domínio/MX), em vez da regex simples atual
* Rate limiting e/ou CAPTCHA no cadastro e login, para mitigar tentativas de força bruta e reduzir o risco de user enumeration via mensagem "email já existente" no cadastro

---

# Próximos Passos — Após routes/ e templates/

## Testes automatizados (pytest)

Depois que a aplicação estiver completa (routes + templates funcionando), reescrever os cenários já validados manualmente em `manual_test.py` como testes formais com `pytest` — ex: `pytest.raises(BusinessError)` para os casos de erro. Objetivo: cobertura de testes automatizada como diferencial de portfólio, não só "funciona na mão".

## Hospedagem — PythonAnywhere

Escolhido por já incluir banco MySQL gratuito no plano free (evita migrar de MySQL para Postgres, que é o que aconteceria em Render/Railway). Checklist para quando chegar nessa etapa:

```text
- debug=False em produção (nunca True — vaza informação sensível em erros)
- SECRET_KEY forte já gerada (feito, ver .env)
- Variáveis de ambiente configuradas na plataforma (não só no .env local)
- Arquivo de entrada compatível com WSGI (exigido pelo PythonAnywhere)
```

Nenhum desses pontos exige mudar a estrutura das routes — são ajustes de configuração no fim do projeto.

---

# Filosofia do Projeto

Não adicionar funcionalidade sem requisito.

Prioridade:

```text
terminar
>
deixar preparado para tudo
```

Objetivo principal:

```text
mostrar arquitetura limpa
+
mostrar separação de responsabilidades
+
mostrar entendimento de autenticação
+
mostrar organização de código
+
mostrar segurança básica (hash, 2FA, proteção de rotas)
```

---

Esse documento representa o estado atual do projeto e deve ser usado como contexto para continuar a implementação.
