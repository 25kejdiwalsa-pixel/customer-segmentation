"""Create the deterministic synthetic neighborhood microgrid load dataset.

Usage: python generate_dataset.py [--output path/to/file.csv]
Only the Python standard library is required.
"""
import argparse
import csv
import math
from datetime import date, timedelta
from pathlib import Path

HEADER = ["zone_id","district_type","day_index","date","weekday","month","forecast_high_c","forecast_low_c","humidity_pct","solar_irradiance_kwh_m2","wind_kph","rain_mm","occupancy_ratio","ev_charge_share","roof_albedo_pct","tree_canopy_pct","cooling_system_age_yr","tariff_plan","community_event","peak_demand_kw"]
ZONES = [
    ("Z01","compact_urban",164,1.2,23,9,13), ("Z02","tree_rich",136,-1.1,42,43,7),
    ("Z03","industrial_edge",188,0.8,18,12,17), ("Z04","older_residential",151,0.3,27,19,21),
    ("Z05","mixed_use",158,0.2,36,28,10), ("Z06","coastal",132,-2.3,49,39,6),
    ("Z07","campus",147,0.4,39,31,8), ("Z08","suburban",139,-0.6,45,47,11),
]
def clamp(x, lo, hi):
    return max(lo, min(hi, x))
def f(x):
    return f"{x:.3f}"
def rows():
    start = date(2024, 1, 1)
    for d in range(240):
        today = start + timedelta(days=d)
        wd, month = today.weekday(), today.month
        season = math.sin(2 * math.pi * (d - 90) / 365)
        for z, (zone, district, base, offset, albedo, canopy, age) in enumerate(ZONES):
            wave = 1.4*math.sin(d*1.73+z*.81) + .9*math.cos(d*.37+z*1.9)
            high = 26+7*season+2*math.sin(d*2*math.pi/30+z*.72)+offset+wave
            if d == 132:
                high = max(high, 40.5+offset)
            low = high-7-1.2*math.cos(d*.14+z*.61)
            humidity = clamp(64-1.1*(high-20)+6*math.sin(d*.08+z*.4),20,95)
            solar = clamp(4.8+2.2*season+1.4*math.sin(d*.73+z*1.1),.1,9.8)
            if d == 191 and z == 5:
                solar = 10.4
            wind = clamp(11+6*math.sin(d*.19+z*1.2)+wave*.4,.2,38)
            rain = 2+abs(7*math.sin(d*.31+z)) if (d*3+z*5)%11 == 0 else 0.0
            if d == 212 and z == 2:
                rain = 54.0
            weekend = wd in (5,6)
            occupancy = clamp(.68+(-.12 if weekend else 0)+.04*math.sin(d*.13+z*.5)+z*.008,.32,.98)
            ev = clamp(.16+(.18 if weekend else 0)+.06*math.sin(d*.11+z*.73),.04,.6)
            tariff = ("flat","time_of_use","critical_peak")[(d+z*3)%3]
            event = int((d*7+z*11)%47 == 0)
            heat = max(high-24,0)
            tariff_adj = 0 if tariff == "flat" else (-4 if tariff == "time_of_use" else -8)
            noise = 2*math.sin(d*.91+z*.3)+1.2*math.cos(d*.23-z*.7)
            target = (base+2.4*heat+.48*max(high-33,0)**2+.22*max(humidity-50,0)
                      +2.6*solar+48*occupancy+38*ev-.4*canopy*heat/10
                      -.1*(albedo-30)*heat/10+.7*age+event*22+tariff_adj+noise)
            yield [zone,district,d,today.isoformat(),wd,month,f(high),f(low),
                   "" if (d*8+z*3)%31 == 0 else f(humidity),f(solar),
                   "" if (d*5+z*7)%37 == 0 else f(wind),
                   f(rain),"" if (d*9+z*4)%43 == 0 else f(occupancy),
                   f(ev),albedo,canopy,age,tariff,event,f(target)]
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=Path(__file__).with_name("peak_load_synthetic.csv"))
    out = ap.parse_args().output
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(HEADER)
        writer.writerows(rows())
    print(f"Wrote 1,920 deterministic synthetic rows to {out}")
if __name__ == "__main__":
    main()

