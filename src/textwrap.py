import textwrap
from datetime import datetime

def wrap_text(value, width=80):
    """Metni veya metin listesini belirli bir genişlikte satırlara böler."""
    # Değer datetime türünde ise stringe çevir
    if isinstance(value, datetime):
        text = value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, list):
        # Liste öğelerini bir string'e çevir
        text = ', '.join(map(str, value))  # Liste içindeki her öğeyi stringe çevir
    else:
        text = str(value)  # Diğer tüm değerleri stringe çevir

    wrapped_text = '\n'.join(textwrap.wrap(text, width))
    return wrapped_text
