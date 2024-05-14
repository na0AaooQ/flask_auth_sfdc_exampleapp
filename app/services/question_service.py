from app import db
from app.models.question import Question
from sqlalchemy.exc import SQLAlchemyError

def find_all() -> [Question]:
    return Question.query.all()


def find_one(question_id: int) -> Question:
    if question_id is None:
        raise Exception
    return Question.query.filter_by(id=question_id).first()


def save(question_id: int, user_id: int, data: {}) -> Question:
    try:
        if question_id is None:
            question = Question.from_args(
                data.get('title'),
                data.get('body'),
                user_id
            )
            db.session.add(question)
        else:
            question = find_one(question_id)
            question.title = data.get('title')
            question.body = data.get('body')
            question.user_id = user_id
        db.session.commit()
        return question
    except SQLAlchemyError:
        raise Exception

def delete(question_id: int) -> bool:
    if question_id is None:
        raise Exception
    try:
        question = find_one(question_id)
        db.session.delete(question)
        db.session.commit()
        return True
    except SQLAlchemyError:
        raise Exception

def find_sfdc_data() -> str:
    return Question.find_sfdc_data()

def find_sfdc_data_id(question_id: int) -> str:
    return Question.find_sfdc_data_id(question_id)

def find_sfdc_search_data(id: int) -> str:
    return Question.find_sfdc_search_data(id)

def sfdc_data_update(id: int, name: str) -> str:
    return Question.sfdc_data_update(id, name)

def sfdc_data_create(name: str, phone: str) -> str:
    return Question.sfdc_data_create(name, phone)

def sfdc_data_delete(id: int) -> str:
    print(id)
    return Question.sfdc_data_delete(id)
