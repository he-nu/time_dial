from main_modules.sun_moon_dial import TimeDial

if __name__ == "__main__":
    dial = TimeDial()
    dial.animate(
        iterations=3,
        print_lag=0.2
    )