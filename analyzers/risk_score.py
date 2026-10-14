def calculate_risk_score(

    issues
):

    score = 0

    for issue in issues:

        if "[CRITICAL]" in issue:

            score += 40

        elif "[WARNING]" in issue:

            score += 20

    return min(score, 100)