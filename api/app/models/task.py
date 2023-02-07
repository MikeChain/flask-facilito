from . import db

from sqlalchemy import desc, asc


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String[50], nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False,
                           default=db.func.current_timestamp())

    def __str__(self) -> str:
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline
        }

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def new(cls, title, description, deadline, **kwargs):
        return Task(title=title, description=description, deadline=deadline)

    @classmethod
    def get_by_page(cls, page, order, per_page=10):
        sort = desc(Task.id) if order == 'desc' else asc(Task.id)
        return Task.query.order_by(sort).paginate(page=page, per_page=per_page).items

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False


def insert_tasks(*args, **kwargs):
    db.session.add(
        Task(title='Title 1', description='desc',
             deadline='2023-02-06 12:00:00')
    )
    db.session.add(
        Task(title='Title 2', description='desc 2',
             deadline='2023-02-07 12:00:00')
    )

    db.session.commit()
