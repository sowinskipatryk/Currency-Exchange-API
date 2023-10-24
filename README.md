# Currency Exchange API

An application designed to provide exchange rate information. 

Built-in support for two endpoints:

* /currency/ -> list of supported currencies

* /currency/USD/EUR/ -> exchange rate of a given currency pair

The startup of the application proceeds in a standard way, i.e. creating a virtual environment, pip upgrade, installing dependencies, migrating the database and starting the server.

Fetching data (via the management command): python manage.py get_exchange_rates

Testing the application: python manage.py test currency_converter.tests
