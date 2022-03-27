from app import db
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Deck(db.Model):
    __tablename__ = 'deck'

    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cards = db.relationship("BaseCard")

    def __repr__(self):
        return '<id {}, name {}>'.format(self.id, self.name)

class BaseCard(db.Model):
    __tablename__ = 'basecard'

    id: int
    text: list
    created_at: datetime
    nsfw: bool

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(ARRAY(db.String()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    nsfw = db.Column(db.Boolean)
    type = db.Column(db.String(50))
    deck_id = db.Column(db.Integer, db.ForeignKey(Deck.id))

    __mapper_args__ = {
        'polymorphic_identity': 'basecard',
        'polymorphic_on': type
    }

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "created_at": str(self.created_at),
            "nsfw": self.nsfw
        }

@dataclass
class CallCard(BaseCard):
    __tablename__ = 'callcard'

    id = db.Column(db.Integer, db.ForeignKey(BaseCard.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'callcard'
    }

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "created_at": str(self.created_at),
            "nsfw": self.nsfw
        }

@dataclass
class ResponseCard(BaseCard):
    __tablename__ = 'responsecard'

    id = db.Column(db.Integer, db.ForeignKey(BaseCard.id), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'responsecard'
    }

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "created_at": str(self.created_at),
            "nsfw": self.nsfw
        }
