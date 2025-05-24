from flask import render_template, request, redirect, url_for

def basic_search_form():
    return render_template("basic_search.html")

def search_basic():
    budget_input = request.form.get("budget", type=int)
    purpose = request.form.get("purpose")
    portability = request.form.get("portability")

    cpu_min, gpu_min = 0, 0
    if purpose == "office":
        cpu_min, gpu_min = 2000, 500
    elif purpose == "study":
        cpu_min, gpu_min = 6000, 4000
    elif purpose == "design":
        cpu_min, gpu_min = 1000, 8000
    elif purpose == "game":
        cpu_min, gpu_min = 9000, 12000

    # 예산 범위 설정
    budget_min, budget_max = 0, None
    if budget_input == 700000:
        budget_max = 700000
    elif budget_input == 1000000:
        budget_min, budget_max = 700000, 1000000
    elif budget_input == 1300000:
        budget_min, budget_max = 1000000, 1300000
    elif budget_input == 2000000:
        budget_min = 1300000

    # 휴대성 조건
    portability_filter = {}
    if portability == 'yes':
        portability_filter = {'weight_max': 1.5, 'display_max': 14}

    return redirect(url_for("render_results",
                            cpu_min=cpu_min, gpu_min=gpu_min,
                            budget_min=budget_min, budget_max=budget_max,
                            **portability_filter))
