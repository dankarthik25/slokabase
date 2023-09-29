# from datetime import datetime
# # from slokabase import db


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
#     password = db.Column(db.String(60), nullable=False)
#     posts = db.relationship('Post', backref='author', lazy=True)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#         # `db.create_all()
#         # from slokabase import User, Post
#         # user_1 = User(username='Corey', email ='C@demo.com', password = 'password')
#         # db.session.add(user_1)

#         # user_2 = User(username='kCorey', email ='kC@demo.com', password = 'password')
#         # db.session.add(user_2)

#         # db.session.commit()

#         # User.query.all()

#         # User.query.filter_by(username='Cory')

#         # filter_user = User.query.filter_by(username='Cory').first()
#         # filter_user.id

#         # get_user = User.query.get(filter.user.id)


#         # db.drop_all()
#         # db.create_all()



# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"
    
# class SongIdx(db.Model):
#     song_idx        = db.Column(db.Integer, primary_key=True)
#     song_name       = db.Column(db.String(100), unique=True,  nullable=False)
#     song_short_name = db.Column(db.String(100),unique=True,  nullable=False)
#     division        = db.Column(db.String(100),  ) # nullable=False)
#     division_no     = db.Column(db.String(100),) #   nullable=False)
#     sloka_statues   = db.Column(db.String(100),) #   nullable=False)
#     total_slokas    = db.Column(db.Integer, ) #  nullable=False)
#     group           = db.Column(db.String(100), ) #  nullable=False)
#     devotion_god    = db.Column(db.String(100),) #   nullable=False)
#     author          = db.Column(db.String(100), ) #  nullable=False)
#     describtion     = db.Column(db.Text, ) #  nullable=False)
#     other_links     = db.Column(db.Text, ) #  nullable=False)

#     def __repr__(self):
#         return f"SongIdx('{self.song_idx}','{self.song_name}','{self.song_short_name}' '{self.division}' '{self.division_no}' '{self.sloka_statues}')"




