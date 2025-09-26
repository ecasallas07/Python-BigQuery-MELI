SITES = [
    {
        'name': 'Mercado Libre',
        'url': 'https://www.mercadolibre.com.co/ofertas',
        'selectors': {
            'container': '.andes-card.poly-card',                # Contenedor de cada promo
            'title': '.poly-component__title',                   # Título del producto
            'price': '.poly-price__current .andes-money-amount__fraction', # Precio actual
            'link': '.poly-component__title',                    # Enlace (href)
            'image': '.poly-component__picture'                  # Imagen
        }
    },
]