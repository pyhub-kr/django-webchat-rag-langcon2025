from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import RoomForm
from .models import Room, TaxLawDocument


# 채팅방 목록 페이지 (클래스 기반 뷰)
room_list = ListView.as_view(model=Room)


# 새 채팅방 생성 페이지 (클래스 기반 뷰)
room_new = CreateView.as_view(
    model=Room,
    form_class=RoomForm,
    success_url=reverse_lazy("chat:room_list"),
)


# 채팅방 채팅 페이지 (함수 기반 뷰)
def room_detail(request, pk):
    # 지정 채팅방 조회하고, 데이터베이스에 없으면 404 오류 발생
    room = get_object_or_404(Room, pk=pk)
    # 지정 채팅방의 모든 대화 목록
    message_list = room.message_set.all()
    return render(
        request,
        "chat/room_detail.html",
        {
            "room": room,
            "message_list": message_list,
        },
    )


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
