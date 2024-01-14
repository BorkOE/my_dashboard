# TODO:
'''
    - Remove/edit entries
    - back to journal_index page
'''

from flask import Flask, session, render_template, request, g
from db_handler_journal import DatabaseHandlerJournal
from db_handler_study import DatabaseHandlerStudy
from config_handler import ConfigHandler
from utils import update_journal_stats, update_ekonomi_stats
# import json

def safe_json_string(s):
    if not s:
        return 
    return (s
            .replace('\r\n', '\\r\\n')
            .replace('"', '\\"')
            )

app = Flask(__name__)
dbh_journal = DatabaseHandlerJournal()
dbh_study = DatabaseHandlerStudy()
config_hand = ConfigHandler()

'''Main dashboard'''
@app.route("/", methods=['get', 'post'])
def index():
    '''Main page where I navigate to my apps'''
    return render_template("index.html")

@app.route("/update", methods=['get', 'post'])
def update_stats():
    update_journal_stats.run()
    update_ekonomi_stats.run()
    return index()

'''Journal'''
@app.route("/journal_index", methods=['get', 'post'])
def journal_index():
    '''Main page for journal'''
    submited_text = request.form.get('journal_text')
    submited_rank = request.form.get('rank')
    submited_hv = request.form.get('headache')
    if submited_text:
        dbh_journal.add_journal(submited_text)
    if submited_rank:
        dbh_journal.add_rank(submited_rank)
    if submited_hv:
        dbh_journal.add_headache(submited_hv)


    return render_template("journal_index.html")

@app.route("/edit_text", methods=['get', 'post'])
def edit_text():
    '''Main page but from having edited text'''
    submited_text = request.form.get('journal_text')
    submited_rank = request.form.get('rank')
    submited_hv = request.form.get('headache')


    date = request.form.get('date')
    dbh_journal.add_journal(submited_text, purge_old=True, date=date)
    if submited_rank:
        dbh_journal.add_rank(submited_rank, date=date)
    if submited_hv:
        dbh_journal.add_headache(submited_hv, date=date)


    return render_template("journal_index.html")

@app.route("/show_journals")
def show_journals():
    all_journals = dbh_journal.get_all_journals()
    all_rankings = dbh_journal.get_all_rankings()
    all_hv = dbh_journal.get_all_hv()
    all_journals = {k: safe_json_string(v) for k, v in all_journals.items()}
    return render_template("show_journals.html", data=all_journals, rankings=all_rankings, headache=all_hv)

'''Study helper'''
@app.route("/study_index", methods=['get', 'post'])
def study_index():
    '''Main page study helper'''
    table_select = request.form.get('table_select')
    if table_select and table_select not in ['Flashcards', 'Guess game']:
        dbh_study.set_current_table(table_select)
        config_hand.set_last_opened_table(table_select)

    cats = dbh_study.get_all_categories()
    tables = dbh_study.get_tables()
    last_table = config_hand.get_last_opened_table()
    return render_template("study_index.html", categories=cats, tables=tables, last_table=last_table)

@app.route("/add_data")
def add_data():
    '''TODO: Under development'''
    return render_template('add_data.html')

@app.route("/play_all")
def play_all():
    text_dict = dbh_study.get_all_texts(uniqify=True)
    return render_template('flashcards.html', data=text_dict)

@app.route("/play_category", methods=['post'])
def play_category():
    selected_categories = [v for v in request.form if v != 'table_select']
    if not selected_categories:     # Empty selection
        return study_index()
    
    text_dict = dbh_study.get_categorcal_texts(selected_categories)
    game_type = request.form.get('table_select')
    
    if game_type == 'Guess game':
        return render_template('guess_game.html', data=dbh_study.make_json_safe(text_dict))
    elif game_type == 'Flashcards':
        return render_template('flashcards.html', data=text_dict)
    else:
        return study_index()

'''Stats'''
@app.route("/ekonomi", methods=['get', 'post'])
def ekonomi():
    return render_template('bokeh/ekonomi.html')

@app.route("/mående", methods=['get', 'post'])
def mående():
    return render_template('bokeh/mående.html')


'''System'''
def print_exeption(exception):
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1902, debug=True)
