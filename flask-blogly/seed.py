'''seed database -- check if working'''

from models import User, db, Post, Tag, PostTag
from app import app

# (re)create all tables
db.drop_all()
db.create_all()

# seed users
alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', 
            last_name='Burton', 
            image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTupsUcDXQTtgmUy_zslO69gY7r55WNc47Ou_q0Yjaajw&s')
jane = User(first_name='Jane', last_name='Smith')

post_1 = Post(title='First Post by=Jane', content='Another One??', user_id=3)
post_2= Post(title='Second Post', content='Another One??', user_id=1)
post_3 = Post(title='Mother Father', content='Hello hi, how are you.', user_id=1)

tag_1 = Tag(name='Fantasy')
tag_2 = Tag(name='Cottagecore')
tag_3 = Tag(name='Kawaii')
tag_4 = Tag(name='Art')

pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=1, tag_id=2)
pt3 = PostTag(post_id=2, tag_id=3)
pt4 = PostTag(post_id=3, tag_id=3)

# stage & commit changes
db.session.add_all([alan, joel, jane])
db.session.commit()

db.session.add_all([post_1, post_2, post_3])
db.session.commit()

db.session.add_all([tag_1, tag_2, tag_3, tag_4])
db.session.commit()

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()

