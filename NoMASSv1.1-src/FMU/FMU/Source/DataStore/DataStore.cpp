// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <iomanip>
#include <iostream>
#include <fstream>
#include <regex>
#include <string>
#include <utility>
#include <vector>

#include <Configuration/Configuration.hpp>
//#include <Log/Log.hpp>

#include "DataStore.hpp"

//**********************************************************************

std::unordered_map<std::string, int> DataStore::variableMap;
std::vector<std::vector<float>> DataStore::intMap;

int DataStore::variableCount = 0;

//**********************************************************************

DataStore::DataStore() {}

int DataStore::getID(const std::string &name)
    {
    return variableMap.at(name);
    }

int DataStore::addVariable(const std::string &name)
    {
    int ret = -1;
    if (name != "")
        {
        for (std::string reg : Configuration::outputRegexs)
            {
            std::regex rgx(reg);
            std::smatch match;
            if (std::regex_match(name, match, rgx))
                {
                if (variableMap.find(name) == variableMap.end())
                    {
                    ret = DataStore::variableCount;
                    variableMap.insert(std::make_pair(name, ret));
                    intMap.push_back(std::vector<float>());
                    DataStore::variableCount++;
                    }
                else
                    {
                    ret = getID(name);
                    }
                break;
                }
            }
        }
    return ret;
    }

void DataStore::addValueS(const std::string &name, const float value)
    {
    if (name != "")
        {
        int val = variableMap.at(name);
        addValue(val, value);
        }
    }

void DataStore::addValue(const int & id, const float val)
    {
    if (id > -1)
        {
        intMap.at(id).push_back(val);
        }
    }


float DataStore::getValueForZone(const std::string &name,
                                 const std::string &zoneName)
    {
    return getValueS(zoneName + name);
    }

float DataStore::getValueS(const std::string & name)
    {
    if (variableMap.find(name) == variableMap.end())
        {
        LOG << "Cannot find the variable: " << name;
        LOG << "\nThis could happen for a number of reasons:\n";
        LOG << " - Check the Zone Name is correct in ";
        LOG << "the NoMass simulation configuration file\n";
        LOG << " - Check that all variable are defined ";
        LOG << "in the model description file\n";
        LOG.error();
        exit(-1);
        return 0;
        }
    int id = variableMap.at(name);
    return getValue(id);
    }

float DataStore::getValue(const int & id)
    {
    float ret = intMap.at(id).back();
    return ret;
    }

void DataStore::clearValues()
    {
    std::vector<std::vector<float>>::iterator it;
    for (it=intMap.begin(); it != intMap.end(); ++it)
        {
        it->clear();
        }
    }

void DataStore::clear()
    {
    variableMap.clear();
    intMap.clear();
    DataStore::variableCount = 0;
    }

void DataStore::print()
    {
    if (Configuration::info.save)
        {
		time_t Time;
		time(&Time);
		char* pszDate = ctime(&Time);
		if (static_cast<char>(pszDate[strlen(pszDate) - 1]) == '\n')
			pszDate[strlen(pszDate) - 1] = '\0';

		LOG << "...SavingData" << pszDate << "\n";
        std::ofstream myfile;
        myfile.open("NoMASS.csv");
        myfile << std::fixed << std::setprecision(Configuration::info.precision);
        myfile << "stepCount";
        std::vector<int> ids;
        unsigned int maxSize = 0;
        std::unordered_map<std::string, int >::const_iterator it;
        for (it=variableMap.cbegin(); it != variableMap.cend(); ++it)
            {
            myfile << "," << it->first;
            int val = it->second;
            ids.push_back(val);
            if (maxSize < intMap.at(val).size())
                {
                maxSize = intMap.at(val).size();
                }
            }
        myfile << "\n";

        for (unsigned int i = 0; i < maxSize; i++)
            {
            myfile << i;
            for (unsigned int j : ids)
                {
                myfile << ",";
                if (intMap.at(j).size() > i)
                    {
                    myfile << intMap.at(j).at(i);
                    }
                }
            myfile << "\n";
            }
        myfile.close();
        }
    }

//**********************************************************************
