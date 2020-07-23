# vestlus:settings
import os

CRISPY_TEMPLATE_PACK = 'bootstrap4'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': os.environ.get('ELASTICSEARCH_URL', 'http://127.0.0.1:9200/'),
        'INDEX_NAME': 'haystack',
    },
}
