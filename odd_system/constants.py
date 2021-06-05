from datetime import datetime, timedelta

DATE = datetime.today().date()
# DATE = (datetime.today()+timedelta(days=1)).date()
HTML_LINK = "https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=ch&date=" + str(DATE)
WIN_JSON_LINK = "https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=" + str(DATE)