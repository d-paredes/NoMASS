// Copyright 2015 Jacob Chapman

#include <vector>
#include <iostream>
#include <fstream>
#include <utility>
#include <iomanip>
#include <string>
#include <regex>
#include "Log.hpp"
#include "Configuration.hpp"
#include "DataStore.hpp"

std::unordered_map<std::string, int> DataStore::variableMap;
std::vector<std::vector<float>> DataStore::intMap;

int DataStore::variableCount = 0;

DataStore::DataStore() {}

int DataStore::getID(const std::string &name) {
  //  std::cout << "getID: " << name << std::endl;
  return variableMap.at(name);
}

int DataStore::addVariable(const std::string &name) {
  int ret = -1;
  if (name != "") {
    for (std::string reg : Configuration::outputRegexs) {
      std::regex rgx(reg);
      std::smatch match;
      if (std::regex_match(name, match, rgx)) {
        if (variableMap.find(name) == variableMap.end()) {
          //  std::cout << "addVariable: " << ret << ": " << name << std::endl;
          ret = DataStore::variableCount;
          //  std::cout << "addVariable: " << ret << ": " << name << std::endl;
          variableMap.insert(std::make_pair(name, ret));
          intMap.push_back(std::vector<float>());
          DataStore::variableCount++;
        } else {
          ret = getID(name);
        }
        break;
      }
    }
  }
  return ret;
}

void DataStore::addValueS(const std::string &name, const float value) {
    if (name != "") {
        //  std::cout << "addValueS: " << name << ": " << value << std::endl;
        int val = variableMap.at(name);
        //  std::cout << "addValueS: " << val;
        //  std::cout << ": " << name << ": " << value << std::endl;
        addValue(val, value);
    }
}

void DataStore::addValue(const int & id, const float val) {
  if (id > -1) {
    intMap.at(id).push_back(val);
  }
}


float DataStore::getValueForZone(const std::string &name,
                                        const std::string &zoneName) {
    return getValueS(zoneName + name);
}

float DataStore::getValueS(const std::string & name) {
  //  std::cout << "get: " << name << std::endl;
  if (variableMap.find(name) == variableMap.end()) {
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
  //  std::cout << "get: " << id << ": " << name << std::endl;
  return getValue(id);
}

float DataStore::getValue(const int & id) {
  //  std::cout << "getValue: " << id << ": ";
  float ret = intMap.at(id).back();
  //  std::cout << ret << std::endl;

  return ret;
}

void DataStore::clearValues() {
  //std::cout << "clear values" << std::endl;
  std::vector<std::vector<float>>::iterator it;
  for (it=intMap.begin(); it != intMap.end(); ++it) {
    it->clear();
  }
}

void DataStore::clear() {
  //std::cout << "clear" << std::endl;
    variableMap.clear();
    intMap.clear();
    DataStore::variableCount = 0;
}

void DataStore::print() {
  if (Configuration::info.save) {
    //  std::cout << "print " << std::endl;
    std::ofstream myfile;
    myfile.open("NoMASS.out");
    myfile << std::fixed << std::setprecision(Configuration::info.precision);
    myfile << "stepCount";
    std::vector<int> ids;
    unsigned int maxSize = 0;
    std::unordered_map<std::string, int >::const_iterator it;
    for (it=variableMap.cbegin(); it != variableMap.cend(); ++it) {
        myfile << "," << it->first;
        int val = it->second;
        ids.push_back(val);
        if (maxSize < intMap.at(val).size()) {
          maxSize = intMap.at(val).size();
        }
    }
    myfile << "\n";

    for (unsigned int i = 0; i < maxSize; i++) {
        myfile << i;
        for (unsigned int j : ids) {
            myfile << ",";
            if (intMap.at(j).size() > i) {
              myfile << intMap.at(j).at(i);
            }
        }
        myfile << "\n";
    }
    myfile.close();
  }
}
