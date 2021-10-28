// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

//#ifndef MODEL_RANDOMWEIBULL_H
//#define	MODEL_RANDOMWEIBULL_H
#ifndef MODEL_RANDOMWEIBULL_HPP_
#define	MODEL_RANDOMWEIBULL_HPP_

//**********************************************************************

/**
 * @brief Models a weibull function
 * @details Models a weibull function
 */

//**********************************************************************

class Model_RandomWeibull
    {
    public:
        Model_RandomWeibull();

        static double randomWeibull(double scale, double shape);
        static double randomDouble();
        static double randomDouble(double min, double max);
        static double probability(double m);
    };

//**********************************************************************

//#endif	/* MODEL_RANDOMWEIBULL_H */
#endif	// MODEL_RANDOMWEIBULL_HPP_
