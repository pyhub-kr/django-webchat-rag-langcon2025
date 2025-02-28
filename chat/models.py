import json

from django.utils.functional import cached_property
from pyhub.rag.fields.sqlite import SQLiteVectorField
from pyhub.rag.models.sqlite import SQLiteVectorDocument


class TaxLawDocument(SQLiteVectorDocument):
    embedding = SQLiteVectorField(
        dimensions=3072,
        editable=False,
        embedding_model="text-embedding-3-large",
    )

    @cached_property
    def page_content_obj(self):
        return json.loads(self.page_content)
