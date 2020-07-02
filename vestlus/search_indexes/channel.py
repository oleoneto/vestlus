# vestlus:models:search_indexes
from django.utils.timezone import datetime
from vestlus.models import Channel
from haystack import indexes


class ChannelIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    owner = indexes.CharField(model_attr='owner')
    creation_date = indexes.DateTimeField(model_attr='created_at')
    update_date = indexes.DateTimeField(model_attr='updated_at')
    messages = indexes.MultiValueField()
    content_auto = indexes.EdgeNgramField(model_attr='name')  # autocomplete
    rendered = indexes.CharField(use_template=True, indexed=False)  # html renderer

    def get_model(self):
        return Channel

    def prepare_messages(self, obj):
        # Store message content for filtering
        return [message.content for message in obj.conversations.all()]

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=datetime.now())
