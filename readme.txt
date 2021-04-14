This is very much a work in progress.

Goal is to connect our custom CRM and legacy ERP to our more
modern WooCommerce site. First goal is to auto update prices based
on preset parameters and up-to-date information

Log:

4-8-21 - Began repo.
Callback URL is not returning tokens, even though it returns a successful authorization,
and the keys appear in the API Keys page.

4-9-21 - Auth successful
Successful OAuth1 authentication achieved. Successfully managed to update prices on a test run.
Next step is to work on grabbing local data and comparing it to remote data.

4-14-21 - Beginning DB Connection
Beginning DB connection phase of this project. Created data.py for DB connection and queries.
Beginning work on loops for price update automation (still very messy, needs cleanup)