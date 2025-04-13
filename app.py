from flask import Flask, request, render_template
from scraper import scrape_product

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    title = price = weight = None
    if request.method == 'POST':
        url = request.form.get('url')
        title, price, weight = scrape_product(url)
    return render_template("index.html", title=title, price=price, weight=weight)

if __name__ == '__main__':
    app.run(debug=True)
