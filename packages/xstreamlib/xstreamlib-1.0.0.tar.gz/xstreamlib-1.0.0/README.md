# XStreamLib

Una biblioteca Python moderna y fácil de usar para interactuar con la API de Udyat. Diseñada para ser flexible, robusta y permitir configuración personalizada de la URL de la API.

## ✨ Características

- 🚀 **Fácil de usar**: API intuitiva y bien documentada
- 🔒 **Manejo robusto de errores**: Excepciones personalizadas con información detallada
- 📁 **Subida de archivos**: Soporte nativo para multimedia
- 📦 **Context managers**: Gestión automática de recursos
- 🎯 **Type hints**: Completamente tipado para mejor experiencia de desarrollo
- 🔧 **Endpoints personalizados**: Flexibilidad total para cualquier API

## 🚀 Instalación

### Instalación básica

```bash
pip install xstreamlib
```

### 📖 Ejemplo básico
```python
import asyncio
from xstreamlib.stream import Stream

# URL base de la API
API_URL = "https://api.ejemplo.com"

async def main():
    # URL del contenido de ejemplo
    url = "https://t.me/c/1901234342559/1"
    
    # Obtener URL de streaming
    stream_url = await Stream.get_stream_url(url, api_url=API_URL)
    if stream_url:
        print(f"URL de streaming: {stream_url}")
    
    # Obtener subtítulos
    subtitles = await Stream.get_captions(url, api_url=API_URL)
    if subtitles:
        print(f"Subtítulos disponibles: {subtitles}")
    
    # Obtener miniatura
    thumbnail = await Stream.get_thumbnail(url, api_url=API_URL)
    if thumbnail:
        print(f"URL de miniatura: {thumbnail}")

if __name__ == "__main__":
    # Ejecutar el ejemplo
    asyncio.run(main())
```

### Tipos de errores comunes

- **400 Bad Request**: Parámetros inválidos
- **500 Internal Server Error**: Error del servidor

## 🆘 Soporte

- 📖 [Documentación](https://xstreamlib.readthedocs.io/)
- 🐛 [Issues](https://github.com/yourusername/xstreamlib/issues)
- 💬 [Discusiones](https://github.com/yourusername/xstreamlib/discussions)

### Próximas versiones

- [ ] **v0.0.2**: Mejoras

### Características futuras

- [ ] Métricas y monitoréo para limitar las peticiones 

## 🏆 Reconocimientos

- Agradecimientos al creador de la api mi grandioso padre
- Facilidad para obtener enlaces directos de telegram.
- Construido con amor para la comunidad de desarrolladores Python.

---

**¿Te gusta xstreamlib?** ¡Dale una ⭐ en GitHub y compártelo con otros desarrolladores!