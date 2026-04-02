import rx

# Publish some fake temperature readings
xs = rx.from_iterable(range(10))

# Subscribe with on_next, on_error, and on_completed callbacks
def on_next(x):
    print("Temperature is: %s degrees centigrade" % x)
    if x > 6:
        print("Warning: Temperate Is Exceeding Recommended Limit")
    if x == 9:
        print("DataCenter is shutting down. Temperature is too high")

def on_error(e):
    print("Error: %s" % e)

def on_completed():
    print("All Temps Read")

xs.subscribe(on_next=on_next, on_error=on_error, on_completed=on_completed)
