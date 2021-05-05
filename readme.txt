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

5-4-21 - Updated Product Addition Loop

5-5-21 - Multiple Updates
1 - Added functions.py
2 - added some console printing during the loops for troubleshooting purposes
3 - created loop to grab variations info and put it in a workable variable
4 - trimmed source DB table (prices we are updating from) to only contain items that are on Woocommerce
Next step is to create a table that contains both old prices and new prices and compare/update.
