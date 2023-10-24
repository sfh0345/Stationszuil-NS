from locatie import firsttimeinstall

varstad = firsttimeinstall()
#pak de var van firsttimeinstall

if varstad is not None:
    station = varstad
    #station is firsttimeinstall return
else:
    station = firsttimeinstall()
    #omweg omdat het eerst none geeft op de eerste run. dus nu run je het gewoon een 2e keer als het de eerste is.