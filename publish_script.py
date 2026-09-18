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
    
    # We want to keep appsscript.json
    # We will replace Code.gs with our own, or just add DespesasViagem.gs
    new_files = []
    
    for f in files:
        if f["name"] == "appsscript":
            # Ensure it has web app config if needed, but standard is fine
            new_files.append(File(name=f["name"], type=f["type"], source=f["source"]))
            
    code_source = """
function doPost(e) {
  try {
    // Tenta ler os dados enviados na requisição POST
    var data = JSON.parse(e.postData.contents);
    
    // Aqui você poderia salvar na planilha. Exemplo:
    // var plan = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    // plan.appendRow([new Date(), data.funcionario, data.valor, data.descricao]);
    
    // Por enquanto, apenas retornamos sucesso para quem enviou
    return ContentService.createTextOutput(JSON.stringify({
      status: "sucesso",
      mensagem: "Despesa de viagem de " + (data.funcionario || "Desconhecido") + " recebida com sucesso!",
      dadosRecebidos: data
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (erro) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "erro",
      mensagem: erro.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput("A API de Despesas de Viagem está online e pronta para receber requisições POST!");
}
"""
    
    new_files.append(File(name="DespesasViagem", type="SERVER_JS", source=code_source.strip()))
    
    print("Publishing updated files...")
    project_files = ProjectFiles(files=new_files)
    result = service.update_project_files(script_id, project_files)
    
    print("Successfully updated the script!")

if __name__ == "__main__":
    main()
