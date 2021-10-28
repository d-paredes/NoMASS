// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#ifndef DATASTORE_HPP_
#define DATASTORE_HPP_

#include <string>
#include <unordered_map>
#include <vector>

#include <Log/Log.hpp>

//**********************************************************************

/**
 * @brief Stores all the data at each timestep
 * @details Stores all the data at each timestep to be written to a file later in the process
 */

 //**********************************************************************

class DataStore
    {
    public:
        static int addVariable(const std::string &name);
        static int getID(const std::string &name);
        static void addValueS(const std::string &name, const float val);
        static void addValue(const int & id, const float val);
        static float getValueS(const std::string &name);
        static float getValue(const int & id);
        static float getValueForZone(const std::string &name, const std::string &zoneName);
        static void print();
        static void clear();
        static void clearValues();
    private:
        DataStore();
        static std::unordered_map<std::string, int> variableMap;
        static std::vector<std::vector<float>> intMap;
        static int variableCount;
    };

//**********************************************************************

#endif  // DATASTORE_HPP_
