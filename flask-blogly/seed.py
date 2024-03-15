'''seed database -- check if working'''

from models import User, db, Post
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

# stage & commit changes
db.session.add_all([alan, joel, jane])
db.session.commit()

db.session.add_all([post_1, post_2, post_3])
db.session.commit()

