from typing import List, Dict, Tuple
import json
import re

def recommend_menus(menu_data: List[Dict], user_input: str, llm_engine=None) -> Tuple[Dict, List[Dict]]:
    
    intent = {
        "description": user_input,
        "allergies": [],
        "budget": None,
        "preferences": [],
        "understanding": ""
    }
    
    # 메뉴 데이터 간소화 (토큰 절약 및 속도 향상)
    menu_list_text = "\n".join([
        f"- {m['name']} ({m['price']}원, {', '.join(m['tags'])})"
        for m in menu_data
    ])
    
    analysis_prompt = f"""
역할: 햄버거 가게 AI 점원.
목표: 사용자 입력("{user_input}")을 분석하여 가장 적절한 메뉴를 추천.

[메뉴 목록]
{menu_list_text}

[응답 규칙]
1. 반드시 아래 JSON 형식으로만 응답할 것.
2. 설명은 한국어로 작성.
3. 추천 메뉴명은 메뉴 목록에 있는 이름을 정확히 사용.

{{
  "recommended_menus": ["메뉴이름1", "메뉴이름2"],
  "reason": "추천 이유",
  "budget": 숫자 또는 null,
  "allergies": ["감지된 알레르기 성분"],
  "understanding": "사용자 의도 요약"
}}
"""
    
    if llm_engine:
        try:
            print("LLM 분석 시작...") # 디버깅용
            response = llm_engine.generate_response(analysis_prompt)
            print(f"LLM 응답: {response}") # 디버깅용
            
            if response:
                # Markdown 코드 블록 제거 (```json ... ```)
                clean_response = re.sub(r'```json\s*|\s*```', '', response)
                
                # JSON 파싱
                # 혹시 모를 텍스트 섞임 방지를 위해 중괄호 찾기
                json_match = re.search(r'\{.*\}', clean_response, re.DOTALL)
                
                if json_match:
                    analysis = json.loads(json_match.group())
                    
                    # 데이터 매핑
                    intent["understanding"] = analysis.get("understanding", "")
                    intent["budget"] = analysis.get("budget")
                    intent["allergies"] = analysis.get("allergies", [])
                    intent["reason"] = analysis.get("reason", "")
                    
                    # 추천 메뉴 객체 찾기
                    rec_names = analysis.get("recommended_menus", [])
                    recommendations = [
                        m for m in menu_data 
                        if m["name"] in rec_names
                    ]
                    
                    # 추천이 없거나 부족하면 기본 메뉴 채우기
                    if len(recommendations) == 0:
                        return intent, menu_data[:4]
                        
                    return intent, recommendations

        except Exception as e:
            print(f"추천 로직 에러: {e}")
    
    # 실패 시 기본값
    return intent, menu_data[:4]

# suggest_combo 함수는 기존 그대로 유지
def suggest_combo(recommended_menus: List[Dict], all_menus: List[Dict], budget: int = None) -> Dict:
    # (기존 코드와 동일)
    if not recommended_menus: return None
    main = next((m for m in recommended_menus if m["category"] == "버거"), recommended_menus[0])
    
    available_sides = [m for m in all_menus if m["category"] == "사이드"]
    if budget: available_sides = [s for s in available_sides if main["price"] + s["price"] <= budget]
    side = available_sides[0] if available_sides else None
    
    available_drinks = [m for m in all_menus if m["category"] == "음료"]
    if budget and side: available_drinks = [d for d in available_drinks if main["price"] + side["price"] + d["price"] <= budget]
    drink = available_drinks[0] if available_drinks else None
    
    if side and drink:
        total = main["price"] + side["price"] + drink["price"]
        if budget and total > budget: return None
        return {"main": main, "side": side, "drink": drink, "total_price": total}
    return None