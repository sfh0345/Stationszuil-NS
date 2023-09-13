print("Hoe lang ben je in meters?")
lengte = float(input())
print("Hoe zwaar ben je in KG?")
gewicht = float(input())

berekening = gewicht / (lengte ** 2)
if berekening <= 18.5:
  print("Underweight " + str(berekening))
elif berekening > 18.5 and berekening < 25.0:
  print("Normal " + str(berekening))
elif berekening > 25.0:
  print("Overweight " + str(berekening))


for