def should_exclude(price, count):
    # separate exclusion logic from averaging
    return count >= 3


def get_daily_averages(prices):
    # [(date(2016, 1, 1), 1383), (date(2016, 1, 2), 1383)]
    daily_prices = {}
    daily_counts = {}
    for day, price in prices:
        daily_prices[day] = daily_prices.get(day, 0) + price
        daily_counts[day] = daily_counts.get(day, 0) + 1

    for day in daily_prices:
        if should_exclude(daily_prices[day], daily_counts[day]):
            daily_prices[day] = None
        else:
            daily_prices[day] = daily_prices[day] / daily_counts[day]

    return daily_prices