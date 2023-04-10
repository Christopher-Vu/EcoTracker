import math

def goods(clothing, electronics, furniture, other):
    # input in 1000s of dollars spent, output as tons of CO2
    return (clothing / 1000 * 1.2) + (2.8 / 1000 * electronics) + (2.2 / 1000 * furniture) + (2.12 / 1000 * other)

def food(beef, meat, other):
    # input as kg of food, output as tons of CO2
    return (beef * 0.0292112497) + (0.004 * meat) + (other * 0.0011)

def water(bill, cpg): #cpg is cost per gallon
    return 0.000043532215 * (bill / cpg)

def energy(bill, cpkwh, clean_percentage): #cpkwh is the cost per kwh of electricity, clean_percentage is how much of it was clean energy (as a whole #)
    return (bill / cpkwh) * 0.00043532 * (1 - (clean_percentage / 100))

def transport(Dmiles, Dmpg, Gmiles, Gmpg, flight_hours, transit_miles): # the D prefix meand on diesel, G means on gasoline
    Dtons, Gtons = 0, 0
    if Dmpg: Dtons = 0.011741 * (Dmiles / Dmpg)
    if Gmpg: Gtons = 0.011741 * 0.87 / (Gmiles / Gmpg)
    flight_tons = flight_hours * 0.099208
    transit_tons = transit_miles * 0.00022526
    return Dtons + Gtons + flight_tons + flight_hours

def avg_footprint(people, annual_income):
    return (math.log10(people + 1) + 0.7) * (21.4104 + (annual_income * 0.000322351))