'''
See repo README
'''

from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'


class Entry(db.Model):
    '''
    Stores blog entries
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()

    def is_valid(self):
        '''
        Our naive validation just requires that everything be present.
        '''
        if self.title and self.body and self.created:
            return True
        else:
            return False

#
@app.route("/")
def index():
    '''
    Convenience route so the bare URL displays all the entries
    '''
    return redirect("/blog")
#
@app.route("/blog")
def display_blog_entries():
    '''
    Either list one entry with the given ID
    Or list all blog entries (in default or newest order)
    '''
    # TODO refactor to use routes with variables instead of GET parameters
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Entry.query.get(entry_id)
        return render_template('single_entry.html', title="Blog Entry", entry=entry)

    # if we're here, we need to display all the entries
    # TODO store sort direction in session[] so we remember user's preference
    sort = request.args.get('sort')
    if (sort=="newest"):
        all_entries = Entry.query.order_by(Entry.created.desc()).all()
    else:
        all_entries = Entry.query.all()   
    return render_template('all_entries.html', title="All Entries", all_entries=all_entries)

#
@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    '''
    GET: Display form for new blog entry
    POST: create new entry or redisplay form if values are invalid
    '''
    if request.method == 'POST':
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry = Entry(new_entry_title, new_entry_body)

        if new_entry.is_valid():
            db.session.add(new_entry)
            db.session.commit()

            # display just this most recent blog entry
            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
        else:
            flash("Please check your entry for errors. Both a title and a body are required.")
            return render_template('new_entry_form.html',
                title="Create new blog entry",
                new_entry_title=new_entry_title,
                new_entry_body=new_entry_body)

    else: # GET request
        return render_template('new_entry_form.html', title="Create new blog entry")
#
if __name__ == '__main__':
    app.run()