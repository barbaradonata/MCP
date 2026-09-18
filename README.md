# Google Apps Script MCP Server

Este é um servidor MCP (Model Context Protocol) escrito em Python que permite o gerenciamento de projetos do Google Apps Script. 

Ele expõe ferramentas para criar projetos, manipular arquivos (incluindo `appsscript.json`), gerenciar versões e deployments, alterar permissões, executar funções (via API Executable) e consultar logs.

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.10+
- Um projeto no [Google Cloud Console](https://console.cloud.google.com/)
- As APIs abaixo devem estar ativadas no seu projeto do Google Cloud:
  - **Google Apps Script API**
  - **Google Drive API**
  - **Cloud Logging API** (Opcional, para logs)

### 2. Autenticação (OAuth 2.0 Desktop)
Devido às restrições severas de Service Accounts com a API do Apps Script, este servidor usa Autenticação OAuth de Usuário.
1. No Cloud Console, vá em `APIs & Services > Credentials`.
2. Clique em `Create Credentials > OAuth client ID`.
3. Escolha `Desktop app` como tipo de aplicação.
4. Baixe o JSON gerado e renomeie para `credentials.json`.
5. Coloque o arquivo `credentials.json` na raiz deste projeto.

### 3. Instalar Dependências
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Copie o arquivo de exemplo e configure:
```bash
cp .env.example .env
```
Se desejar consultar logs, defina o `GOOGLE_CLOUD_PROJECT_ID` no `.env`.

### 5. Execução (Standalone para teste de autenticação)
Antes de rodar pela MCP, é bom rodar uma vez manualmente para autorizar a aplicação (isso abrirá o navegador e gerará o `token.json`):
```bash
python appsscript_mcp/server.py
```
> O FastMCP usará `stdio` por padrão, então ele ficará esperando comandos. Se o `token.json` não existir, ao usar a primeira tool ele abrirá o navegador. Para forçar, você pode adicionar um script temporário que chame a autenticação.

### 6. Executando via Cliente MCP (Exemplo Claude Desktop)
Adicione o servidor no seu arquivo de configuração do cliente MCP (ex: `claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "google-apps-script": {
      "command": "C:/caminho/para/venv/Scripts/python.exe",
      "args": ["C:/caminho/para/projeto/appsscript_mcp/server.py"]
    }
  }
}
```

## 🛠 Ferramentas (Tools) Disponíveis

- `create_project`: Cria um novo projeto standalone.
- `list_projects`: Lista projetos Apps Script do seu Google Drive.
- `get_project_info`: Obtém metadados do projeto.
- `get_project_files`: Lista arquivos (`.gs`, `.html`, `appsscript.json`).
- `update_project_files`: Atualiza ou substitui todos os arquivos do projeto.
- `run_script_function`: Executa função remotamente (requer deploy API Executable).
- `create_version`: Congela a versão atual do código.
- `list_deployments`: Lista Web Apps / API Deployments.
- `create_deployment`: Cria um novo deploy a partir de uma versão.
- `manage_permissions`: Compartilha o projeto com outros usuários.
- `get_logs`: Lê os logs usando o GCP Cloud Logging.

## 🏗 Arquitetura
O projeto usa:
- `FastMCP`: Servidor leve e tipado do protocolo MCP.
- `Google API Python Client`: Integração oficial.
- `Pydantic`: Validação estrita de esquemas para arquivos e projetos.
- `OAuth Flow`: Fluxo local para aquisição de Refresh Tokens.
