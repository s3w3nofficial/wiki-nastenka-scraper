#!flask/bin/python3
from flask import Flask, jsonify, request
import requests
from lxml import html
import threading, time

caching_time = 3600
is_caching = False

studenti_users_tree = None
studenti_articles_tree = None
studenti_programs_tree = None
seniori_users_tree = None
seniori_articles_tree = None
seniori_programs_tree = None
knihovny_users_tree = None
knihovny_articles_tree = None
knihovny_programs_tree = None

class ReCache(threading.Thread ):

    
    def __init__(self):
        global thread
        threading.Thread.__init__(self)

    def run(self):
        global caching_time
        global is_caching
        global studenti_users_tree
        global studenti_articles_tree
        global studenti_programs_tree
        global seniori_users_tree
        global seniori_articles_tree
        global seniori_programs_tree
        global knihovny_users_tree
        global knihovny_articles_tree
        global knihovny_programs_tree
        while  True:
            is_caching = True
            print ("caching")
            studenti_users_body = requests.get(base + 'studenti/users')
            studenti_articles_body = requests.get(base + 'studenti/articles')
            studenti_programs_body = requests.get(base + '/studenti/programs')
            seniori_users_body = requests.get(base + 'seniori/users')
            seniori_articles_body = requests.get(base + 'seniori/articles')
            seniori_programs_body = requests.get(base + '/seniori/programs')
            knihovny_users_body = requests.get(base + 'knihovny/users')
            knihovny_articles_body= requests.get(base + 'knihovny/articles')
            knihovny_programs_body = requests.get(base + '/knihovny/programs')
            studenti_users_tree = html.fromstring(studenti_users_body.content)
            studenti_articles_tree = html.fromstring(studenti_articles_body.content)
            studenti_programs_tree = html.fromstring(studenti_programs_body.content)
            seniori_users_tree = html.fromstring(seniori_users_body.content)
            seniori_articles_tree = html.fromstring(seniori_articles_body.content)
            seniori_programs_tree = html.fromstring(seniori_programs_body.content)
            knihovny_users_tree = html.fromstring(knihovny_users_body.content)
            knihovny_articles_tree = html.fromstring(knihovny_articles_body.content)
            knihovny_programs_tree = html.fromstring(knihovny_programs_body.content)
            is_caching = False
            print('done caching')
            time.sleep(caching_time)

base = "https://outreachdashboard.wmflabs.org/campaigns/";

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return jsonify({'it works': True})

@app.route('/api/studenti/users', methods=['GET'])
def api_studenti_users():
    while is_caching:
        time.sleep(1)

    tree = studenti_users_body
    if len(request.args) == 0:
        users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
        edit = tree.xpath('//*[@id="users"]/table/tbody/tr/td[2]/text()')
        for e in range(len(edit)):
            edit[e] = edit[e].replace('\n', '')
        program = tree.xpath('//*[@id="users"]/table/tbody/tr/td[3]/small/a/text()')
        return jsonify({'users': users, 'edit_count': edit, 'program' : program})
   
    payload = {}

    if request.args.get("users") == "1":
        users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
        payload['users'] = users
    if request.args.get("edit") == "1":
        edit = tree.xpath('//*[@id="users"]/table/tbody/tr/td[2]/text()')
        for e in range(len(edit)):
            edit[e] = edit[e].replace('\n', '')
        payload['edit'] = edit
    if request.args.get("program") == "1":
        program = tree.xpath('//*[@id="users"]/table/tbody/tr/td[3]/small/a/text()')
        payload['program'] = program

    return jsonify(payload)

@app.route('/api/studenti/articles', methods=['GET'])
def api_studenti_articles():
    while is_caching:
        time.sleep(1)

    tree = studenti_articles_tree
    if len(request.args) == 0:
        title = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td/a/text()')
        chars_added = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[2]/text()')
        for c in range(len(chars_added)):
            chars_added[c] = chars_added[c].replace('\n', '')
        views = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[3]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        return jsonify({'title' : title, 'chars_added' : chars_added, 'views' : views})
    
    payload = {}

    if request.args.get("title") == "1":
        title = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td/a/text()')
        payload['title'] = title
    if request.args.get("chars_added") == "1":
        chars_added = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[2]/text()')
        for c in range(len(chars_added)):
            chars_added[c] = chars_added[c].replace('\n', '')
        payload['chars_added'] = chars_added
    if request.args.get("views") == "1":
        views = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[3]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        payload['views'] = views

    return jsonify(payload)

@app.route('/api/studenti/programs', methods=['GET'])
def api_studenti_programs():
    while is_caching:
        time.sleep(1)

    tree = studenti_programs_tree
    if len(request.args) == 0:
        programs = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[1]/text()')
        for p in range(len(programs)):
            programs[p] = programs[p].replace('\n', 'n')
        institution_or_when = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[2]/text()')
        for iow in range(len(institution_or_when)):
            institution_or_when[iow] = institution_or_when[iow].replace('\n', '')
        recent_edits = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[3]/text()')
        for re in range(len(recent_edits)):
            recent_edits[re] = recent_edits[re].replace('\n', '')
        words_added = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[4]/span[1]/text()')
        for wa in range(len(words_added)):
            words_added[wa] = words_added[wa].replace('\n', '')
        views = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[5]/span[1]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        editors = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[6]/span/text()')
        for ed in range(len(editors)):
            editors[ed] = editors[ed].replace('\n', '')

        return jsonify({'programs' : programs, 'institution_or_when' : institution_or_when, 'recent_edits' : recent_edits, 'words_added' : words_added, 'views' : views, 'editors' : editors})

    payload = {}

    if request.args.get("programs") == "1":
        programs = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[1]/text()')
        for p in range(len(programs)):
            programs[p] = programs[p].replace('\n', 'n')
        payload['programs'] = programs
    if request.args.get('institution_or_when') == "1":
        institution_or_when = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[2]/text()')
        for iow in range(len(institution_or_when)):
            institution_or_when[iow] = institution_or_when[iow].replace('\n', '')
        payload['institution_or_when'] = institution_or_when
    if request.args.get('recent_edits') == "1":
        recent_edits = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[3]/text()')
        for re in range(len(recent_edits)):
            recent_edits[re] = recent_edits[re].replace('\n', '')
        payload['recent_edits'] = recent_edits
    if request.args.get("words_added") == "1":
        words_added = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[4]/span[1]/text()')
        for wa in range(len(words_added)):
            words_added[wa] = words_added[wa].replace('\n', '')
        payload['words_added'] = words_added
    if request.args.get('views') == "1":
        editors = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[6]/span/text()')
        for ed in range(len(editors)):
            editors[ed] = editors[ed].replace('\n', '')
        payload['views'] = views

    return jsonify(payload)

@app.route('/api/seniori/users', methods=['GET'])
def api_seniori_users():
    while is_caching:
        time.sleep(1)

    tree = seniori_users_tree
    if len(request.args) == 0:
        users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
        edit = tree.xpath('//*[@id="users"]/table/tbody/tr/td[2]/text()')
        for e in range(len(edit)):
            edit[e] = edit[e].replace('\n', '')
        program = tree.xpath('//*[@id="users"]/table/tbody/tr/td[3]/small/a/text()')
        return jsonify({'users': users, 'edit_count': edit, 'program' : program})
   
    payload = {}

    if request.args.get("users") == "1":
        users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
        payload['users'] = users
    if request.args.get("edit") == "1":
        edit = tree.xpath('//*[@id="users"]/table/tbody/tr/td[2]/text()')
        for e in range(len(edit)):
            edit[e] = edit[e].replace('\n', '')
        payload['edit'] = edit
    if request.args.get("program") == "1":
        program = tree.xpath('//*[@id="users"]/table/tbody/tr/td[3]/small/a/text()')
        payload['program'] = program

    return jsonify(payload)

@app.route('/api/seniori/articles', methods=['GET'])
def api_seniori_articles():
    while is_caching:
        time.sleep(1)

    tree = html.seniori_articles_tree
    if len(request.args) == 0:
        title = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td/a/text()')
        chars_added = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[2]/text()')
        for c in range(len(chars_added)):
            chars_added[c] = chars_added[c].replace('\n', '')
        views = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[3]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        return jsonify({'title' : title, 'chars_added' : chars_added, 'views' : views})
    
    payload = {}

    if request.args.get("title") == "1":
        title = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td/a/text()')
        payload['title'] = title
    if request.args.get("chars_added") == "1":
        chars_added = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[2]/text()')
        for c in range(len(chars_added)):
            chars_added[c] = chars_added[c].replace('\n', '')
        payload['chars_added'] = chars_added
    if request.args.get("views") == "1":
        views = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[3]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        payload['views'] = views

    return jsonify(payload)

@app.route('/api/seniori/programs', methods=['GET'])
def api_seniori_programs():
    while is_caching:
        time.sleep(1)

    tree = seniori_programs_tree
    if len(request.args) == 0:
        programs = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[1]/text()')
        for p in range(len(programs)):
            programs[p] = programs[p].replace('\n', 'n')
        institution_or_when = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[2]/text()')
        for iow in range(len(institution_or_when)):
            institution_or_when[iow] = institution_or_when[iow].replace('\n', '')
        recent_edits = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[3]/text()')
        for re in range(len(recent_edits)):
            recent_edits[re] = recent_edits[re].replace('\n', '')
        words_added = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[4]/span[1]/text()')
        for wa in range(len(words_added)):
            words_added[wa] = words_added[wa].replace('\n', '')
        views = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[5]/span[1]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        editors = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[6]/span/text()')
        for ed in range(len(editors)):
            editors[ed] = editors[ed].replace('\n', '')

        return jsonify({'programs' : programs, 'institution_or_when' : institution_or_when, 'recent_edits' : recent_edits, 'words_added' : words_added, 'views' : views, 'editors' : editors})

    payload = {}

    if request.args.get("programs") == "1":
        programs = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[1]/text()')
        for p in range(len(programs)):
            programs[p] = programs[p].replace('\n', 'n')
        payload['programs'] = programs
    if request.args.get('institution_or_when') == "1":
        institution_or_when = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[2]/text()')
        for iow in range(len(institution_or_when)):
            institution_or_when[iow] = institution_or_when[iow].replace('\n', '')
        payload['institution_or_when'] = institution_or_when
    if request.args.get('recent_edits') == "1":
        recent_edits = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[3]/text()')
        for re in range(len(recent_edits)):
            recent_edits[re] = recent_edits[re].replace('\n', '')
        payload['recent_edits'] = recent_edits
    if request.args.get("words_added") == "1":
        words_added = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[4]/span[1]/text()')
        for wa in range(len(words_added)):
            words_added[wa] = words_added[wa].replace('\n', '')
        payload['words_added'] = words_added
    if request.args.get('views') == "1":
        editors = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[6]/span/text()')
        for ed in range(len(editors)):
            editors[ed] = editors[ed].replace('\n', '')
        payload['views'] = views

    return jsonify(payload)

@app.route('/api/knihovny/users', methods=['GET'])
def api_knihovny_users():
    while is_caching:
        time.sleep(1)

    tree = knihovny_users_tree
    if len(request.args) == 0:
        users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
        edit = tree.xpath('//*[@id="users"]/table/tbody/tr/td[2]/text()')
        for e in range(len(edit)):
            edit[e] = edit[e].replace('\n', '')
        program = tree.xpath('//*[@id="users"]/table/tbody/tr/td[3]/small/a/text()')
        return jsonify({'users': users, 'edit_count': edit, 'program' : program})
   
    payload = {}

    if request.args.get("users") == "1":
        users = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
        payload['users'] = users
    if request.args.get("edit") == "1":
        edit = tree.xpath('//*[@id="users"]/table/tbody/tr/td[2]/text()')
        for e in range(len(edit)):
            edit[e] = edit[e].replace('\n', '')
        payload['edit'] = edit
    if request.args.get("program") == "1":
        program = tree.xpath('//*[@id="users"]/table/tbody/tr/td[3]/small/a/text()')
        payload['program'] = program

    return jsonify(payload)

@app.route('/api/knihovny/articles', methods=['GET'])
def api_knihovny_articles():
    while is_caching:
        time.sleep(1)

    tree = knihovny_articles_tree
    if len(request.args) == 0:
        title = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td/a/text()')
        chars_added = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[2]/text()')
        for c in range(len(chars_added)):
            chars_added[c] = chars_added[c].replace('\n', '')
        views = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[3]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        return jsonify({'title' : title, 'chars_added' : chars_added, 'views' : views})
    
    payload = {}

    if request.args.get("title") == "1":
        title = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td/a/text()')
        payload['title'] = title
    if request.args.get("chars_added") == "1":
        chars_added = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[2]/text()')
        for c in range(len(chars_added)):
            chars_added[c] = chars_added[c].replace('\n', '')
        payload['chars_added'] = chars_added
    if request.args.get("views") == "1":
        views = tree.xpath('//*[@id="campaign-articles"]/table/tbody/tr/td[3]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        payload['views'] = views

    return jsonify(payload)

@app.route('/api/knihovny/programs', methods=['GET'])
def api_knihovny_programs():
    while is_caching:
        time.sleep(1)

    tree = knihovny_programs_tree
    if len(request.args) == 0:
        programs = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[1]/text()')
        for p in range(len(programs)):
            programs[p] = programs[p].replace('\n', 'n')
        institution_or_when = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[2]/text()')
        for iow in range(len(institution_or_when)):
            institution_or_when[iow] = institution_or_when[iow].replace('\n', '')
        recent_edits = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[3]/text()')
        for re in range(len(recent_edits)):
            recent_edits[re] = recent_edits[re].replace('\n', '')
        words_added = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[4]/span[1]/text()')
        for wa in range(len(words_added)):
            words_added[wa] = words_added[wa].replace('\n', '')
        views = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[5]/span[1]/text()')
        for v in range(len(views)):
            views[v] = views[v].replace('\n', '')
        editors = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[6]/span/text()')
        for ed in range(len(editors)):
            editors[ed] = editors[ed].replace('\n', '')

        return jsonify({'programs' : programs, 'institution_or_when' : institution_or_when, 'recent_edits' : recent_edits, 'words_added' : words_added, 'views' : views, 'editors' : editors})

    payload = {}

    if request.args.get("programs") == "1":
        programs = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[1]/text()')
        for p in range(len(programs)):
            programs[p] = programs[p].replace('\n', 'n')
        payload['programs'] = programs
    if request.args.get('institution_or_when') == "1":
        institution_or_when = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[2]/text()')
        for iow in range(len(institution_or_when)):
            institution_or_when[iow] = institution_or_when[iow].replace('\n', '')
        payload['institution_or_when'] = institution_or_when
    if request.args.get('recent_edits') == "1":
        recent_edits = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[3]/text()')
        for re in range(len(recent_edits)):
            recent_edits[re] = recent_edits[re].replace('\n', '')
        payload['recent_edits'] = recent_edits
    if request.args.get("words_added") == "1":
        words_added = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[4]/span[1]/text()')
        for wa in range(len(words_added)):
            words_added[wa] = words_added[wa].replace('\n', '')
        payload['words_added'] = words_added
    if request.args.get('views') == "1":
        editors = tree.xpath('//*[@id="courses"]/table/tbody/tr/td[6]/span/text()')
        for ed in range(len(editors)):
            editors[ed] = editors[ed].replace('\n', '')
        payload['views'] = views

    return jsonify(payload)

if __name__ == '__main__':
    thread = threading.Thread()
    thread = ReCache()
    thread.daemon = True
    thread.start()
    app.run(debug=True, host="0.0.0.0", threaded=True)