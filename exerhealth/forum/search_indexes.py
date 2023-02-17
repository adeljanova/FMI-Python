from haystack import indexes
from .models import Thread, Post


class ThreadIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    created_by = indexes.CharField(model_attr='created_by')

    def get_model(self):
        return Thread

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    body = indexes.CharField(model_attr='body')
    created_by = indexes.CharField(model_attr='created_by')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
