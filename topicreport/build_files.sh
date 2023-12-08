mkdir static -p
mkdir staticfiles_build -p
mkdir staticfiles_build/static -p
pip install -r ./requirements.txt
python3.9 manage.py collectstatic --noinput

