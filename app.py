import requests   
import csv

# Passo 1: Fazer a requisição para a API
def rodadas(url):
    response = requests.get(url)

    # Verifique se a requisição foi bem-sucedida
    if response.status_code == 200:
        dados_json = response.json()  # Converte o conteúdo da resposta para JSON
        return dados_json
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None  # Retorna None em caso de erro

# Inicializando uma lista para armazenar os dados das partidas
partidas_info = []

for rodada in range(1, 36):  # Rodadas de 1 a 38
    url = f'https://api.cartola.globo.com/partidas/{rodada}'
    dados_json = rodadas(url)  # Obtendo os dados da rodada

    # Se não houver dados, ignora essa rodada
    if dados_json is None:
        continue

    # Loop para pegar os dados de cada partida
    for partida_data in dados_json['partidas']:
        partida = {
            'date': partida_data['partida_data'][:10],  # Pegando só a data (primeiros 10 caracteres)
            'home_team': partida_data['clube_casa_id'],
            'away_team': partida_data['clube_visitante_id'],        
            'home_score': partida_data['placar_oficial_mandante'],        
            'away_score': partida_data['placar_oficial_visitante'],
            'round': dados_json['rodada']
        }

        # Adicionando as informações da partida na lista
        partidas_info.append(partida)

# Exibindo a lista de partidas
'''for partida in partidas_info:
    print(partida)'''


nome_arquivo = 'partidas.csv'

# Abrindo o arquivo CSV para escrita
with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
    # Criando o writer para escrever no arquivo CSV
    writer = csv.DictWriter(arquivo_csv, fieldnames=partidas_info[0].keys())
    
    # Escrevendo o cabeçalho (nomes das colunas)
    writer.writeheader()
    
    # Escrevendo os dados
    writer.writerows(partidas_info)

print(f"Dados salvos no arquivo {nome_arquivo}")
