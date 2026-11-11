# Workshop Energy Cost Estimator

> A Python command-line program that estimates the electricity use and running cost of workshop machines over a five-day working week (Monday to Friday).

**Author:** JOSEPH IDEBA, ND2 Mechatronics Engineering, YABATECH  
**Language:** Python 3
**Main file:** `JOSEPH_IDEBA_WORKSHOP_ESTIMATOR_PROJECT.py`

---

## Table of Contents

1. [What It Does](#what-it-does)
2. [Features](#features)
3. [How To Run It](#how-to-run-it)
4. [How To Use It](#how-to-use-it)
5. [How It Works](#how-it-works)
6. [Sample Output](#sample-output)
7. [My Own Twist](#my-own-twist)
8. [Testing](#testing)
9. [Future Improvements](#future-improvements)
10. [What I Learned](#what-i-learned)
11. [Author](#author)

---

## What It Does

The Workshop Energy Cost Estimator is a Python program designed to calculate, monitor, and estimate the electricity consumption and operating costs of machines used in a workshop over a five-day working week (Monday to Friday).

The program allows users to enter each machine's name, power rating in watts, and daily operating hours. It then calculates the energy consumed in kilowatt-hours (kWh) and estimates the corresponding electricity cost using the user's electricity tariff.

The core of the program is `record_day()`, which collects the machines used on one day, shows running totals, and raises the warning or alarm when the daily target is hit:

```python
def record_day(day, tariff, target, previous_machines):
    #Collect the machines used on one day. Returns a list of machine records.
    #Each record is a dictionary: name, watts, hours, kwh.
    machines = []            # list that stores this day's machines
    day_total = 0.0
    alarm_sounded = False    # so the alarm only rings once per day
    warned = False

    print(f"\n===== {day.upper()} =====")
    print("Type a machine name, or 'done' to finish the day.")
    if previous_machines:
        print("Type 'same' to reuse the machines from the previous day.")

    while True:                                  # loop until the user types 'done'
        name = input("\nMachine name: ").strip()

        if name == "":
            print("  The name cannot be empty.")
            continue
        if name.lower() == "done":
            break
        if name.lower() == "same":
            if previous_machines and not machines:
                machines = [m.copy() for m in previous_machines]
                day_total = sum(m["kwh"] for m in machines)
                print(f"  Copied {len(machines)} machine(s). Day total: {day_total:.2f} kWh")
                if check_target(day_total, target) == "reached":
                    print("\a  *** ALARM: daily target reached or exceeded! ***")
                break
            print("  'same' only works before adding machines and after day 1.")
            continue

        watts = get_number("  Power rating (watts): ")
        hours = get_number("  Hours used per day (max 24): ", max_value=24)

        kwh_day = calc_kwh(watts, hours)
        kwh_month = kwh_day * DAYS_IN_MONTH
        print(f"  Daily  : {kwh_day:.2f} kWh -> {CURRENCY} {kwh_day * tariff:,.2f}")
        print(f"  Monthly: {kwh_month:.2f} kWh -> {CURRENCY} {kwh_month * tariff:,.2f}")

        machines.append({"name": name, "watts": watts, "hours": hours, "kwh": kwh_day})
        day_total += kwh_day

        # Alarm / warning when the preset target is hit
        status = check_target(day_total, target)
        if status == "reached" and not alarm_sounded:
            print(f"\a\n  *** ALARM: target of {target} kWh reached! "
                  f"Usage so far: {day_total:.2f} kWh ***")
            alarm_sounded = True
        elif status == "near" and not warned:
            print(f"  Warning: you are above 80% of your {target} kWh target "
                  f"({day_total:.2f} kWh).")
            warned = True
        else:
            print(f"  Running total today: {day_total:.2f} / {target} kWh")

    return machines
```

## Features

| Feature | Description |
|---|---|
| Machine entry | Record any number of machines per day (name, watts, hours) |
| Energy calculation | `kWh = (watts × hours) ÷ 1000` |
| Cost estimate | Daily and monthly cost (30-day month) per machine |
| Daily target | Warning at 80% of the target, alarm at 100% |
| `same` shortcut | Reuse the previous day's machines without typing them again |
| Input checking | Rejects text, zero/negative numbers, and more than 24 hours |
| Weekly report | Per-day totals, weekly cost, target comparison, highest-usage day and machine |

## How To Run It

1. Install [Python 3](https://www.python.org/downloads/).
2. Download or clone this repository.
3. Open a terminal in the project folder and run:

```bash
python3 JOSEPH_IDEBA_WORKSHOP_ESTIMATOR_PROJECT.py
```

No extra libraries are needed.

## How To Use It

1. Enter your electricity tariff (NGN per kWh).
2. Enter your daily energy target in kWh.
3. For each day, Monday to Friday:
   - type a machine name, then its power rating (watts) and hours used,
   - repeat for each machine,
   - type `same` (from Tuesday on) to copy the previous day's machines,
   - type `done` to finish the day.
4. Read the weekly report printed at the end.

## How It Works

The program is split into small functions:

| Function | Purpose |
|---|---|
| `get_number(prompt, max_value)` | Keeps asking until the user types a valid number greater than 0 (and not above `max_value`) |
| `calc_kwh(watts, hours)` | Returns energy in kWh |
| `check_target(day_total, target)` | Returns `"reached"`, `"near"` (80% or more) or `"ok"` |
| `record_day(day, tariff, target, previous_machines)` | Collects one day's machines and shows running totals, warnings and alarms |
| `weekly_report(week, tariff, daily_target)` | Prints the Monday–Friday summary |
| `main()` | Asks for the tariff and target, loops through the week, then prints the report |

Settings you can change at the top of the file:

```python
WORK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DAYS_IN_MONTH = 30   # days used to estimate monthly energy
CURRENCY = "NGN"     # currency label shown in the output
```

Each machine is stored as a dictionary:

```python
{"name": "Welding machine", "watts": 3000, "hours": 4, "kwh": 12.0}
```

## Sample Output

Example run with a tariff of **NGN 225/kWh** and a daily target of **20 kWh**:

```text
=== WORKSHOP ENERGY COST ESTIMATOR ===
Enter your local tariff (NGN per kWh): 225
Set your daily energy target (kWh): 20

===== MONDAY =====
Type a machine name, or 'done' to finish the day.

Machine name: Welding machine
  Power rating (watts): 3000
  Hours used per day (max 24): 4
  Daily  : 12.00 kWh -> NGN 2,700.00
  Monthly: 360.00 kWh -> NGN 81,000.00
  Running total today: 12.00 / 20.0 kWh

Machine name: Drill press
  Power rating (watts): 750
  Hours used per day (max 24): 3
  Daily  : 2.25 kWh -> NGN 506.25
  Monthly: 67.50 kWh -> NGN 15,187.50
  Running total today: 14.25 / 20.0 kWh

Machine name: Angle grinder
  Power rating (watts): 1200
  Hours used per day (max 24): 2
  Daily  : 2.40 kWh -> NGN 540.00
  Monthly: 72.00 kWh -> NGN 16,200.00
  Warning: you are above 80% of your 20.0 kWh target (16.65 kWh).

Machine name: done

===== TUESDAY =====
Type a machine name, or 'done' to finish the day.
Type 'same' to reuse the machines from the previous day.

Machine name: same
  Copied 3 machine(s). Day total: 16.65 kWh

...

==================================================
WEEKLY REPORT (Monday - Friday)
==================================================
Monday       16.65 kWh  NGN   3,746.25  [close to target]
Tuesday      16.65 kWh  NGN   3,746.25  [close to target]
Wednesday    16.65 kWh  NGN   3,746.25  [close to target]
Thursday     11.00 kWh  NGN   2,475.00  [within target]
Friday       11.00 kWh  NGN   2,475.00  [within target]
--------------------------------------------------
Weekly usage : 71.95 kWh  (NGN 16,188.75)
Weekly target: 100.00 kWh (20.0 kWh x 5 days)
Under target : 28.05 kWh saved
Highest-usage day    : Monday (16.65 kWh)
Highest-usage machine: Welding Machine (36.00 kWh this week)
Biggest single entry : Welding machine on Monday (12.00 kWh)
```

## My Own Twist

<!-- Describe what you added beyond the basic brief. Suggested points from the code: -->

- **Daily target alarm:** the user sets a daily kWh limit. The program warns once at 80% and sounds an alarm (`\a`) once the limit is reached.
- **`same` shortcut:** copies the previous day's machines, so a workshop with the same routine doesn't have to type everything five times.
- **Weekly insights:** the report names the highest-usage day, the machine that used the most energy over the week, and the biggest single entry.

_Why I added this:_ _(write 1–2 sentences here)_

## Testing

| Test | Input | Expected result | Passed? |
|---|---|---|---|
| Text instead of a number | `abc` for watts | "Invalid input" message, asks again | ☐ |
| Zero or negative value | `0` or `-5` | "must be greater than 0", asks again | ☐ |
| Too many hours | `30` hours | "cannot be more than 24", asks again | ☐ |
| Empty machine name | (press Enter) | "name cannot be empty" | ☐ |
| `same` on Monday | `same` | "'same' only works ... after day 1" | ☐ |
| Reach 80% of target | 16 kWh of 20 | Warning shown once | ☐ |
| Reach target | 20+ kWh of 20 | Alarm shown once | ☐ |
| No machines all week | `done` every day | "No machines were recorded this week." | ☐ |

## Future Improvements

- [ ] Save the weekly report to a `.txt` or `.csv` file
- [ ] Let the user choose the number of working days
- [ ] Compare this week with last week
- [ ] Add a simple chart of daily usage

## What I Learned

1. **Breaking a problem into functions:** splitting the program into small functions (`get_number`, `calc_kwh`, `check_target`, `record_day`, `weekly_report`) made each part easier to write, test and fix on its own.
2. **Handling user input safely:** using `try`/`except` and loops to reject bad input taught me that a program has to expect mistakes from the user and recover without crashing.

## Author

**JOSEPH IDEBA**  
ND2 Mechatronics Engineering  
Yaba College of Technology (YABATECH)
