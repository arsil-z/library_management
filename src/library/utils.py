import datetime
import logging

from sqlalchemy.exc import SQLAlchemyError

from src.library.models import Circulation, EventType, Members, Books
from src.sql import Session


def circulation_helper(circulation_data):

    response_data = []
    for circulation in circulation_data:
        event_type = circulation.get('eventtype')
        if event_type == EventType.CHECKOUT:
            book = checkout_helper(circulation)
            response_data.append({
                'circulation': circulation,
                **book
            })
        elif event_type == EventType.RETURN:
            book = return_helper(circulation)
            return_helper(circulation)
            response_data.append({
                'circulation': circulation,
                **book
            })
        else:
            raise ValueError(f'Invalid event type: {event_type}')
    return response_data


def checkout_helper(circulation):
    """
    {
        "eventtype": "checkout",
        "book_id": 1000,
        "member_id": 2003,
        "date": "2023-05-10"
    }
    . Check if the member exists
    . Check if the same book is already checked out by the same member
    . Subtract the numberofcopies in books table by 1 and see if the count is >= 0
    . Create entry in Circulation table for the checked out book
    . Return the book
    """
    book_id = circulation.get('book_id')
    member_id = circulation.get('member_id')
    date = circulation.get('date')
    circulation_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    with Session() as session:
        member = Members.get(session=session, member_id=member_id)
        if not member:
            return {'error': 'Member not found'}

        existing_circulation = Circulation.get(
            session=session, bookid=book_id, memberid=member_id, event_type=EventType.CHECKOUT,
            empty_return_date=True
        )
        if existing_circulation:
            return {'error': 'Book already taken by the user'}

        book = Books.get(session=session, book_id=book_id)
        if not book or book.numberofcopies <= 0:
            return {'error': 'Book not available'}

        circulation = Circulation.create(
            event_type=EventType.CHECKOUT, bookid=book_id, memberid=member_id,
            checkout_date=circulation_date.date()
        )

        book.numberofcopies -= 1

        try:
            session.add_all([book, circulation])
            session.commit()
            return {'book': book.get_dict()}
        except SQLAlchemyError as err:
            logging.info(f'Error in checkout_helper commit: {err}')
            session.rollback()
            return {'error': 'Something went wrong'}


def return_helper(circulation):
    """
    {
        "eventtype": "return",
        "book_id": 1000,
        "member_id": 2013,
        "date": "2023-05-22"
    }
    . Get the entry from circulation table
    . Mark return_date
    . Increase numberofcopies count
    :param circulation:
    :return:
    """
    book_id = circulation.get('book_id')
    member_id = circulation.get('member_id')
    date = circulation.get('date')
    circulation_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    with Session() as session:
        existing_circulation = Circulation.get(
            session=session, bookid=book_id, memberid=member_id, empty_return_date=True,
            event_type=EventType.CHECKOUT
        )
        if existing_circulation:
            existing_circulation = existing_circulation[0]
        else:
            return {'error': 'Circulation does not exists'}

        existing_circulation.return_date = circulation_date.date()
        existing_circulation.event_type = EventType.RETURN
        book = Books.get(session=session, book_id=book_id)
        book.numberofcopies += 1

        try:
            session.add_all([existing_circulation, book])
            session.commit()
            return {'book': book.get_dict()}
        except SQLAlchemyError as err:
            logging.info(f'Error in checkout_helper commit: {err}')
            session.rollback()
            return {'error': 'Something went wrong'}


def member_stats_helper(member_id):
    with Session() as session:
        circulations = Circulation.get(
            session=session, memberid=member_id, empty_return_date=True
        )
        over_due_data = []
        for circulation in circulations:
            circulation_over_due_data = overdue_and_fine_helper(circulation)
            if circulation_over_due_data:
                over_due_data.append(circulation_over_due_data)
    return over_due_data


def overdue_and_fine_helper(circulation):
    checkout_date = circulation.checkout_date
    calculating_date = datetime.date(year=2023, month=5, day=31)

    book_hold_days = (calculating_date - checkout_date)
    book_hold_days = book_hold_days.days

    if book_hold_days > 7:
        over_due_days = book_hold_days - 7

    return