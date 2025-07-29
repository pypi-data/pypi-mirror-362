import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Tuple
from bs4 import BeautifulSoup


def extract_tabnews_articles(state: Dict[str, Any], args: Dict[str, Any]) -> Optional[Tuple[str, Any]]:
    """
    Fetches recent news from TabNews, extracts the URLs, 
    titles, and publication dates, and returns them as a list of dictionaries.
    """
    url = "https://www.tabnews.com.br/recentes/rss"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for non-200 status codes
        
        root = ET.fromstring(response.content)
        
        articles_list = []
        
        for item in root.findall('.//item'):
            link = item.find('link').text
            title = item.find('title').text
            pub_date = item.find('pubDate').text
            
            articles_list.append({
                "url": link,
                "title": title,
                "publication_date": pub_date
            })
            
        return ("articles", articles_list)

    except requests.exceptions.RequestException as e:
        return ("articles", f"Failed to fetch news: {e}")

def process_html_content(html_content: bytes) -> Optional[str]:
    """
    Analisa o conteúdo HTML, encontra a tag <main> e o primeiro <div> dentro dela,
    e retorna o texto limpo.

    Args:
        html_content: O conteúdo HTML da página em bytes.

    Returns:
        Uma string com o texto extraído e limpo, ou None se não encontrar.
    """
    if not html_content:
        return None

    # 1. Inicia o BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 2. Encontra a tag <main>
    main_tag = soup.find('main')
    if not main_tag:
        print("Erro: A tag <main> não foi encontrada no HTML.")
        return None

    # 3. Encontra o primeiro <div> dentro da tag <main>
    # O método .find() retorna a primeira ocorrência que encontrar.
    content_div = main_tag.find('div')
    if not content_div:
        print("Erro: Nenhum <div> foi encontrado dentro da tag <main>.")
        return None
        
    # 4. Extrai todo o texto do div e seus filhos
    # O 'separator' ajuda a manter as quebras de linha entre os parágrafos
    text = content_div.get_text(separator='\n', strip=True)
    
    # 5. Limpeza final: remove linhas vazias extras para um resultado mais limpo
    cleaned_text = "\n".join(line for line in text.splitlines() if line.strip())

    return cleaned_text

def load_and_process_url(state: Dict[str, Any], args: Dict[str, Any]) -> Tuple[str, Dict[str, str]]:
    """
    Busca o conteúdo de uma URL do TabNews e extrai o conteúdo principal.
    
    Args:
        state: Estado atual do agente (não utilizado aqui, mas mantido por padrão).
        args: Argumentos da ferramenta, esperando uma chave "url".
    
    Returns:
        Uma tupla com o nome do campo a ser atualizado no estado e um dicionário
        contendo o 'content' ou um 'error'.
    """
    url = args.get("url", "")
    if "tabnews.com.br" not in url:
        return ("url_content", {"error": "A URL deve ser do domínio tabnews.com.br"})

    try:
        # Define um timeout para evitar que a requisição fique presa indefinidamente
        response = requests.get(url, timeout=10)
        # Lança uma exceção para códigos de erro HTTP (4xx ou 5xx)
        response.raise_for_status()

        # Usa nossa nova função para processar o conteúdo
        main_text = process_html_content(response.content)

        if not main_text:
            return ("url_content", {"error": "Falha ao processar o conteúdo HTML da página."})

        # Retorna o conteúdo processado com sucesso
        return ("url_content", {"content": main_text})

    except requests.exceptions.RequestException as e:
        # Captura erros de rede (DNS, conexão, timeout, etc.)
        return ("url_content", {"error": f"Falha ao buscar a URL: {e}"})