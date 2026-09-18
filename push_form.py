import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from appsscript_mcp.services.apps_script import AppsScriptService
from appsscript_mcp.schemas.file import ProjectFiles, File

def main():
    service = AppsScriptService()
    script_id = "1YeN-8z_E-9a0iKrIZ9G1qqLdDiM9OcjFo-t6ujVPV0BGvS6oKhq0tKRs"
    
    print("Fetching current files...")
    current_content = service.get_project_files(script_id)
    files = current_content.get("files", [])
    
    new_files = []
    
    # Keep appsscript.json
    for f in files:
        if f["name"] == "appsscript":
            new_files.append(File(name=f["name"], type=f["type"], source=f["source"]))
            
    code_gs = """
function doGet(e) {
  // Retorna a interface gráfica (HTML)
  return HtmlService.createHtmlOutputFromFile('Index')
      .setTitle('Registro de Despesas')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function processExpense(data) {
  try {
    var userEmail = Session.getActiveUser().getEmail();
    if (!userEmail) {
      // Fallback in case user is not logged in / running as developer
      userEmail = "xicarapaulapires@gmail.com"; 
    }
    
    var subject = "Nova Despesa de Viagem Registrada - " + data.nome;
    var body = "Você recebeu um novo registro de despesa:\\n\\n" +
               "Funcionário: " + data.nome + "\\n" +
               "Data da Despesa: " + data.data + "\\n" +
               "Descrição: " + data.descricao + "\\n" +
               "Valor: R$ " + data.valor + "\\n\\n" +
               "Enviado pelo sistema automatizado.";
               
    MailApp.sendEmail(userEmail, subject, body);
    
    return { success: true, message: "Despesa registrada e enviada por email com sucesso!" };
  } catch (e) {
    return { success: false, message: e.toString() };
  }
}
"""

    index_html = """
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --primary: #6366f1;
        --primary-hover: #4f46e5;
        --bg: #0f172a;
        --surface: rgba(30, 41, 59, 0.7);
        --text: #f8fafc;
        --text-muted: #94a3b8;
        --border: rgba(255, 255, 255, 0.1);
      }
      
      body {
        margin: 0;
        padding: 0;
        font-family: 'Inter', sans-serif;
        background: var(--bg);
        background-image: 
          radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
          radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .container {
        width: 100%;
        max-width: 480px;
        padding: 2rem;
      }

      .glass-card {
        background: var(--surface);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
      }

      @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
      }

      h1 {
        margin: 0 0 0.5rem 0;
        font-size: 1.75rem;
        font-weight: 700;
        background: linear-gradient(to right, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }

      p.subtitle {
        margin: 0 0 2rem 0;
        color: var(--text-muted);
        font-size: 0.95rem;
      }

      .form-group {
        margin-bottom: 1.5rem;
      }

      label {
        display: block;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        color: #cbd5e1;
      }

      input, textarea {
        width: 100%;
        box-sizing: border-box;
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: var(--text);
        font-family: inherit;
        font-size: 1rem;
        transition: all 0.2s ease;
      }

      input:focus, textarea:focus {
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
      }
      
      textarea {
        resize: vertical;
        min-height: 80px;
      }

      button {
        width: 100%;
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 1rem;
      }

      button:hover {
        background: var(--primary-hover);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);
      }
      
      button:active {
        transform: translateY(0);
      }

      .status {
        margin-top: 1.5rem;
        padding: 1rem;
        border-radius: 12px;
        font-size: 0.9rem;
        display: none;
        text-align: center;
        animation: fadeIn 0.3s ease;
      }

      .status.success {
        display: block;
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.2);
      }

      .status.error {
        display: block;
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.2);
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      
      /* Micro-interactions */
      input:hover, textarea:hover {
        border-color: rgba(255,255,255,0.3);
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="glass-card">
        <h1>Despesas de Viagem</h1>
        <p class="subtitle">Registre seus gastos e receba por e-mail.</p>
        
        <form id="expenseForm">
          <div class="form-group">
            <label for="nome">Nome do Funcionário</label>
            <input type="text" id="nome" name="nome" required placeholder="Ex: Maria Silva">
          </div>
          
          <div class="form-group">
            <label for="data">Data da Despesa</label>
            <input type="date" id="data" name="data" required>
          </div>
          
          <div class="form-group">
            <label for="descricao">Descrição do Gasto</label>
            <input type="text" id="descricao" name="descricao" required placeholder="Ex: Táxi para o aeroporto">
          </div>
          
          <div class="form-group">
            <label for="valor">Valor (R$)</label>
            <input type="number" id="valor" name="valor" step="0.01" required placeholder="0.00">
          </div>
          
          <button type="submit" id="submitBtn">Enviar Despesa</button>
        </form>
        
        <div id="statusMsg" class="status"></div>
      </div>
    </div>

    <script>
      document.getElementById('expenseForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        var btn = document.getElementById('submitBtn');
        var statusMsg = document.getElementById('statusMsg');
        
        btn.innerText = 'Enviando...';
        btn.disabled = true;
        statusMsg.className = 'status';
        
        var data = {
          nome: document.getElementById('nome').value,
          data: document.getElementById('data').value,
          descricao: document.getElementById('descricao').value,
          valor: document.getElementById('valor').value
        };
        
        google.script.run
          .withSuccessHandler(function(response) {
            btn.innerText = 'Enviar Despesa';
            btn.disabled = false;
            
            if(response.success) {
              statusMsg.innerText = response.message;
              statusMsg.className = 'status success';
              document.getElementById('expenseForm').reset();
            } else {
              statusMsg.innerText = 'Erro: ' + response.message;
              statusMsg.className = 'status error';
            }
          })
          .withFailureHandler(function(error) {
            btn.innerText = 'Enviar Despesa';
            btn.disabled = false;
            statusMsg.innerText = 'Erro na conexão: ' + error.message;
            statusMsg.className = 'status error';
          })
          .processExpense(data);
      });
    </script>
  </body>
</html>
"""

    new_files.append(File(name="Code", type="SERVER_JS", source=code_gs.strip()))
    new_files.append(File(name="Index", type="HTML", source=index_html.strip()))
    
    print("Publishing updated files...")
    project_files = ProjectFiles(files=new_files)
    result = service.update_project_files(script_id, project_files)
    
    print("Successfully updated the script with UI and Email!")

if __name__ == "__main__":
    main()
