"""
Esta es la documentación del módulo stream.
Proporciona la clase principal Stream para manejar contenido multimedia.
"""
from .utils import url_streaming, url_download, captions_url, url_image, thumbnail_url, video_durations

class Stream:
    """
    Clase que representa un gestor de streaming de contenido multimedia.
    """
    
    @staticmethod
    async def get_stream_url(url: str, api_url: str) -> str:
        """
        Obtiene la URL de streaming del contenido.
        
        Args:
            url (str): URL de Telegram del contenido
            api_url (str): URL base de la API
            
        Returns:
            str: URL de streaming o None si hay error
        """
        if not url or not api_url:
            return None
        return await url_streaming(url, api_url)
    
    @staticmethod
    async def get_url_download(url: str, api_url: str) -> str:
        """
        Obtiene la URL de streaming del contenido.
        
        Args:
            url (str): URL de Telegram del contenido
            api_url (str): URL base de la API
            
        Returns:
            str: URL de streaming o None si hay error
        """
        if not url or not api_url:
            return None
        return await url_download(url, api_url)

    @staticmethod
    async def get_captions(url: str, api_url: str) -> dict:
        """
        Obtiene la descripción del contenido.
        
        Args:
            url (str): URL de Telegram del contenido
            api_url (str): URL base de la API
            
        Returns:
            dict: Respuesta con el caption o None si hay error
        """
        if not url or not api_url:
            return None
        return await captions_url(url, api_url)
    
    @staticmethod
    async def get_images(url: str, api_url: str) -> str:
        """
        Obtiene la URL de la miniatura del contenido.
        
        Args:
            url (str): URL de Telegram del contenido
            api_url (str): URL base de la API
            
        Returns:
            str: URL de la imagen o None si hay error
        """
        if not url or not api_url:
            return None
        return await url_image(url, api_url)
    
    @staticmethod
    async def get_thumbnail(url: str, api_url: str) -> str:
        """
        Obtiene la URL del banner del contenido.
        
        Args:
            url (str): URL de Telegram del contenido
            api_url (str): URL base de la API
            
        Returns:
            str: URL del banner o None si hay error
        """
        if not url or not api_url:
            return None
        return await thumbnail_url(url, api_url)

    @staticmethod
    async def get_video_durations(url: str, api_url: str) -> str:
        """
        Obtiene la duración de un video.
        
        Args:
            url (str): URL de Telegram del contenido
            api_url (str): URL base de la API
            
        Returns:
            str: URL del video o None si hay error
        """
        if not url or not api_url:
            return None
        return await video_durations(url, api_url)