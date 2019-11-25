from flask import Flask,request,render_template,jsonify
from resolver import resolver

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html") 

@app.route('/process',methods= ['POST'])
def process():
    ctext = request.form['ctext']
    key = resolver(ctext)['key']
    plaintext = resolver(ctext)['text']
    if key and plaintext:
        return jsonify({'key': key,
                        'text': plaintext})
    return jsonify({'error' : 'Missing data!'})

if __name__ == '__main__':
    app.run()