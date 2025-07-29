import argparse
from datetime import datetime
import pytz
import tzlocal

def get_current_time(use_utc=False):
    tz = pytz.utc if use_utc else tzlocal.get_localzone()
    return datetime.now(tz)

def main():
    parser = argparse.ArgumentParser(description="Display the current time/date.")
    parser.add_argument('--utc', action='store_true', help='Show time in UTC')
    parser.add_argument('--timezone', action='store_true', help='Show the timezone name')
    parser.add_argument('--date', action='store_true', help='Show only the date')
    parser.add_argument('--time', action='store_true', help='Show only the time')

    args = parser.parse_args()
    now = get_current_time(args.utc)

    if args.date and not args.time:
        output = now.strftime("%Y-%m-%d")
    elif args.time and not args.date:
        output = now.strftime("%H:%M:%S")
    else:
        output = now.strftime("%Y-%m-%d %H:%M:%S")

    if args.timezone:
        output += f" ({now.tzname()})"

    print(output)

if __name__ == "__main__":
    main()
