from django.views.generic import ListView
from .models import TaxLawDocument


# 템플릿에서의 URL Reverse 참조를 위해 빈 View 함수 정의
def room_list(request):
    pass


def room_new(request):
    pass


def room_detail(request, pk):
    pass


# 문서 검색 페이지
class TaxLawDocumentListView(ListView):
    model = TaxLawDocument
    # sqlite의 similarity_search 메서드가 쿼리셋이 아닌 리스트를 반환하기 때문에
    # ListView에서 템플릿 이름을 찾지 못하기에 직접 지정해줍니다.
    template_name = "chat/taxlawdocument_list.html"

    def get_queryset(self):
        qs = super().get_queryset()

        query = self.request.GET.get("query", "").strip()
        if query:
            qs = qs.similarity_search(query)  # noqa: list 타입
        else:
            # 검색어가 없다면 빈 쿼리셋을 반환합니다.
            qs = qs.none()

        return qs
