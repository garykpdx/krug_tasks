def get_daily_averages(prices):
    daily_prices = {}
    daily_counts = {}
    for day, price in prices:
        daily_prices[day] = daily_prices.get(day, 0) + price
        daily_counts[day] = daily_counts.get(day, 0) + 1

    for day in daily_prices:
        if daily_counts[day] < 3:
            daily_prices[day] = None
        else:
            daily_prices[day] = int(daily_prices[day] / daily_counts[day])
    return list(daily_prices.items())
