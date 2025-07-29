"""
Funciones útiles para streaming
"""
import base64
import requests
import re
from typing import Optional



async def get_token(url: str, api_url: str) -> Optional[str]:
    """
    Obtiene un token de acceso para un archivo de Telegram.
    
    Args:
        url (str): URL del mensaje de Telegram (formato: https://t.me/c/12345/67890)
        api_url (str): URL base de la API
        
    Returns:
        Optional[str]: Token de acceso o None si hay error
    """

    try:
        # Extraer chat_id y file_id de la URL de Telegram
        match = re.match(r'https://t\.me/c/(\d+)/(\d+)', url)
        if not match:
            return None
            
        chat_id, file_id = match.groups()
        
        # Preparar payload como diccionario con valores string
        payload = {
            "chat_id": str(f"-100{chat_id}"),
            "file_id": str(file_id)
        }
        
        # Obtener token con headers específicos
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # Obtener token
        response = requests.post(
            f"{api_url}/token",
            json=payload,
            headers=headers,
            timeout=10
        )
        
        response.raise_for_status()  # Lanza excepción si status_code != 200
        return response.json().get('token')

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el token: {str(e)}")
        return None
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None

async def url_streaming(url: str, api_url: str) -> Optional[str]:
    """
    Genera URL para streaming de un archivo.
    
    Args:
        url (str): URL del mensaje de Telegram
        api_url (str): URL base de la API
        
    Returns:
        Optional[str]: URL de streaming o None si hay error
    """

    try:

        # Construir y devolver la URL final
        token = await get_token(url, api_url)
        if not token:
            return None
        final_url = f"{api_url}/dl?token={token}"
        
        return final_url

    except Exception as e:
        print(f"Error en: {str(e)}")
        return None


async def url_download(url: str, api_url: str) -> Optional[str]:
    """
    Genera URL para descarga de un archivo.
    
    Args:
        url (str): URL del mensaje de Telegram
        api_url (str): URL base de la API
        
    Returns:
        Optional[str]: URL de descarga o None si hay error
    """

    try:

        # Construir y devolver la URL final
        token = await get_token(url, api_url)
        if not token:
            return None
        final_url = f"{api_url}/download?token={token}"
        
        return final_url

    except Exception as e:
        print(f"Error en: {str(e)}")
        return None

async def captions_url(url, api_url):
    """Obtiene los subtítulos de la película o serie"""

    try:
        caption_response = requests.get(
            f"{api_url}/get?url={url}",
            timeout=10
        )
        if caption_response.status_code != 200:
            return None 
        
        return caption_response

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los subtítulos: {str(e)}")
        return None

async def get_base64(url):
    """Obtiene el enlace base64 de la película o serie"""

    try:
        base64_url = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        return base64_url

    except Exception as e:
        print(f"Error al obtener el enlace base64: {str(e)}")
        return None
    
async def url_image(url, api_url):
    """Obtiene la imagen de la película o serie"""

    try:
        # Mandamos la url a base64
        base64_url = await get_base64(url)
        if not base64_url:
            return None
        
        # Construir la URL de la imagen 
        image_url = f"{api_url}/img?url={base64_url}"
        
        return image_url

    except Exception as e:
        print(f"Error al obtener la imagen: {str(e)}")
        return None

async def thumbnail_url(url, api_url):
    """
    Obtiene la URL del thumbnail de un video
    """
    try:

        base64_url = await get_base64(url)
        if not base64_url:
            return None
        
        # Construir la URL final
        api_url = f"{api_url}/thumb?url={base64_url}"
        return api_url
    
    except Exception as e:
        print(f"Error al obtener la URL de la imagen: {str(e)}")
        return None

async def video_durations(url, api_url):
    """
    Obtiene la duración del video
    """

    try:
        base64_url = await get_base64(url)
        if not base64_url:
            return None
        
        api_url = f"{api_url}/d?url={base64_url}"
        return api_url
    
    except Exception as e:
        print(f"Error al obtener la duración del video: {str(e)}")

