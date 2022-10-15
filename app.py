from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 메인 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 검색 페이지
@app.route('/search')
def search():
    return render_template('search.html')

# 신규 도서 추가 페이지
@app.route('/newbook')
def newbook():
    return render_template('newbook.html')

@app.route('/newbook_action', methods=['POST'])
def newbook_action():
    title = request.form['bookname']
    booknumber = request.form['bookno']
    barcode = request.form['barcode']
    bookshelf = request.form['bookshelf']
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookdata VALUES (:title, :booknumber, :barcode, :bookshelf)",
            {'title': title, 'booknumber': booknumber, 'barcode': barcode, 'bookshelf': bookshelf})
    conn.commit()
    conn.close()
    return render_template('newbook_action.html')

# 도서 검색 결과 페이지
@app.route("/search_bookname", methods=['POST'])
def search_bookname():
    bookname = request.form['bookname']
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookdata WHERE title = :title", {'title': bookname})
    items = c.fetchall()
    if len(items) == 0:
        return render_template("error.html")
    c.execute("SELECT * FROM bookdata WHERE bookshelf = :bookshelf ORDER BY booknumber", {'title': bookname, 'bookshelf': items[0][3]})
    searchdata = c.fetchall()
    for i in range(len(searchdata)):
        if searchdata[i][0] == bookname:
            if i == 0:
                prevdata = ["(책 없음)", "(책 없음)", "(책 없음)", "(책 없음)"]
                nextdata = searchdata[i+1]
                break
            if i == len(searchdata)-1:
                prevdata = searchdata[i-1]
                nextdata = ["(책 없음)", "(책 없음)", "(책 없음)", "(책 없음)"]
                break
            prevdata = searchdata[i-1]
            nextdata = searchdata[i+1]
    conn.close()
    return render_template("search_bookname.html", bookname=bookname, prevbook=prevdata[0], nextbook=nextdata[0], bookshelf=items[0][3])

@app.route("/search_booknumber", methods=['POST'])
def search_booknumber():
    booknumber = request.form['booknumber']
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookdata WHERE booknumber = :booknumber", {'booknumber': booknumber})
    items = c.fetchall()
    if len(items) == 0:
        return render_template("error.html")
    c.execute("SELECT * FROM bookdata WHERE bookshelf = :bookshelf ORDER BY booknumber", {'bookshelf': items[0][3]})
    searchdata = c.fetchall()
    for i in range(len(searchdata)):
        if searchdata[i][0] == items[0][0]:
            if i == 0:
                prevdata = ["(책 없음)", "(책 없음)", "(책 없음)", "(책 없음)"]
                nextdata = searchdata[i+1]
                break
            if i == len(searchdata)-1:
                prevdata = searchdata[i-1]
                nextdata = ["(책 없음)", "(책 없음)", "(책 없음)", "(책 없음)"]
                break
            prevdata = searchdata[i-1]
            nextdata = searchdata[i+1]
    conn.close()
    return render_template("search_booknumber.html", bookname=items[0][0], prevbook=prevdata[0], nextbook=nextdata[0], bookshelf=items[0][3])

@app.route("/search_barcode", methods=['POST'])
def search_barcode():
    barcode = request.form['barcode']
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookdata WHERE barcode = :barcode", {'barcode': barcode})
    items = c.fetchall()
    if len(items) == 0:
        return render_template("error.html")
    c.execute("SELECT * FROM bookdata WHERE bookshelf = :bookshelf ORDER BY booknumber", {'bookshelf': items[0][3]})
    searchdata = c.fetchall()
    for i in range(len(searchdata)):
        if searchdata[i][0] == items[0][0]:
            if i == 0:
                prevdata = ["(책 없음)", "(책 없음)", "(책 없음)", "(책 없음)"]
                nextdata = searchdata[i+1]
                break
            if i == len(searchdata)-1:
                prevdata = searchdata[i-1]
                nextdata = ["(책 없음)", "(책 없음)", "(책 없음)", "(책 없음)"]
                break
            prevdata = searchdata[i-1]
            nextdata = searchdata[i+1]
    conn.close()
    return render_template("search_barcode.html", bookname=items[0][0], prevbook=prevdata[0], nextbook=nextdata[0], bookshelf=items[0][3])

# 서버 실행
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)