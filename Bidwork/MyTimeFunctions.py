import datetime

def MyCurrentTime():
	TimeZone_Offset = -5
	Current_DateTime=datetime.datetime.now()+datetime.timedelta(hours = TimeZone_Offset)
	return Current_DateTime

def setWeekStartDay(Week_Number):
	start_date = "2019-12-29"	
	date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
	offset = ((Week_Number-1) * 7)
	date2 = date_1 + datetime.timedelta(days = int(offset))
	return date2	