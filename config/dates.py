# Default timezone and date formatting
# Also, if you want to use a different time zone in some of your posts,
# you can use the ISO 8601/RFC 3339 format (ex. 2012-03-30T23:00:00+02:00)
TIMEZONE = "America/Toronto"
# FORCE_ISO8601 = False # does not affect DATE_FORMAT even if True
# Date format used to display post dates. (translatable)
# Used by babel.dates, CLDR style: 
# http://cldr.unicode.org/translation/date-time-1/date-time
# You can also use 'full', 'long', 'medium', or 'short'
# DATE_FORMAT = 'yyyy-MM-dd HH:mm'
# LUXON_DATE_FORMAT = {
#     DEFAULT_LANG: {'preset': False, 'format': 'yyyy-MM-dd HH:mm'},
# }
# 0 = using DATE_FORMAT and TIMEZONE (without JS)
# 1 = using LUXON_DATE_FORMAT and local user time (JS, using Luxon)
# 2 = using a string like “2 days ago” (JS, using Luxon)
# Your theme must support it, Bootstrap already does.
# DATE_FANCINESS = 0
