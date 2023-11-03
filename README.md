# TJPI Web Scraper

## Descrição
Este projeto é um web scraper que extrai informações de processos judiciais do Tribunal de Justiça do Piauí (TJPI) a partir do site de consulta pública.

## Funcionalidades
- Captura cookies da sessão para autenticação em cada requisição.
- Realiza consultas de processos judiciais com base no número do processo.
- Extrai informações, como partes envolvidas e últimas movimentações, dos resultados da consulta.
- Permite o envio das informações extraídas para outra rota via POST.

## Pré-requisitos
- Python 3.6 ou superior
- Bibliotecas Python: Flask, lxml, requests

## Instalação
1. Clone este repositório para o seu ambiente local.
2. Instale as dependências do Python executando `pip install -r requirements.txt`.

## Como Usar
- Execute o arquivo `app.py` para iniciar o servidor Flask.
- Use uma ferramenta como o Postman para fazer requisições POST para as rotas `/api/v1/find-process/`, `/api/v1/send-info/`, e `/api/v1/receive-info/`.
- Siga a ordem das rotas para extrair, enviar e receber informações dos processos judiciais.

## Exemplos
- Consulte os exemplos no código-fonte para entender como usar as rotas.

## Contribuição
- Sinta-se à vontade para contribuir com melhorias, correções de bugs e adições de recursos.
- Abra um problema (issue) ou envie um pedido de pull (pull request) com suas contribuições.

## Licença
Este projeto é distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para obter mais informações.

## Contato
- Para perguntas ou mais informações, entre em contato com [seu nome] em [seu email].

## Créditos
- Este projeto utiliza as bibliotecas Flask, lxml e requests para web scraping e API de servidor web.

## Status do Projeto
- Este projeto está atualmente em desenvolvimento.

## Screenshots
- [Adicione capturas de tela aqui, se aplicável.]

## Links Úteis
- [Adicione links para documentação, site ou blog, se aplicável.]

## Agradecimentos
- Agradecemos à comunidade de código aberto e aos desenvolvedores das bibliotecas que tornaram este projeto possível.

