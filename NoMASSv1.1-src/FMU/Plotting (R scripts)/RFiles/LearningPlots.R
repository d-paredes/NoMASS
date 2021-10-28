
agent <- read.csv("~/git/results/learn/agent0000.csv")

plot(agent$Weekday.1._action0[48:96]+10, type="l", ylim=c(-3,30))
lines(agent$Weekday.1._state0[48:96], type="l",col="red")
lines(agent$Weekday.1._reward0[48:96], type="l",col="blue")
lines(agent$Weekday.1._steps0[48:96], type="l",col="green")
lines(agent$Weekday.1._pmv0[48:96], type="l",col="brown")



plot(agent$Agent_pmv_0[0:400], type="l", ylim=c(-5,30))
lines(agent$Agent_PMV_meanRadient0[0:400], type="l",col="red")
lines(agent$Agent_PMV_airTemp0[0:400], type="l",col="blue")

par(mfrow=c(2,1))
timestep <- read.csv("~/git/results/learn/timestep0000.csv")
plot(timestep$BLOCK1.ZONE1.Zone.Mean.Air.Temperature..C..TimeStep., type="l", ylim=c(-5,30))
lines(timestep$BLOCK1.ZONE1.Zone.People.Occupant.Count....TimeStep., type="l",col="red")
lines(timestep$BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep., type="l",col="blue")


par(mar=c(3,5,1,2)+0.1)

par(mfrow=c(2,2))
timestep <- read.csv("~/git/results/learn/timestep0001.csv")

plot(timestep$BLOCK1.ZONE1.Zone.Mean.Air.Temperature..C..TimeStep., type="l", ylim=c(-5,30))
lines(timestep$BLOCK1.ZONE1HEATING.Schedule.Value....TimeStep., col="orange")
plot(timestep$BLOCK1.ZONE1.Zone.Mean.Radiant.Temperature..C..TimeStep., type="l", col="orange")
plot(timestep$BLOCK1.ZONE1.Zone.Air.Relative.Humidity.....TimeStep., type="l", col="red")
plot(timestep$BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep., type="l", col="red")
sum(timestep$BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)
mean(timestep$BLOCK1.ZONE1.Zone.Mean.Radiant.Temperature..C..TimeStep.)

timestep <- read.csv("~/git/results/det/timestep0002.csv")

plot(timestep$BLOCK1.ZONE1.Zone.Mean.Air.Temperature..C..TimeStep., type="l", ylim=c(-5,30))
lines(timestep$BLOCK1.ZONE1HEATING.Schedule.Value....TimeStep., col="orange")
plot(timestep$BLOCK1.ZONE1.Zone.Mean.Radiant.Temperature..C..TimeStep., type="l", col="orange")
plot(timestep$BLOCK1.ZONE1.Zone.Air.Relative.Humidity.....TimeStep., type="l", col="red")
plot(timestep$BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep., type="l", col="red")
sum(timestep$BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep.)
mean(timestep$BLOCK1.ZONE1.Zone.Mean.Radiant.Temperature..C..TimeStep.)


lines(timestep$BLOCK1.ZONE1.Zone.Thermostat.Heating.Setpoint.Temperature..C..TimeStep., col="orange")
lines(timestep$BLOCK1.ZONE1.Zone.People.Occupant.Count....TimeStep., type="l",col="red")
lines(timestep$BLOCK1.ZONE1_WALL_5_0_0_0_0_0_WIN.AFN.Surface.Venting.Window.or.Door.Opening.Factor....TimeStep., type="l",col="blue")
lines(timestep$Environment.Site.Outdoor.Air.Drybulb.Temperature..C..TimeStep., type="l",col="green")

plot(timestep$BLOCK1.ZONE1.Zone.Total.Internal.Total.Heating.Energy..J..TimeStep., type="l",col="green")
lines(timestep$BLOCK1.ZONE1.Zone.Air.System.Sensible.Cooling.Energy..J..TimeStep., type="l",col="red")
lines(timestep$BLOCK1.ZONE1.Zone.Total.Internal.Convective.Heating.Energy..J..TimeStep., type="l",col="blue")
lines(timestep$BLOCK1.ZONE1.Zone.Total.Internal.Radiant.Heating.Energy..J..TimeStep., type="l",col="orange")

plot(timestep$PEOPLE.BLOCK1.ZONE1.Zone.Thermal.Comfort.Fanger.Model.PPD.....TimeStep., type="l",col="green")
