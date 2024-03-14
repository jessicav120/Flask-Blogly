'''seed database -- check if working'''

from models import User, db
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

# stage & commit changes
db.session.add_all([alan, joel, jane])
db.session.commit()

