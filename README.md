# IA claude

Prova de conceito (POC) que envia uma pergunta à API da Anthropic usando o modelo Claude e imprime a resposta completa em JSON.

## O que o código faz

O arquivo `main.py` é um script simples que demonstra uma chamada à API de mensagens da Anthropic:

1. **Carrega variáveis de ambiente** — usa `python-dotenv` para ler a chave de API do arquivo `.env`.
2. **Inicializa o cliente** — cria uma instância de `Anthropic()`, que usa automaticamente a variável `ANTHROPIC_API_KEY`.
3. **Define o modelo** — utiliza `claude-sonnet-4-6`.
4. **Configura o system prompt** — instrui o Claude a ser um assistente útil que responde de forma breve.
5. **Envia uma mensagem** — faz uma pergunta de exemplo: _"What is the main difference between cats and dogs as pets"_.
6. **Imprime a resposta** — exibe o objeto de resposta completo da API em JSON formatado.

## Pré-requisitos

- Python **3.12.6** ou superior
- [uv](https://docs.astral.sh/uv/) (recomendado) ou `pip`
- [GnuPG](https://gnupg.org/) (`gpg`) para criptografar o `.env`
- Uma chave de API da Anthropic ([console.anthropic.com](https://console.anthropic.com/))

## Configuração

1. Clone o repositório e entre na pasta do projeto:

```bash
git clone <url-do-repositorio>
cd ai_claude
```

2. Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

3. Edite o `.env` e substitua o placeholder pela sua chave:

```
ANTHROPIC_API_KEY=sua-chave-aqui
```

4. Instale as dependências:

**Com uv (recomendado):**

```bash
uv sync
```

**Com pip:**

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -e .
```

## Criptografar o `.env`

O `.env` fica fora do Git (segredos locais). Para compartilhar as variáveis de ambiente com a equipe, use o arquivo criptografado `env.data` (AES256 via GPG).

**Descriptografar** (ao clonar o repositório ou receber um `env.data` atualizado):

```bash
uv run task env:decrypt
```

Isso gera o `.env` a partir de `env.data`. O GPG pede a passphrase definida na criptografia.

**Criptografar** (depois de editar o `.env`):

```bash
uv run task env:encrypt
```

Isso sobrescreve `env.data` com o conteúdo atual do `.env`. Use a mesma passphrase da equipe para que todos consigam descriptografar.

## Como rodar

**Com uv:**

```bash
uv run python main.py
```

**Com o ambiente virtual ativado:**

```bash
python main.py
```

A saída será o JSON completo retornado pela API, incluindo metadados como `id`, `model`, `usage` (tokens consumidos) e o conteúdo da resposta em `content`.

## Dependências

| Pacote          | Uso                                         |
| --------------- | ------------------------------------------- |
| `anthropic`     | SDK oficial da API Anthropic                |
| `python-dotenv` | Carregamento de variáveis do arquivo `.env` |
| `taskipy`       | Tarefas do projeto (`env:encrypt`, `env:decrypt`) |

## Personalização

Para testar outra pergunta, edite o campo `content` em `messages` no `main.py`. Para alterar o comportamento do assistente, modifique o `system_prompt` ou o `model`.
