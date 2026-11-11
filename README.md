<h1> Workshop Energy Cost Estimator </h1>
<h2> What it does</h2>
The Workshop Energy Cost Estimator is a Python program designed to calculate, monitor, and estimate the electricity consumption and operating costs of machines used in a workshop over a five-day working week (Monday to Friday).
The program allows users to enter each machine's name, power rating in watts, and daily operating hours. It then calculates the energy consumed in kilowatt-hours (kWh) and estimates the corresponding electricity cost using the user's electricity tariff.
<h2> How To Run It</h2>
Install Python 3, then run: python workshop_energy_estimator.py
<h2> Sample Output </h2>

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

  <h2> My Own Twist</h2>
  
