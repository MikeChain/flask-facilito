from . import db

from sqlalchemy.event import listen

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
