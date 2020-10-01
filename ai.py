import tensorflow as tf
import datetime as dt
import numpy as np

try:
    from .csv_convert import ov_card
except ImportError:
    from csv_convert import ov_card








if __name__ == "__main__":
    print(ov_card)
    dataset = []
    for (i,t) in enumerate(ov_card):
        date_parts = [int(i) for i in t['Datum'].split('-')]
        date = dt.datetime(date_parts[2], date_parts[1], date_parts[0])
        weekday = print(date.isoweekday())
        if len(t["Check-in"]) > 0:
            print(t["Check-in"])
        
        checkout_parts = [0, 0]
        check_out = None
        if len(t["Check-uit"]) > 0:
            checkout_parts = [int(i) for i in  t["Check-uit"].split(":")]
            check_out = dt.datetime(date_parts[2], date_parts[1], date_parts[0], checkout_parts[0], checkout_parts[1])
        dataset.append(
            {
                "day_of_week": date.isoweekday(),
                "minutes_of_day": checkout_parts[0] * 60 + checkout_parts[1]
            }
        )
    dataset = np.array([list(d.values()) for d in dataset])
    tf.keras.models.Sequential(
        
    )

        
        

        



