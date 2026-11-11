# Settings
from ast import Return


WORK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]  # list of work days
DAYS_IN_MONTH = 30      # days used to estimate monthly energy
CURRENCY = "NGN"        # currency label shown in the output


# Functions
def get_number(prompt, max_value=None):
    #Keep asking until the user types a valid number greater than 0, input is converted with float(); returns the number
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)              # convert text to a decimal number
        except ValueError:                   # user typed letters or symbols
            print("  Invalid input. Please type a number, e.g. 750 or 2.5.")
            continue
        if value <= 0:
            print("  The value must be greater than 0.")
        elif max_value is not None and value > max_value:
            print(f"  The value cannot be more than {max_value}.")
        else:
            return value                     # valid number, send it back


def calc_kwh(watts, hours):
    #Return energy in kWh: (watts x hours) / 1000."""
    return watts * hours / 1000


def check_target(day_total, target):
    #Return 'reached', 'near' (80% or more) or 'ok' for the day's usage.
    if day_total >= target:
        return "reached"
    elif day_total >= 0.8 * target:
        return "near"
    else:
        return "ok"


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


def weekly_report(week, tariff, daily_target):
    #Print the Monday-Friday report. 'week' maps each day to its machine list.
    weekly_target = daily_target * len(WORK_DAYS)
    day_totals = {}          # day -> kWh
    machine_totals = {}      # machine name -> kWh for the week
    heaviest = None          # single biggest machine-on-a-day record

    print("\n" + "=" * 50)
    print("WEEKLY REPORT (Monday - Friday)")
    print("=" * 50)

    for day in WORK_DAYS:
        total = sum(m["kwh"] for m in week[day])
        day_totals[day] = total
        status = check_target(total, daily_target)
        if status == "reached":
            note = "TARGET EXCEEDED/MET"
        elif status == "near":
            note = "close to target"
        else:
            note = "within target"
        print(f"{day:<10} {total:7.2f} kWh  {CURRENCY} {total * tariff:>10,.2f}  [{note}]")

        for m in week[day]:
            key = m["name"].lower()
            machine_totals[key] = machine_totals.get(key, 0) + m["kwh"]
            if heaviest is None or m["kwh"] > heaviest["kwh"]:
                heaviest = {"name": m["name"], "day": day, "kwh": m["kwh"]}

    weekly_total = sum(day_totals.values())
    print("-" * 50)
    print(f"Weekly usage : {weekly_total:.2f} kWh  ({CURRENCY} {weekly_total * tariff:,.2f})")
    print(f"Weekly target: {weekly_target:.2f} kWh ({daily_target} kWh x {len(WORK_DAYS)} days)")

    excess = weekly_total - weekly_target
    if excess > 0:
        print(f"Above target : {excess:.2f} kWh over ({CURRENCY} {excess * tariff:,.2f} extra)")
    else:
        print(f"Under target : {abs(excess):.2f} kWh saved")

    if weekly_total == 0 or heaviest is None:
        print("No machines were recorded this week.")
        return

    top_day = max(day_totals, key=day_totals.get)
    top_machine = max(machine_totals, key=machine_totals.get)
    print(f"Highest-usage day    : {top_day} ({day_totals[top_day]:.2f} kWh)")
    print(f"Highest-usage machine: {top_machine.title()} "
          f"({machine_totals[top_machine]:.2f} kWh this week)")
    print(f"Biggest single entry : {heaviest['name']} on {heaviest['day']} "
          f"({heaviest['kwh']:.2f} kWh)")


# Main program 
def main():
    print("=== WORKSHOP ENERGY COST ESTIMATOR ===")
    tariff = get_number(f"Enter your local tariff ({CURRENCY} per kWh): ")
    target = get_number("Set your daily energy target (kWh): ")

    week = {}                 # dictionary: day -> list of machines
    previous = []
    for day in WORK_DAYS:     # loop through Monday to Friday
        week[day] = record_day(day, tariff, target, previous)
        previous = week[day]

    weekly_report(week, tariff, target)


main()