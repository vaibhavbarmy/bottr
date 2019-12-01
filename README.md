# bottr
Dependencies

pip install flask

pip install pymongo

pip install numpy

pip install -U nltk

$ python

>>> import nltk

>>> nltk.download('punkt')

>>> nltk.download('averaged_perceptron_tagger')

Load data to mongodb test collection

$ brew services start mongodb

$ python load_data.py

Reference link to resolve error in case above command doesn't work
https://stackoverflow.com/questions/23418134/cannot-connect-to-mongodb-errno61-connection-refused
https://superuser.com/questions/1478156/error-mongodb-unknown-version-mountain-lion

How to run

$ python app.py

UI interface on

http://127.0.0.1:5002/
