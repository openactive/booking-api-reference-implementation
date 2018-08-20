export FLASK_APP=main.py
export FLASK_DEBUG=1
rm -rf local_data
mkdir local_data
cd local_data
mkdir events
mkdir offers
mkdir orders
cd ..
python manage.py
flask run
