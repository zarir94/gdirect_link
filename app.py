from flask import Flask, request, jsonify
from re import findall
from requests import get
from urllib.parse import unquote_plus


def get_link_offline(link):
    data = findall(r"d/\w+", link)
    if not data:
        return False
    file_id = data[0].split('/')[1]
    direct_link = f"https://drive.google.com/uc?id={file_id}&export=download&confirm=t"
    return direct_link


def get_link_online(link):
    resp = get(link)
    html = resp.text
    data = findall(r"{config: {'id': '\w+'", html)
    if not data:
        return False
    file_id = findall(r"\w+", data[0])[-1]
    direct_link = f"https://drive.google.com/uc?id={file_id}&export=download&confirm=t"
    return direct_link


app = Flask(__name__)
app.config['SECRET_KEY'] = 'iureyu48783d#8*#^37489xnhkc'


@app.route("/", methods=['POST'])
def home():
    link = unquote_plus(request.form.get('url'))
    mode = request.form.get('mode', 'online')
    if mode == 'online':
        direct_link = get_link_online(link)
    else:
        direct_link = get_link_offline(link)
    if not direct_link:
        return jsonify({'success': False})
    else:
        return jsonify({'success': True, 'link': direct_link})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)

# https://drive.google.com/file/d/1itF4K1mkYhU5DgRKh6vaAmtBRz5aXlki/view?usp=sharing
