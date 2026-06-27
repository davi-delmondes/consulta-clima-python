# ==================================================
# Consulta de Clima com WeatherAPI
# Autor: Davi de Carvalho Delmondes
# ==================================================
# Programa de terminal para consultar o clima atual
# de uma cidade usando a API da WeatherAPI.
#
# Observação:
# A chave da API é carregada a partir de um arquivo .env.
# O arquivo .env não deve ser enviado para o GitHub.
# ==================================================

import os

import requests
from dotenv import load_dotenv


# =========================
# Configurações gerais
# =========================

# Carrega as variáveis do arquivo .env.
load_dotenv()

# Dados principais usados na comunicação com a API.
API_KEY = os.getenv("API_KEY")
LINK_API = "https://api.weatherapi.com/v1/current.json"

# Largura usada para centralizar títulos e montar o layout do terminal.
LARGURA_LAYOUT = 44


# =========================
# Mensagens de erro da API
# =========================

# Mensagens traduzidas para os principais erros retornados pela WeatherAPI.
MENSAGENS_ERRO = {
    1002: "Chave da API não informada.",
    1003: "Cidade não informada. Digite uma cidade válida.",
    1005: "URL da API inválida.",
    1006: "Cidade não encontrada. Verifique o nome e tente novamente.",
    2006: "Chave da API inválida.",
    2007: "Limite mensal de consultas excedido.",
    2008: "Chave da API desativada.",
    2009: "Seu plano não permite acessar esse recurso.",
    9000: "JSON inválido em requisição em lote.",
    9001: "Muitas localizações na requisição em lote.",
    9999: "Erro interno da WeatherAPI. Tente novamente mais tarde."
}


# =========================
# Campos esperados da API
# =========================

# Campos obrigatórios dentro do bloco "location".
CAMPOS_LOCATION = ("name", "region", "country", "localtime")

# Campos obrigatórios dentro do bloco "current".
CAMPOS_CURRENT = (
    "temp_c",
    "feelslike_c",
    "humidity",
    "wind_kph",
    "wind_dir",
    "wind_degree",
    "pressure_mb",
    "uv",
    "vis_km",
    "last_updated",
)

# Campos obrigatórios dentro do bloco "condition".
CAMPOS_CONDITION = ("text",)


# =========================
# Funções utilitárias
# =========================

def limpar_tela() -> None:
    # Limpa o terminal no Windows, Linux ou macOS.
    os.system("cls" if os.name == "nt" else "clear")


def pausar_e_limpar() -> None:
    # Aguarda o usuário pressionar ENTER antes de limpar a tela.
    print()
    input("Pressione ENTER para continuar...")
    limpar_tela()


# =========================
# Verificação inicial
# =========================

def verificar_configuracao() -> bool:
    # Verifica se a chave da API foi carregada corretamente.
    if not API_KEY:
        limpar_tela()
        print("=" * LARGURA_LAYOUT)
        print("ERRO DE CONFIGURAÇÃO".center(LARGURA_LAYOUT))
        print("=" * LARGURA_LAYOUT)
        print()
        print("API_KEY não encontrada.")
        print("Crie um arquivo .env na pasta do projeto.")
        print()
        print("Exemplo:")
        print("API_KEY=sua_chave_aqui")
        print()
        input("Pressione ENTER para encerrar...")
        return False
    return True


# =========================
# Consulta na API
# =========================

def buscar_clima(cidade: str) -> tuple[dict | None, int]:
    # Parâmetros enviados para a WeatherAPI.
    params = {
        "key": API_KEY,
        "q": cidade,
        "lang": "pt"
    }

    try:
        # Faz a requisição com timeout para evitar travamentos.
        response = requests.get(LINK_API, params=params, timeout=10)

        try:
            # Tenta converter a resposta da API para JSON.
            data = response.json()

            # Garante que a resposta seja um dicionário válido.
            if not data or not isinstance(data, dict):
                return (None, -1)

        except ValueError:
            # Status -1 representa uma resposta inválida dentro do programa.
            return (None, -1)
    
        status_code = response.status_code

        return (data, status_code)

    except requests.exceptions.RequestException:
        # Status 0 representa erro de conexão dentro do programa.
        return (None, 0)


# =========================
# Fluxo da consulta
# =========================

def consultar_clima() -> None:
    limpar_tela()

    cidade = input("Digite uma cidade: ").strip()

    # Impede consulta vazia.
    if not cidade:
        print("\nDigite uma cidade válida.")
        pausar_e_limpar()
        return

    # Busca os dados da cidade e recebe também o código de status.
    dados, status_code = buscar_clima(cidade)

    if status_code == 200:
        # Exibe o clima somente se os dados necessários estiverem completos.
        if validar_dados_clima(dados):
            mostrar_clima(dados)

        else:
            print("\n[ERRO] A API retornou dados incompletos.")

    elif status_code == -1:
        print("\n[ERRO] A API retornou uma resposta inválida.")

    elif status_code == 0:
        print("\n[ERRO] Não foi possível conectar à API.")

    else:
        mostrar_erro_api(dados)

    pausar_e_limpar()


# =========================
# Validação dos dados
# =========================

def validar_dados_clima(dados: dict | None) -> bool:
    # Garante que os dados existem e estão no formato esperado.
    if not dados:
        return False

    if not isinstance(dados, dict):
        return False

    # Confere se os blocos principais existem na resposta da API.
    if "location" not in dados or "current" not in dados:
        return False
    
    location = dados["location"]

    if not isinstance(location, dict):
        return False

    current = dados["current"]

    if not isinstance(current, dict):
        return False

    # Confere se o bloco de condição climática existe dentro de "current".
    if "condition" not in current:
        return False

    condition = current["condition"]

    if not isinstance(condition, dict):
        return False

    # Valida os campos usados na exibição da localização.
    for campo in CAMPOS_LOCATION:
        if campo not in location:
            return False

    # Valida os campos usados na exibição do clima atual.
    for campo in CAMPOS_CURRENT:
        if campo not in current:
            return False

    # Valida os campos usados na exibição da condição climática.
    for campo in CAMPOS_CONDITION:
        if campo not in condition:
            return False

    return True


# =========================
# Exibição dos dados
# =========================

def mostrar_secao(titulo: str) -> None:
    # Exibe um título centralizado para separar as informações.
    print()
    print("=" * LARGURA_LAYOUT)
    print(titulo.center(LARGURA_LAYOUT))
    print("=" * LARGURA_LAYOUT)


def mostrar_campo(nome: str, valor) -> None:
    # Exibe o nome do campo alinhado com seu valor.
    campo = nome + ":"
    print(f"{campo:<22} {valor}")


def mostrar_clima(data: dict) -> None:
    # Exibe informações de localização.
    mostrar_secao("LOCALIZAÇÃO")
    mostrar_campo("Cidade", data['location']['name'])
    mostrar_campo("Região", data['location']['region'])
    mostrar_campo("País", data['location']['country'])
    mostrar_campo("Horário local", data['location']['localtime'])

    # Exibe informações principais do clima.
    mostrar_secao("CLIMA ATUAL")
    mostrar_campo("Condição", data['current']['condition']['text'])
    mostrar_campo("Temperatura", f"{data['current']['temp_c']}°C")
    mostrar_campo("Sensação térmica", f"{data['current']['feelslike_c']}°C")
    mostrar_campo("Umidade", f"{data['current']['humidity']}%")

    # Exibe informações de vento e ambiente.
    mostrar_secao("VENTO E AMBIENTE")
    mostrar_campo("Vento", f"{data['current']['wind_kph']} km/h")
    mostrar_campo("Direção do vento", data['current']['wind_dir'])
    mostrar_campo("Direção em graus", f"{data['current']['wind_degree']}°")
    mostrar_campo("Pressão atmosférica", f"{data['current']['pressure_mb']} mb")
    mostrar_campo("Índice UV", data['current']['uv'])
    mostrar_campo("Visibilidade", f"{data['current']['vis_km']} km")

    # Exibe a data e hora da última atualização enviada pela API.
    mostrar_secao("DADOS ATUALIZADOS")
    mostrar_campo("Última atualização", data['current']['last_updated'])


# =========================
# Exibição de erros da API
# =========================

def mostrar_erro_api(dados: dict | None) -> None:
    # Garante que a resposta possui um bloco de erro válido.
    if not dados or "error" not in dados:
        print("\n[ERRO] A API retornou um erro inesperado.")
        return

    erro = dados["error"]

    if not isinstance(erro, dict):
        print("\n[ERRO] A API retornou um erro inesperado.")
        return         

    error_code = erro.get("code")
    mensagem_original = erro.get("message", "Erro desconhecido retornado pela API.")

    if not error_code:
        print(f"\n[ERRO] {mensagem_original}")
        return

    # Usa uma mensagem traduzida, ou a mensagem original da API se o código não estiver mapeado.
    mensagem = MENSAGENS_ERRO.get(error_code, mensagem_original)

    print(f"\nErro {error_code}: {mensagem}")


# =========================
# Menu principal
# =========================

def mostrar_menu() -> None:
    # Exibe o menu principal do programa.
    print("╔" + "═" * LARGURA_LAYOUT + "╗")
    print("║" + "CONSULTA DE CLIMA".center(LARGURA_LAYOUT) + "║")
    print("║" + "WeatherAPI - Dados em tempo real".center(LARGURA_LAYOUT) + "║")
    print("╠" + "═" * LARGURA_LAYOUT + "╣")
    print("║" + " [1] Consultar clima".ljust(LARGURA_LAYOUT) + "║")
    print("║" + " [0] Sair".ljust(LARGURA_LAYOUT) + "║")
    print("╚" + "═" * LARGURA_LAYOUT + "╝")


# =========================
# Função principal
# =========================

def main() -> None:
    # Encerra o programa se a configuração inicial estiver incompleta.
    if not verificar_configuracao():
        return

    limpar_tela()

    while True:
        mostrar_menu()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            consultar_clima()

        elif opcao == "0":
            print("\nEncerrando o programa...")
            break

        else:
            print("\nOpção inválida. Escolha 1 ou 0.")
            pausar_e_limpar()
            continue


# Executa o programa somente quando este arquivo for iniciado diretamente.
if __name__ == "__main__":
    main()
