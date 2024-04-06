from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, func, update
from sqlalchemy.orm import relationship

from src.sql import Base


class Books(Base):
    __tablename__ = 'books'

    bookid = Column(Integer, primary_key=True)
    bookname = Column(String, nullable=False)
    numberofcopies = Column(Integer, nullable=False)

    @classmethod
    def get(cls, session, book_id):
        book = session.query(cls).filter(cls.bookid == book_id).first()
        return book

    def get_dict(self):
        return {
            'bookid': self.bookid,
            'bookname': self.bookname,
            'numberofcopies': self.numberofcopies
        }


class Members(Base):
    __tablename__ = 'members'

    memberid = Column(Integer, primary_key=True)
    membername = Column(String, nullable=False)

    @classmethod
    def get(cls, session, member_id):
        member = session.query(cls).filter(cls.memberid == member_id).first()
        return member


class EventType:
    CHECKOUT = 'checkout'
    RETURN = 'return'


class Circulation(Base):
    __tablename__ = 'circulation'

    circulationid = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    bookid = Column(Integer, ForeignKey(Books.bookid))
    memberid = Column(Integer, ForeignKey(Members.memberid))
    checkout_date = Column(Date)
    return_date = Column(Date)
    fine_amount = Column(Float)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def create(cls, **kwargs):
        circulation = Circulation()
        for key, value in kwargs.items():
            setattr(circulation, key, value)

        return circulation

    @classmethod
    def get(cls, session, **kwargs):
        circulation_query = session.query(cls)

        if kwargs.get('bookid'):
            circulation_query = circulation_query.filter(cls.bookid == kwargs.get('bookid'))

        if kwargs.get('memberid'):
            circulation_query = circulation_query.filter(cls.memberid == kwargs.get('memberid'))

        if kwargs.get('event_type'):
            circulation_query = circulation_query.filter(cls.event_type == kwargs.get('event_type'))

        if kwargs.get('empty_return_date'):
            circulation_query = circulation_query.filter(cls.return_date == None)

        return circulation_query.all()

    def get_dict(self):
        return {
            "circulationid": self.circulationid,
            "event_type": self.event_type,
            "bookid": self.bookid,
            "memberid": self.memberid,
            "checkout_date": str(self.checkout_date) if self.checkout_date else None,
            "return_date": str(self.return_date) if self.return_date else None,
            "fine_amount": self.fine_amount,
            "time_created": str(self.time_created) if self.time_created else None,
            "time_updated": str(self.time_updated) if self.time_updated else None
        }
