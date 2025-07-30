# Static helper functions
def is_leap_year(year):
    """Gregorian-compatible leap year calculation"""
    if year % 4 != 0:
        return False
    if year % 100 != 0:
        return True
    return year % 400 == 0

def gregorian_days_in_month(year, month):
    """Days per month in Gregorian calendar"""
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return 30 if month in [4, 6, 9, 11] else 31

def gregorian_to_jd(year, month, day, hour, minute, second):
    """Convert Gregorian date to Julian Day (from scratch)"""
    # Base JD for 0001-01-01 00:00:00
    base_jd = 1721425.0
    
    # Days from year 1 to current year-1
    total_days = (year - 1) * 365
    total_days += (year - 1) // 4
    total_days -= (year - 1) // 100
    total_days += (year - 1) // 400
    
    # Days in current year
    month_days = 0
    for m in range(1, month):
        month_days += gregorian_days_in_month(year, m)
    year_days = month_days + day - 1
    
    # Time fraction
    total_seconds = hour * 3600 + minute * 60 + second
    fraction = total_seconds / 86400.0
    
    return base_jd + total_days + year_days + fraction

# Main Calendar Class
class ThirteenCalendar:
    JD_EPOCH = 1721425.0  # Julian Day for 0001-01-01 00:00:00
    
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month  # 0=extra, 1-13=regular
        self.day = day
        self.hour = hour    # 0-25
        self.minute = minute  # 0-99
        self.second = second  # 0-99
    
    @property
    def is_leap(self):
        return is_leap_year(self.year)
    
    def day_of_year(self):
        """Calculate day of year (1-366)"""
        if self.month == 0:  # Extra days
            return 364 + self.day
        return (self.month - 1) * 28 + self.day
    
    def weekday(self):
        """Calculate weekday (0-7) with continuous 8-day cycles"""
        # Years since epoch
        total_years = self.year - 1
        
        # Leap days in prior years
        leap_days = total_years // 4 - total_years // 100 + total_years // 400
        
        # Total days since epoch
        total_days = total_years * 365 + leap_days + self.day_of_year() - 1
        return int(total_days % 8)
    
    def era_info(self):
        """Calculate era and year within era"""
        era = (self.year - 1) // 13 + 1
        year_in_era = (self.year - 1) % 13 + 1
        return era, year_in_era
    
    def to_julian_day(self):
        """Convert to Julian Day for astronomical calculations"""
        # Days in prior years
        total_years = self.year - 1
        leap_days = total_years // 4 - total_years // 100 + total_years // 400
        total_days = total_years * 365 + leap_days + self.day_of_year() - 1
        
        # Time fraction (26-hr clock)
        total_sec = self.hour * 10000 + self.minute * 100 + self.second
        day_fraction = total_sec / 260000.0
        
        return self.JD_EPOCH + total_days + day_fraction
    
    @classmethod
    def from_gregorian(cls, year, month, day, hour, minute, second):
        """Convert from Gregorian date"""
        # Get Julian Day
        jd = gregorian_to_jd(year, month, day, hour, minute, second)
        base_jd = jd - cls.JD_EPOCH
        
        # Extract full days and fraction
        total_days = int(base_jd)
        fraction = base_jd - total_days
        
        # Calculate year
        year_val = 1
        days_left = total_days
        while days_left >= (366 if is_leap_year(year_val) else 365):
            days_in_year = 366 if is_leap_year(year_val) else 365
            days_left -= days_in_year
            year_val += 1
        
        # Calculate date components
        doy = days_left + 1  # Day of year (1-based)
        
        # Month/day calculation
        if doy <= 364:
            month_val = (doy - 1) // 28 + 1
            day_val = (doy - 1) % 28 + 1
        else:
            month_val = 0
            day_val = doy - 364
        
        # Time conversion (24hr -> 26hr)
        total_si_sec = fraction * 86400
        new_sec_total = total_si_sec * (260000 / 86400)
        hour_val = int(new_sec_total // 10000) % 26
        rem = new_sec_total % 10000
        min_val = int(rem // 100)
        sec_val = int(rem % 100)
        
        return cls(year_val, month_val, day_val, hour_val, min_val, sec_val)
    
    def __str__(self):
        """Human-readable representation"""
        # Date components
        if self.month == 0:
            date_str = f"Year {self.year}, Intercalary Day {self.day}"
        else:
            date_str = f"Year {self.year}, Month {self.month}, Day {self.day}"
        
        # Weekday
        weekdays = ["Sol", "Luna", "Terra", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
        weekday_str = weekdays[self.weekday()]
        
        # Era info
        era, year_in_era = self.era_info()
        era_str = f"Era {era}, Year {year_in_era}/13"
        
        # Time
        time_str = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        
        return f"{date_str} | {weekday_str} | {era_str} | {time_str}"

# Example usage
if __name__ == "__main__":
    # Convert current date (2025-07-09 ~12:00 UTC)
    custom_date = ThirteenCalendar.from_gregorian(2025, 7, 9, 12, 0, 0)
    print("Current DateTime:\n", custom_date)
    print("Julian Day:", custom_date.to_julian_day())
    
    # Test leap year handling
    leap_test = ThirteenCalendar.from_gregorian(2024, 12, 31, 23, 59, 59)
    print("\nLeap Year Test:\n", leap_test)
    print("Julian Day:", leap_test.to_julian_day())