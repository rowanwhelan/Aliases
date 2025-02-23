from app import app, db

with app.app_context():
    db.create_all()
    db.session.commit()
    print("Database tables created successfully!")
    tables = db.inspect(db.engine).get_table_names()
    print("Tables in database:", tables)