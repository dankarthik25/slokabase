from flask import render_template, url_for, flash, redirect
from slokabase import app, db
from slokabase.forms import RegistrationForm, LoginForm, SongIndex, Song_Details
from slokabase.models import User, Post

sloka_no = 'Bg.1.1'
devanagari_text = ["धृतराष्ट्र उवाच","धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सव: ।","मामका: पाण्डवाश्चैव किमकुर्वत सञ्जय ॥ १ ॥"]
iskcon_font = ["dhṛtarāṣṭra uvāca","dharma-kṣetre kuru-kṣetre","samavetā yuyutsavaḥ","māmakāḥ pāṇḍavāś caiva","kim akurvata sañjaya"]
synonyms= {
    "dhṛtarāṣṭraḥ uvāca" :"King Dhṛtarāṣṭra said", "dharma-kṣetre": "in the place of pilgrimage", "kuru-kṣetre" :  "in the place named Kurukṣetra",
    "samavetāḥ" : "assembled","yuyutsavaḥ" : "desiring to fight","māmakāḥ":"my party (sons)","pāṇḍavāḥ ":" the sons of Pāṇḍu",
    "ca ":" and","eva ":" certainly","kim ":" what","akurvata ":" did they do","sañjaya ":" O Sañjaya"
} 

translation = "Dhṛtarāṣṭra said: O Sañjaya, after my sons and the sons of Pāṇḍu assembled in the place of pilgrimage at Kurukṣetra, desiring to fight, what did they do?"
purpot = """Bhagavad-gītā is the widely read theistic science summarized in the Gītā-māhātmya (Glorification of the Gītā). There it says that one should read Bhagavad-gītā very scrutinizingly with the help of a person who is a devotee of Śrī Kṛṣṇa and try to understand it without personally motivated interpretations. The example of clear understanding is there in the Bhagavad-gītā itself, in the way the teaching is understood by Arjuna, who heard the Gītā directly from the Lord. If someone is fortunate enough to understand the Bhagavad-gītā in that line of disciplic succession, without motivated interpretation, then he surpasses all studies of Vedic wisdom, and all scriptures of the world. One will find in the Bhagavad-gītā all that is contained in other scriptures, but the reader will also find things which are not to be found elsewhere. That is the specific standard of the Gītā. It is the perfect theistic science because it is directly spoken by the Supreme Personality of Godhead, Lord Śrī Kṛṣṇa."""
posts = {
    'sloka_no': sloka_no,
    'devanagari_text' : devanagari_text,
    'iskcon_font' : iskcon_font,
    'synonyms' : synonyms,
    'translation' : translation,
    'purpot' : purpot
}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts,)


# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/editor",methods=['GET', 'POST'])
def editor():
    form = SongIndex()
    print(form)
    if form.validate_on_submit():
        song_idx = SongIndex(song_name=form.song_name.data, 
                             song_short_name=form.song_short_name.data, 
                             division=form.division.data, 
                             division_no=form.division_no.data, 
                             sloka_statues=form.sloka_statues.data, 
                             total_slokas= form.total_slokas.data, 
                             group = form.group.data, 
                             devotion=form.devotion_god.data, 
                             author = form.author.data, 
                             describtion = form.describtion.data, 
                             other_link = form.other_links.data)
        print('adsfasd')
        print(song_idx.song_name)
        db.session.add(song_idx)
        db.session.commit()

        flash(f'Song created for {form.song_name.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('editor.html', title='Editor',form=form)
