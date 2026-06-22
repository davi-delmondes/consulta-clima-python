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


# ==================================================
# CONFIGURAÇÕES
# ==================================================

load_dotenv()

API_KEY = os.getenv("API_KEY")
LINK_API = "https://api.weatherapi.com/v1/current.json"
LARGURA_LAYOUT = 44


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


# ==================================================
# FUNÇÕES AUXILIARES
# ==================================================

def limpar_tela() -> None:
    # Limpa o terminal no Windows, Linux ou macOS.
    os.system("cls" if os.name == "nt" else "clear")


def pausar_e_limpar() -> None:
    # Aguarda o usuário pressionar ENTER antes de limpar a tela.
    print()
    input("Pressione ENTER para continuar...")
    limpar_tela()


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


# ==================================================
# CONSULTA NA API
# ==================================================

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

        data = response.json()
        status_code = response.status_code

        return (data, status_code)

    except requests.exceptions.RequestException:
        # Status 0 representa erro de conexão dentro do programa.
        return (None, 0)


def consultar_clima() -> None:
    limpar_tela()

    cidade = input("Digite uma cidade: ").strip()

    # Impede consulta vazia.
    if not cidade:
        print("\nDigite uma cidade válida.")
        pausar_e_limpar()
        return

    dados, status_code = buscar_clima(cidade)

    if status_code == 200:
        mostrar_clima(dados)

    elif status_code == 0:
        print("\nErro ao conectar com a API.")

    else:
        mostrar_erro_api(dados)

    pausar_e_limpar()


# ==================================================
# EXIBIÇÃO DOS DADOS
# ==================================================

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
    mostrar_secao("LOCALIZAÇÃO")
    mostrar_campo("Cidade", data['location']['name'])
    mostrar_campo("Região", data['location']['region'])
    mostrar_campo("País", data['location']['country'])
    mostrar_campo("Horário local", data['location']['localtime'])

    mostrar_secao("CLIMA ATUAL")
    mostrar_campo("Condição", data['current']['condition']['text'])
    mostrar_campo("Temperatura", f"{data['current']['temp_c']}°C")
    mostrar_campo("Sensação térmica", f"{data['current']['feelslike_c']}°C")
    mostrar_campo("Umidade", f"{data['current']['humidity']}%")

    mostrar_secao("VENTO E AMBIENTE")
    mostrar_campo("Vento", f"{data['current']['wind_kph']} km/h")
    mostrar_campo("Direção do vento", data['current']['wind_dir'])
    mostrar_campo("Direção em graus", f"{data['current']['wind_degree']}°")
    mostrar_campo("Pressão atmosférica", f"{data['current']['pressure_mb']} mb")
    mostrar_campo("Índice UV", data['current']['uv'])
    mostrar_campo("Visibilidade", f"{data['current']['vis_km']} km")

    mostrar_secao("DADOS ATUALIZADOS")
    mostrar_campo("Última atualização", data['current']['last_updated'])


def mostrar_erro_api(dados: dict) -> None:
    error_code = dados['error']['code']

    # Usa uma mensagem traduzida, ou a mensagem original da API se o código não estiver mapeado.
    mensagem = MENSAGENS_ERRO.get(error_code, dados['error']['message'])

    print(f"\nErro {error_code}: {mensagem}")


# ==================================================
# MENU PRINCIPAL
# ==================================================

def mostrar_menu() -> None:
    print("╔" + "═" * LARGURA_LAYOUT + "╗")
    print("║" + "CONSULTA DE CLIMA".center(LARGURA_LAYOUT) + "║")
    print("║" + "WeatherAPI - Dados em tempo real".center(LARGURA_LAYOUT) + "║")
    print("╠" + "═" * LARGURA_LAYOUT + "╣")
    print("║" + " [1] Consultar clima".ljust(LARGURA_LAYOUT) + "║")
    print("║" + " [0] Sair".ljust(LARGURA_LAYOUT) + "║")
    print("╚" + "═" * LARGURA_LAYOUT + "╝")


def main() -> None:
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
