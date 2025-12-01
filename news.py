from datetime import datetime

moscow_times_date = "Wednesday, October 2, 2002"
moscow_times_format = "%A, %B %d, %Y"
datetime1 = datetime.strptime(moscow_times_date, moscow_times_format)
print(f"The Moscow Times: {datetime1}")

guardian_date = "Friday, 11.10.13"
guardian_format = "%A, %d.%m.%y"  # запятая после %A
datetime2 = datetime.strptime(guardian_date, guardian_format)
print(f"The Guardian: {datetime2}")

daily_news_date = "Thursday, 18 August 1977"
daily_news_format = "%A, %d %B %Y"
datetime3 = datetime.strptime(daily_news_date, daily_news_format)
print(f"Daily News: {datetime3}")
