// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef MODEL_WINDOWS_H
//#define MODEL_WINDOWS_H
#ifndef MODEL_WINDOWS_HPP_
#define MODEL_WINDOWS_HPP_

#include <Models/Model_RandomWeibull.hpp>

//**********************************************************************

/**
 * @brief Models occupant window openings
 * @details Models occupant window openings adapted from
 * \n Haldi, F., & Robinson, D. (2009). Interactions with window openings by office occupants. Building and Environment, 44(12), 2378–2395. https://doi.org/10.1016/j.buildenv.2009.03.025
 */

//**********************************************************************

class Model_Windows : public Model_RandomWeibull
    {
    public:
        Model_Windows();

        void setWindowState(bool windowState);
        bool getWindowState() const;
        void setDurationOpen(int durationOpen);
        int getDurationOpen() const;

        void arrival(double indoorTemperature, double outdoorTemperature, double previousDuration, bool rain, int timeStepLengthInMinutes );
        void intermediate(double indoorTemperature, double outdoorTemperature, double currentDuration, bool rain, int timeStepLengthInMinutes);
        void departure(double indoorTemperature, double dailyMeanTemperature, double futureDuration, double groundFloor);

        void setDurationVars(double aop, double bopout, double shapeop);
        void setArrivalVars(double a01arr, double b01inarr, double b01outarr, double b01absprevarr, double b01rnarr);
        void setInterVars(double a01int, double b01inint, double b01outint, double b01presint, double b01rnint);
        void setDepartureVars(double a01dep, double b01outdep, double b01absdep, double b01gddep, double a10dep, double b10indep, double b10outdep, double b10absdep, double b10gddep);

        double getAop() const;
        double getBopout() const;
        double getshapeop() const;

        double getA01arr() const;
        double getB01inarr() const;
        double getB01outarr() const;
        double getB01absprevarr() const;
        double getB01rnarr() const;
        // P01int
        double getA01int() const;
        double getB01inint() const;
        double getB01outint() const;
        double getB01presint() const;
        double getB01rnint() const;
        // P01dep
        double getA01dep() const;
        double getB01outdep() const;
        double getB01absdep() const;
        double getB01gddep() const;
        // P10dep
        double getA10dep() const;
        double getB10indep() const;
        double getB10outdep() const;
        double getB10absdep() const;
        double getB10gddep() const;

    private:
        bool state;
        int durationOpen;

        double aop;
        double bopout;
        double shapeop;

        double a01arr;
        double b01inarr;
        double b01outarr;
        double b01absprevarr;
        double b01rnarr;
        // P01int
        double a01int;
        double b01inint;
        double b01outint;
        double b01presint;
        double b01rnint;
        // P01dep
        double a01dep;
        double b01outdep;
        double b01absdep;
        double b01gddep;
        // P10dep
        double a10dep;
        double b10indep;
        double b10outdep;
        double b10absdep;
        double b10gddep;

        double calculateDurationOpen(double outdoorTemperature);
    };

//**********************************************************************

//#endif  /* MODEL_WINDOWS_H */
#endif  // MODEL_WINDOWS_HPP_
