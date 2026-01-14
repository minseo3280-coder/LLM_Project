"""
AI BURGER HOUSE - 메뉴 데이터
버거 9개 + 사이드 3개 + 음료 3개 (총 15개)
"""
from typing import List, Dict, Any

MENU_DATA: List[Dict[str, Any]] = [
    # ===== 버거 (9개) =====
    {
        "menu_id": "BG001",
        "category": "버거",
        "name": "클래식 비프 버거",
        "price": 6900,
        "description": "신선한 소 패티, 토마토, 양상추, 피클",
        "spicy": 1,
        "calories": 520,
        "protein": 28,
        "preparation_time": "5분",
        "allergy": ["wheat", "soy"],
        "tags": ["meat", "beef", "classic"]
    },
    {
        "menu_id": "BG002",
        "category": "버거",
        "name": "더블 치즈 버거",
        "price": 8500,
        "description": "두 장의 비프 패티와 체다 치즈, 베이컨",
        "spicy": 1,
        "calories": 680,
        "protein": 38,
        "preparation_time": "7분",
        "allergy": ["wheat", "soy", "dairy"],
        "tags": ["meat", "beef", "cheese", "premium"]
    },
    {
        "menu_id": "BG003",
        "category": "버거",
        "name": "스파이시 할라피뇨 버거",
        "price": 7800,
        "description": "매운 할라피뇨 페퍼, 잭 치즈, 스리라차 소스",
        "spicy": 3,
        "calories": 580,
        "protein": 32,
        "preparation_time": "6분",
        "allergy": ["wheat", "soy", "dairy"],
        "tags": ["meat", "beef", "spicy", "premium"]
    },
    {
        "menu_id": "BG004",
        "category": "버거",
        "name": "버비큐 비프 버거",
        "price": 7500,
        "description": "스모키 BBQ 소스, 양파 링, 베이컨",
        "spicy": 2,
        "calories": 620,
        "protein": 30,
        "preparation_time": "6분",
        "allergy": ["wheat", "soy"],
        "tags": ["meat", "beef", "bbq"]
    },
    {
        "menu_id": "BG005",
        "category": "버거",
        "name": "크리스피 치킨 버거",
        "price": 6800,
        "description": "바삭한 튀긴 치킨 패티, 타르타르 소스",
        "spicy": 1,
        "calories": 540,
        "protein": 26,
        "preparation_time": "6분",
        "allergy": ["wheat", "soy", "eggs", "dairy"],
        "tags": ["meat", "chicken", "crispy"]
    },
    {
        "menu_id": "BG006",
        "category": "버거",
        "name": "머쉬룸 스위스 버거",
        "price": 8200,
        "description": "그릴드 머쉬룸, 스위스 치즈, 카라멜화 양파",
        "spicy": 0,
        "calories": 560,
        "protein": 24,
        "preparation_time": "7분",
        "allergy": ["wheat", "soy", "dairy"],
        "tags": ["meat", "beef", "mushroom", "premium"]
    },
    {
        "menu_id": "BG007",
        "category": "버거",
        "name": "터플 미트 버거",
        "price": 9200,
        "description": "비프, 베이컨, 소시지, 더블 치즈 (초대형)",
        "spicy": 1,
        "calories": 750,
        "protein": 45,
        "preparation_time": "8분",
        "allergy": ["wheat", "soy", "dairy"],
        "tags": ["meat", "beef", "premium", "highprotein"]
    },
    {
        "menu_id": "BG008",
        "category": "버거",
        "name": "그린 베지 버거",
        "price": 6500,
        "description": "두부 패티, 버섯, 아보카도, 시금치",
        "spicy": 0,
        "calories": 380,
        "protein": 14,
        "preparation_time": "5분",
        "allergy": ["wheat", "soy"],
        "tags": ["vegetarian", "healthy", "vegan"]
    },
    {
        "menu_id": "BG009",
        "category": "버거",
        "name": "아메리칸 클래식 콤보",
        "price": 7200,
        "description": "시그니처 비프, 아메리칸 치즈, 분쇄 양파",
        "spicy": 0,
        "calories": 540,
        "protein": 28,
        "preparation_time": "5분",
        "allergy": ["wheat", "soy", "dairy"],
        "tags": ["meat", "beef", "classic", "popular"]
    },

    # ===== 사이드 (3개) =====
    {
        "menu_id": "SD001",
        "category": "사이드",
        "name": "크리스피 감자튀김",
        "price": 3500,
        "description": "황금색 바삭한 감자튀김, 자염 양념",
        "spicy": 1,
        "calories": 320,
        "protein": 4,
        "preparation_time": "2분",
        "allergy": [],
        "tags": ["side", "fried", "popular"]
    },
    {
        "menu_id": "SD002",
        "category": "사이드",
        "name": "나초 with 치즈",
        "price": 4200,
        "description": "또띠아 칩, 녹인 치즈, 살사, 사워크림",
        "spicy": 1,
        "calories": 380,
        "protein": 8,
        "preparation_time": "3분",
        "allergy": ["dairy"],
        "tags": ["side", "cheese", "appetizer"]
    },
    {
        "menu_id": "SD003",
        "category": "사이드",
        "name": "치킨 너겟 (6개)",
        "price": 4000,
        "description": "부드러운 닭고기 너겟, 혼스 머스터드",
        "spicy": 0,
        "calories": 340,
        "protein": 18,
        "preparation_time": "3분",
        "allergy": ["wheat", "eggs", "soy"],
        "tags": ["side", "chicken", "fried"]
    },

    # ===== 음료 (3개) =====
    {
        "menu_id": "DR001",
        "category": "음료",
        "name": "콜드 소다",
        "price": 2500,
        "description": "얼음이 가득한 상큼한 소다 (250ml)",
        "spicy": 0,
        "calories": 140,
        "protein": 0,
        "preparation_time": "1분",
        "allergy": [],
        "tags": ["beverage", "cold", "soda"]
    },
    {
        "menu_id": "DR002",
        "category": "음료",
        "name": "단백질 쉐이크",
        "price": 5000,
        "description": "휘프로틴, 바나나, 우유 (고단백)",
        "spicy": 0,
        "calories": 220,
        "protein": 28,
        "preparation_time": "2분",
        "allergy": ["dairy"],
        "tags": ["beverage", "shake", "highprotein", "healthy"]
    },
    {
        "menu_id": "DR003",
        "category": "음료",
        "name": "콜라",
        "price": 2500,  # 가격 수정: 5000 → 2500 (일반적인 음료 가격)
        "description": "시원한 콜라 (250ml)",
        "spicy": 0,
        "calories": 140,
        "protein": 0,
        "preparation_time": "1분",
        "allergy": [],  # dairy 제거 (콜라에는 유제품 없음)
        "tags": ["beverage", "cold", "cola"]
    }
]


def get_menu_data() -> List[Dict[str, Any]]:
    """메뉴 데이터 반환"""
    return MENU_DATA


def get_categories() -> Dict[str, List[Dict[str, Any]]]:
    """카테고리별 메뉴 목록 반환"""
    categories: Dict[str, List[Dict[str, Any]]] = {}
    for menu in MENU_DATA:
        cat = menu["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(menu)
    return categories


def get_menu_by_id(menu_id: str) -> Dict[str, Any] | None:
    """메뉴 ID로 메뉴 검색"""
    for menu in MENU_DATA:
        if menu["menu_id"] == menu_id:
            return menu
    return None


def get_menus_by_tag(tag: str) -> List[Dict[str, Any]]:
    """태그로 메뉴 검색"""
    return [m for m in MENU_DATA if tag in m["tags"]]