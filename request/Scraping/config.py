SITES = [
    {
        'name': 'E-commerce 1',
        'url': 'https://www.ecommerce1.com/promotions',
        'selectors': {
            'container': '.promo-container',  # Selector del contenedor de cada promoción
            'title': '.promo-title',         # Selector del título del producto
            'price': '.promo-price',         # Selector del precio
            'link': '.promo-link',           # Selector del enlace
            'image': '.promo-image'          # Selector de la imagen
        }
    },
    {
        'name': 'E-commerce 2',
        'url': 'https://www.ecommerce2.com/deals',
        'selectors': {
            'container': '.deal-item',
            'title': '.deal-title',
            'price': '.deal-price',
            'link': '.deal-link',
            'image': '.deal-image'
        }
    }
]