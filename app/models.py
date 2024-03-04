import sqlalchemy as sa
import sqlalchemy.orm as so
from hashlib import md5           #biblioteca para pegar avatares para usuários
from typing import Optional
from flask_login import UserMixin #Fornece as propriedades e métodos: is_autheticated, is_active, is_anonymous e get_id()
from datetime import datetime, timezone
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

followers = sa.Table(  #Associação entre tabelas. Não é uma tabela modelo como User e Posts.
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)

class User(UserMixin, db.Model): #Herdando atributos da classe db instanciada no __init__py
    id: so.Mapped[int] = so.mapped_column(primary_key=True)     #variavel : so.Mapped[type] indica o tipo e que não pode ser um valor nulo
    username: so.Mapped[str] = so.mapped_column(sa.String(64),  #Tamanho máximo da string 
                                                index=True,     #index indica se esse dado será adicionado na coluna do db
                                                unique=True)    #unique indica se esse dado deve ser unico em relação a todos os outros no db
    email: so.Mapped[str] = so.mapped_column(sa.String(120),
                                             index=True,
                                             unique=True)
    
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))   #O Optional indica que pode ser um valor nulo
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
                                                    default=lambda: datetime.now(timezone.utc))
    posts: so.WriteOnlyMapped['Posts'] = so.relationship(back_populates='author') #so.relationship conecta as duas classes User e Post. Não faz parte direta da tabela do banco de dados
    following: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')

    def set_password(self, password):   #criptografando a senha
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  #Conferindo se a senha informada é a mesma da senha criptografada.
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def __repr__(self):
        return f'<User: {self.username}>'
    
class Posts(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    time_stamp: so.Mapped[datetime] = so.mapped_column(index=True,
                                                       default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')           #back_populates se refere ao nome da variavel que se conecta da outra classe

    def __repr__(self):
        return f'<Post: {self.body}>'
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))