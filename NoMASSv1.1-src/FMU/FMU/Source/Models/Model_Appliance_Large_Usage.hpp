// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef MODEL_APPLIANCE_LARGE_USAGE_HPP_
#define MODEL_APPLIANCE_LARGE_USAGE_HPP_

#include <string>
#include <vector>
#include <cstddef>

#include <RapidXML/rapidxml_utils.hpp>
#include <RapidXML/rapidxml.hpp>
#include <Models/Model_RandomWeibull.hpp>

//**********************************************************************

/**
 * @brief Models the large appliance
 * @details Models large appliance for prediction of appliance use at each timestep adapted from
 * \n Jaboob, S. (2015). Stochastic Modelling of Occupants’ Activities and Related Behaviours. The University of Nottingham.
 */

//**********************************************************************

class Model_Appliance_Large_Usage : public Model_RandomWeibull
    {
    public:
        Model_Appliance_Large_Usage();

        double consumption(const int timeStep);
        double getPower();
        double getMeanFraction();
        virtual bool onAt(const int timeStep);
        void parseConfiguration(const std::string &filename);
        void setCountry(const std::string & name);
        void setID(const int id);
        std::string getCountry();
        bool isOn() const;

    protected:
        template <typename T>
        std::vector<T> as_vector(rapidxml::xml_node<> *node);
        template <typename T>
        std::vector<std::vector<T>> as_vector_vector(rapidxml::xml_node<> *node);

        double probOn(int timestep) const;
        virtual void parseShapeScale(rapidxml::xml_node<> *node);
        bool on;
        std::string name;
        std::string country;
        int id;
        int state;
        double maxPower;
        std::vector<double> meanF;
        std::vector<double> onProbabilities10;
        std::vector<double> onProbabilities;
        std::vector<std::vector<double>> transitions;
    };

//**********************************************************************

#endif  // MODEL_APPLIANCE_LARGE_USAGE_HPP_
