from flask import Flask, request, jsonify
import logging
import json
from lxml import html
import requests
app = Flask(__name__)


logging.basicConfig(filename='app.log', level=logging.INFO)

jsessionid = None
oauth_token_request_state = None
awsalbapp = None

# basicamente essa função captura os cookies da sessão e os retorna na função de baixo "find_process_tj"
#tentei fazer com que ele não precisasse criar um novo hash toda vez que fizesse uma requisição nova, ele pudesse aproveitar 
# o tempo de sessão atual. Apenas um capricho :) então em teoria ele só vai criar esses ids se não existir
def get_session_cookies_and_headers():
    global jsessionid, oauth_token_request_state, awsalbapp
    if not jsessionid or not oauth_token_request_state or not awsalbapp:
        response = requests.get('https://tjpi.pje.jus.br/1g/ConsultaPublica/listView.seam')
        if response.status_code == 200:
            logging.info("Capturando cookies da sessão")
            cookies = response.cookies
            jsessionid = cookies.get('JSESSIONID')
            oauth_token_request_state = cookies.get('OAuth_Token_Request_State')
            awsalbapp = cookies.get('AWSALBAPP-0')
        else:
            return None, None, None  
    return jsessionid, oauth_token_request_state, awsalbapp




#Aqui é a rota e a função onde capturamos o que está vindo do POSTMAN via json e o retorno da função acima(no caso os cookies, os headers nao precisou)
# a rota aceita os dados vindo da requisição como string mesmo
# basicamente isso aqui vai na rota e faz a busca por numero do processo e retorna a sucesso se todos os requisitos estiverem cumpridos
#basicamente essa rota peguei por cURL
@app.route("/api/v1/find-process/", methods=["POST"])
def find_process_tj():

    try:
        request_data = request.get_json()

        if not request_data:
            return {
                "error": "Nenhum dado JSON encontrado no corpo da solicitação."
            }, 400

        nome_parte = request_data.get("nomeParte")
        numero_processo = request_data.get("numeroProcesso")

        if not numero_processo:
            return {
                "error": "O campo 'numeroProcesso' é obrigatório."
            }, 400

        jsessionid, oauth_token_request_state, awsalbapp = get_session_cookies_and_headers()

        if jsessionid is None:
            return {
                "error": "Não foi possível obter os cookies de sessão."
            }, 500
        

        if awsalbapp is None:
            return {
                "error": "Não foi possível obter os cookies de sessão."
            }, 500
        

        cookies = {
        'MO': 'P',
        'JSESSIONID': jsessionid,
        'AWSALBAPP-1': '_remove_',
        'AWSALBAPP-2': '_remove_',
        'AWSALBAPP-3': '_remove_',
        'OAuth_Token_Request_State': oauth_token_request_state,
        'AWSALBAPP-0': awsalbapp
        
        }

        headers = {
        'authority': 'tjpi.pje.jus.br',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.5',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': 'MO=P; JSESSIONID=Ue8gSwQPQbaEcMx0N3g-L5_rs5b1Cqjk3nRwyEjX.pje-legacy-5dd9f85df9-469k6; AWSALBAPP-1=_remove_; AWSALBAPP-2=_remove_; AWSALBAPP-3=_remove_; OAuth_Token_Request_State=1c7f08a1-faf9-488d-9317-0ded07ad0a8a; AWSALBAPP-0=AAAAAAAAAACFchNmwUkTNF4dnZ9BrC/0OKd+LG9YKK+PqRsERQIWDfx6TocLHQf4Oun4aPLlIVglUHrHd4AI7mhHl+P63wJfOdpczDgmOJLotSeHYjg/EHidoriz4tWqlQfGYqhFj3c5S/Y=',
        'origin': 'https://tjpi.pje.jus.br',
        'referer': 'https://tjpi.pje.jus.br/1g/ConsultaPublica/listView.seam',
        'sec-ch-ua': '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

        data = f'AJAXREQUEST=_viewRoot&fPP%3AnumProcesso-inputNumeroProcessoDecoration%3AnumProcesso-inputNumeroProcesso={numero_processo}&mascaraProcessoReferenciaRadio=on&fPP%3Aj_id147%3AprocessoReferenciaInput=&fPP%3Adnp%3AnomeParte=&fPP%3Aj_id165%3AnomeAdv=&fPP%3Aj_id174%3AclasseProcessualProcessoHidden=&fPP%3ADecoration%3AnumeroOAB=&fPP%3ADecoration%3Aj_id200=&fPP%3ADecoration%3AestadoComboOAB=org.jboss.seam.ui.NoSelectionConverter.noSelectionValue&fPP=fPP&autoScroll=&javax.faces.ViewState=j_id1&fPP%3Aj_id206=fPP%3Aj_id206&AJAX%3AEVENTS_COUNT=1&'

        logging.info("Realizando consulta")
        response = requests.post('https://tjpi.pje.jus.br/1g/ConsultaPublica/listView.seam', cookies=cookies, headers=headers, data=data)
        
        process_info = {}

        #aqui basicamente eu só faço a captura do conteudo se o status da rota for menor ou igual a 300
        #status acima disso se configuram em error http
        if response.status_code <= 300:
            response_data = response.text

            #aqui eu faço a leitura do código HTML gerado no retorno da rota eu poderia ter utilizado o beatifulsoup para manipular os dados
            # da resposta HTML.
            tree = html.fromstring(response_data)
            logging.info("Consulta realizada com sucesso!!")
            td_elements = tree.xpath('//table[@id="fPP:processosTable"]/tbody/tr/td')
            
            if len(td_elements) >= 3:
                process_info["partes envolvidas"] = td_elements[1].text_content()
                process_info["ultimas movimentações"] = td_elements[2].text_content()

        if response.status_code > 300:
            # Tratamento de erro para códigos de status HTTP diferentes de sucesso
            logging.warning("Recebido código de status HTTP inesperado: %d", response.status_code)
            return {
                "error": response.status_code
            }
        
        if not process_info:
            # Tratamento de erro para número de processo inválido ou campo não preenchido
            logging.error("Número de processo inválido ou campo não preenchido.")
            return {
                "error": "Número de processo inválido ou campo não preenchido."
            }, 400
        
        with open('dados_extraidos.txt', 'w') as file:
            file.write(json.dumps(process_info))
            
        return jsonify({
            "Sucess": "Informações Enviadas com Sucesso para `dados_extraidos.txt`"
        })
    
    except requests.exceptions.RequestException as e:
        # Tratamento de erro para problemas na requisição HTTP
        logging.error("Erro na requisição HTTP: %s", str(e))
        return {
            "error": "Erro na requisição HTTP.",
            "detail": str(e)
        }, 500 

    except Exception as e:
        # Tratamento de erro genérico para exceções inesperadas
        logging.error("Erro inesperado: %s", str(e))
        return {
            "error": "Erro inesperado.",
            "detail": str(e)
        }, 500






@app.route("/api/v1/send-info", methods=["POST"])
def send_info():
    try:
        # Ler as informações do arquivo
        with open('dados_extraidos.txt', 'r') as file:
            saved_data = json.loads(file.read())
            logging.info("Enviando Informações extraídas para http://127.0.0.1:5000/api/v1/receive-info")

        # Enviar as informações para a nova rota via POST
        response = requests.post('http://127.0.0.1:5000/api/v1/receive-info', json=saved_data)
        if response.status_code == 200:
            logging.info("Informações recebidas com sucesso http://127.0.0.1:5000/api/v1/receive-info")
            return {
                "result": response.json()
            }
        else:
            logging.error("Erro ao enviar informações para a nova rota")
            return {
                "error": "Erro ao enviar informações para a nova rota."
            }, 500
    except Exception as e:
        return {
            "error": "Erro inesperado.",
            "detail": str(e)
        }, 500




@app.route("/api/v1/receive-info", methods=["POST"])
def receive_info():
    try:
        # pode acessar os dados recebidos do POST
        received_data = request.get_json()
        logging.info("sucess")
        # Faz o processamento necessário com os dados recebidos
        return  received_data
        
    except Exception as e:
        logging.error("Erro ao processar informações recebidas")
        return {
            "error": "Erro ao processar informações recebidas.",
            "detail": str(e)
        }, 500

