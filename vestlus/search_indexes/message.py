# vestlus:models:search_indexes
from vestlus.models import Message, PrivateMessage, GroupMessage
from haystack import indexes


class MessageIndex(indexes.BasicSearchIndex, indexes.Indexable):
    content_auto = indexes.EdgeNgramField(model_attr='content')
    rendered = indexes.CharField(
        use_template=True,
        indexed=False,
        template_name='search/indexes/vestlus/message_rendered.txt'
    )

    def get_model(self):
        return Message


class PrivateMessageIndex(MessageIndex):

    def get_model(self):
        return PrivateMessage


class GroupMessageIndex(MessageIndex):

    def get_model(self):
        return GroupMessage
