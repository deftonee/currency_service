1. Set environment variable DB_CONNECTION containing empty database address
Example: postgresql://localhost:5432/currency_service

2. Run server:
python app.py

3. Collect rates data from https://api-pub.bitfinex.com
http://0.0.0.0:8080/fetch

4. Show currencies (default page size is 5)
http://0.0.0.0:8080/currencies

5. Show currencies with certain page size and/or page number
http://0.0.0.0:8080/currencies?page_size=2&page=3

6. Show rate and average trading volume for last 10 days for given currency id
http://0.0.0.0:8080/rates/3
