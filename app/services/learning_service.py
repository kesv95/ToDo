
def diagnose_learning(study, plan, review):
    """학습 점수를 계산하고 진단 결과와 조언을 반환한다."""

    score = study + plan + review

    if score >= 10:
        diagnosis = "우수한 학습 습관입니다!"
        advice = "현재의 공부 습관을 유지하고 심화 학습에 도전하세요."

    elif score >= 7:
        diagnosis = "양호하지만 개선할 부분이 있어요."
        advice = "공부 계획을 세우고 배운 내용을 꾸준히 복습하세요."

    else:
        diagnosis = "학습 습관을 조금씩 만들어 보세요."
        advice = "하루 20분부터 시작해 작은 목표를 실천하세요."

    return score, diagnosis, advice
