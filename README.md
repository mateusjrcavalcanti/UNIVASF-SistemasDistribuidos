# Django

```console
..\.venv\Scripts\Activate.ps1
```

```python
pip install -r requirements.txt
django-admin startproject django_tcc .
python manage.py startapp tcc
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py flush
```

```python
python3 manage.py dumpdata auth.group --indent 4 > project/seed/0001_Group.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0002_User.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0003_Curso.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0004_Semestre.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0005_Horario.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0006_Trabalho.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0007_Banca.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0008_Avaliacao.json
python3 manage.py dumpdata tcc --indent 4 > project/seed/0009_Resultado.json

python manage.py loaddata django_tcc/seed/*.json
```
