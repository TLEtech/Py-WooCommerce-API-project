# a = SQL results, b = ItemIDList
# function to create a list of ItemIDs from SQL query that match items from WooCommerce
def trim_sql_results(a, b):
    result_list = []
    for sql_item in a:
        if sql_item['ItemID'] in b:
            result_list.append(sql_item)
    return result_list

