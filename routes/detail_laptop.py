from flask import render_template
from laptopDB import Notebook, PriceHistory, Review, Consumer

def notebook_detail(id):
    notebook = Notebook.query.get_or_404(id)

    # 가격 이력 데이터를 정렬하여 가져오기
    price_history = PriceHistory.query.filter_by(notebook_key=id).order_by(PriceHistory.date).all()
    reviews = Review.query.filter_by(notebook_key=id).join(Consumer).all()
    return render_template("detail.html", notebook=notebook, price_history=price_history, reviews=reviews)