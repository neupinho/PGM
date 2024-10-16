from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

file_path_canada = 'classificacao_final_Canadá.xlsx'
file_path_eua = 'classificacao_final_EUA.xlsx'
file_path_chile = 'classificacao_final_Chile.xlsx'
file_path_geral = 'per_geral_1.xlsx'

df_canada = pd.read_excel(file_path_canada)
df_eua = pd.read_excel(file_path_eua)
df_chile = pd.read_excel(file_path_chile)
df_geral = pd.read_excel(file_path_geral)

print("Colunas do arquivo de classificação geral:", df_geral.columns)

html_template = """
<!doctype html>
<title>Verificação de Classificação por Nota</title>
<h2>Digite seu número de inscrição</h2>
<h4>Feito carinhosamente por João Victor Cosmo - ETEPD</h4>
<form method="post">
  <input type="text" name="inscricao" required>
  <input type="submit" value="Verificar">
</form>
<p>{{ result }}</p>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        inscricao = request.form['inscricao']
        inscricao = int(inscricao)
        if inscricao in df_geral['INSCRIÇÃO'].values:
            nome = df_geral.loc[df_geral['INSCRIÇÃO'] == inscricao, 'NOME'].values[0]
            pais_escolhido = df_geral.loc[df_geral['INSCRIÇÃO'] == inscricao, 'PAÍS'].values[0]
            if pais_escolhido == 'INTERCÂMBIO INTERNACIONAL NOS ESTADOS UNIDOS DA AMÉRICA - INGLÊS':
                df_pais = df_eua
                limite = 301
            elif pais_escolhido == 'INTERCÂMBIO INTERNACIONAL NO CANADÁ - INGLÊS':
                df_pais = df_canada
                limite = 401
            elif pais_escolhido == 'INTERCÂMBIO INTERNACIONAL NO CHILE - ESPANHOL':
                df_pais = df_chile
                limite = 201
            else:
                result = 'País inválido.'
                return render_template_string(html_template, result=result)
            
            if inscricao in df_pais['INSCRIÇÃO'].values:
                classificacao_final = df_pais.loc[df_pais['INSCRIÇÃO'] == inscricao, 'CLASSIFICAÇÃO'].values[0]
                if classificacao_final < limite:
                    result = f'Parabéns, {nome}! Você passou para {pais_escolhido}. Sua classificação final é {classificacao_final}.'
                else:
                    result = f'Infelizmente, {nome}, você não passou. Sua classificação final é {classificacao_final} no país {pais_escolhido}.'
            else:
                result = 'Número de inscrição não encontrado na lista de classificação final do país escolhido.'
        else:
            result = 'Número de inscrição não encontrado na lista de classificação geral.'

    return render_template_string(html_template, result=result)

if __name__ == '__main__':
    app.run(debug=True)
