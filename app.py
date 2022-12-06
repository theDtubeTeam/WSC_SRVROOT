from flask import Flask, render_template, request, redirect, Response
from flask_babel import Babel, gettext
from werkzeug.serving import WSGIRequestHandler
from werkzeug.urls import url_encode
from urllib.request import Request, urlopen

import time
import random
import json
import osc
import ssl
import socket

OpenShopChannel = osc.API()
OpenShopChannel.load_packages()

app = Flask(__name__)
babel = Babel(app)

lastCheckedFeaturedApp = 0


def category_translation(category):
    if category == "demos":
        return gettext("Demos")
    elif category == "utilities":
        return gettext("Utilities")
    elif category == "emulators":
        return gettext("Emulators")
    elif category == "games":
        return gettext("Games")
    elif category == "media":
        return gettext("Media")


app.jinja_env.globals.update(category_translation=category_translation)


@babel.localeselector
def get_locale():
    if request.cookies.get('language'):
        return request.cookies.get('language')
    else:
        return 'en'


def get_error_text(code):
    with open("data/errors.json", 'r') as f:
        data = json.load(f)[code][0]["desc"]
        return gettext(data)


def get_motd():
    with open("data/motd.txt") as f:
        lines = f.readlines()
        return random.choice(lines).rstrip("\n")


def get_featured_app():
    global lastCheckedFeaturedApp
    if time.time() - lastCheckedFeaturedApp > 1800:
        lastCheckedFeaturedApp = time.time()
        req = Request('https://oscwii.org')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0')
        contents = str(urlopen(req).read()).split("App of the Day: ")[1].split("/library/app/")[1].split("\"")[0]
        with open('data/featuredApp.txt', "w") as f:
            f.write(contents)
    with open('data/featuredApp.txt', "r") as f:
        featured_app = f.read()
    return featured_app


@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))


@app.route("/")
def splash():
    return render_template('splash.html')

@app.route("/B_24.jsp")
def randompage():
    return render_template('splash.html')

@app.route("/virtcon")
def virtcon():
    return render_template('virtual_console.html')

@app.route("/sbs")
def sbs():
    return render_template('search_by_system.html')

@app.route("/str2")
def str2():
    return render_template('str2hax.html')

@app.route("/debug")
def debug():
    return render_template('debug.html')


@app.route("/landing")
def landing():
    return render_template('landing.html', motd=get_motd(),
                           featured_app=OpenShopChannel.package_by_name(get_featured_app()))


@app.route("/donate")
def donate():
    return render_template('donate.html')


@app.route("/browse")
def browse():
    return render_template('browse.html', featuredApp=get_featured_app())


@app.route("/keyword")
def keyword():
    return render_template('keyword.html')

@app.route("/home")
def home():
    return render_template('home.html')
    
@app.route("/WiiPoints")
def WiiPoints():
    return render_template('Wii_Points.html')
    
@app.route("/pointscard")
def pointscard():
    return render_template('Redeem_PointCard.html')

@app.route("/downloadinfo")
def downloadinfo():
    return render_template('downloadinfo.html')

@app.route("/Amount")
def Amount():
    return render_template('Amount.html')

@app.route("/creditcard")
def creditcard():
    return render_template('creditcard.html')
  
@app.route("/visa")
def visa():
    return render_template('visa.html')

@app.route("/settingsandfeatures")
def settingsandfeatures():
    return render_template('settingsandfeatures.html')
    
@app.route("/gift")
def gift():
    return render_template('gift.html')
    
@app.route("/wiiticket")
def wiiticket():
    return render_template('wiiticket.html')


@app.route("/category")
def category():
    return render_template('catalog.html', wiipoints=random.randint(0, 10000))


@app.route("/startdownload")
def start_download():
    selected_app = request.args.get('app', default='danbo', type=str)
    selected_app = OpenShopChannel.package_by_name(selected_app)
    return render_template('startdownload.html', app=selected_app)


@app.route("/search")
def search():
    rpp = 16 # max results
    key = request.args.get('key', default='category', type=str)
    value = request.args.get('value', default='Wii Channels', type=str).lower()
    page = request.args.get('page', default=0, type=int)

    results = OpenShopChannel.search_packages(key, value)

    last_page = ""
    next_page = ""

    if len(results[page * 2 * rpp:(page * 2 * rpp) + rpp]) == 0 or len(results[page * rpp:(page * rpp) + rpp]) < 4:
        next_page = ""
    elif len(results) > 0:
        next_page = "search?key=" + key + "&value=" + value + "&page=" + str(page + 1)

    if page == 0:
        last_page = ""
    elif len(results) > 0:
        last_page = "search?key=" + key + "&value=" + value + "&page=" + str(page - 1)
    print(results)
    return render_template('catalog.html', results=results[page * rpp:(page * rpp) + rpp], lastPage=last_page,
                           nextPage=next_page, wiipoints=random.randint(0, 10000))

@app.route("/popular")
def popular():
    rpp = 16 # max results
    key = request.args.get('key', default='category', type=str).replace("%20", " ")
    value = request.args.get('value', default='danbo', type=str).lower()
    page = request.args.get('page', default=0, type=int)

    results = OpenShopChannel.search_packages(key, value)

    last_page = ""
    next_page = ""

    if len(results[page * 2 * rpp:(page * 2 * rpp) + rpp]) == 0 or len(results[page * rpp:(page * rpp) + rpp]) < 4:
        next_page = ""
    elif len(results) > 0:
        next_page = "search?key=" + key + "&value=" + value + "&page=" + str(page + 1)

    if page == 0:
        last_page = ""
    elif len(results) > 0:
        last_page = "search?key=" + key + "&value=" + value + "&page=" + str(page - 1)
    print(results)
    return render_template('pop_titles.html', results=results[page * rpp:(page * rpp) + rpp], lastPage=last_page,
                           nextPage=next_page, wiipoints=random.randint(0, 10000))

@app.route("/news")
def news():
    page = request.args.get('p', default=1, type=int)

    if page == 1:
        newss = '{"title":"penis", "data":"uugha"}'
        news = json.loads(newss)
        return render_template('news.html', wiipoints=random.randint(0, 10000), news=news)

    elif page == 2:
        newss = '{"title":"Never Gonna GIVE YOU UP", "data":"Never Gonna LET YOU DOWN<br>Never Gonna Tell a lie<br>Or HURT YOU"}'
        news = json.loads(newss)
        return render_template('news.html', wiipoints=random.randint(0, 10000), news=news)

    elif page == 3:
        newss = '{"title":"penis", "data":"uugha"}'
        news = json.loads(newss)
        return render_template('news.html', wiipoints=random.randint(0, 10000), news=news)

@app.route("/app")
def app_page():
    selected_app = request.args.get('app', default='danbo', type=str)
    selected_app = OpenShopChannel.package_by_name(selected_app)
    print(selected_app)
    return render_template('app.html', game=selected_app, wiipoints="1000")


@app.route("/eula/018/en.html")
def random_app():
    return render_template('str2hax.html', wiipoints=random.randint(0, 10000))


@app.route("/error")
def error_age():
    error_code = request.args.get('error', default='danbo', type=str)
    error_text = get_error_text(error_code)
    if error_code == "SUCCESS":
        return redirect("/", code=302)
    else:
        return render_template('error.html', error_code=error_code, error_text=error_text)


@app.errorhandler(404)
def page_not_found(e):
    error_code = "HTTP_404"
    error_text = gettext("The requested page could not be found.")
    return render_template('error.html', error_code=error_code, error_text=error_text), 404


@app.errorhandler(500)
def server_error(e):
    error_code = "HTTP_500"
    error_text = gettext("The server has encountered an error. Try again later.")
    return render_template('error.html', error_code=error_code, errortext=error_text), 500


if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    # Hint that we are about to use very brittle ciphers.
    context.set_ciphers('ALL:@SECLEVEL=0')
    context.load_cert_chain('cert.pem', 'key.pem')

    app.run(host=socket.gethostbyname(socket.gethostname()), port=443, debug=True, ssl_context=context)