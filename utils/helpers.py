def pretty_time_delta(seconds):
    s = seconds
    seconds = round(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        p = "%d days, %d hours, %d minutes, %d seconds" % (
            days,
            hours,
            minutes,
            seconds,
        )
    elif hours > 0:
        p = "%d hours, %d minutes, %d seconds" % (hours, minutes, seconds)
    elif minutes > 0:
        p = "%d minutes, %d seconds" % (minutes, seconds)
    else:
        p = "%d seconds" % (seconds,)

    if s < 0:
        p = "-" + p
    return p
