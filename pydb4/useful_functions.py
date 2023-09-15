from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
import pandas as pd


# convert from string into datetime object, in the given format of date (will be YYYY-mm-dd ultimately)
def convert_str_mm_dd_yyyy_to_datetime_yyyy_mm_dd(date_str):
    date_object = datetime.strptime(date_str, "%m-%d-%Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    date = datetime.strptime(formatted_date, "%Y-%m-%d")
    return date

# val has to be a datetime object, if not, then converted first using above helper function
def time_remaining_till_expiry(val):
	today = date.today()
	time_remaining = relativedelta(val.date(), today)
	return time_remaining

# df has will be pandas dataframe object, read from csv, set at 9months from now currently
# also sorts by expiry, returns new df and exported into its own csv
def find_products_by_expiry(file):
    df = pd.read_csv(file)
    df['expiry_date'] = pd.to_datetime(df['expiry_date'], format="%m-%d-%Y")
	start_date = pd.to_datetime(date.today())
	end_date = pd.to_datetime(start_date + timedelta(days=9 * 30))
	date_condition = (df["expiry_date"] >= start_date) & (df["expiry_date"] <= end_date)
	filtered_df = df[date_condition]
	filtered_df.sort_values(by="expiry_date", inplace=True)
	filtered_df.to_csv(f"products_expiry_9months_{datetime.now().date()}.csv", index=False)
	return filtered_df

# file should be csv, full path string, as in r""
def sort_products_by_name_then_expiry(file):
	df = pd.read_csv(file)
	df['expiry_date'] = pd.to_datetime(df['expiry_date'], format="%m-%d-%Y")
	product_names = df['product'].unique()
	separated_rows = []
	for product_name in product_names:
		product_df = df[df['product'] == product_name].copy()
		product_df.sort_values(by='expiry_date', inplace=True)
		# can add empty rows to increase spacing
		# separated_rows.extend({}, {}, {})
		# also adding product name as header row, can be removed if needed
		separated_rows.append({'Product': product_name})
		product_df.sort_values(by='expiry_date', inplace=True)
		separated_rows.extend(product_df.to_dict('records'))
	sorted_df = pd.DataFrame(separated_rows)
	sorted_df.to_csv(f"collated_by_products_expiry_{datetime.now().date()}.csv", index=False)



"""
additional date formatting if needed:

def convert_str_to_django_db_format_yyyy_mm_dd(date_str):
    date = datetime.strptime(date_str, "%m-%d-%Y")
    return date.strftime("%Y-%m-%d")


def convert_str_to_datetime_mm_dd_yyyy(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%m-%d-%Y")


def convert_str_to_db_search_format_yyyy_mm_dd(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date


def convert_str_mm_dd_yyyy_to_datetime_yyyy_mm_dd(date_str):
    date_object = datetime.strptime(date_str, "%m-%d-%Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    date = datetime.strptime(formatted_date, "%Y-%m-%d")
    return date


"""