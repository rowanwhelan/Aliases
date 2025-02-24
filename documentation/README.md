# Common Questions:

### How do I setup the enviornment?
```powershell 
conda env create -f environment.yml
conda activate wordgame-env
```

### How do I setup the database?
```powershell
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```