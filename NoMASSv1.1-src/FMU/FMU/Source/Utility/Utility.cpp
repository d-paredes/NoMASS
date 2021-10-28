// Undefined description of file -- Jacob Chapman -- 2015
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018

//**********************************************************************

#include <algorithm>
#include <ctime>
#include <fstream>
#include <iostream>
#include <list>
#include <numeric>
#include <random>
#include <string>
#include <vector>

#include "Utility.hpp"

//**********************************************************************

std::random_device Utility::r;
std::mt19937_64 Utility::engine(r());

Utility::Utility() {}

void Utility::setSeed(int seed)
    {
    Utility::engine.seed(seed);
    Utility::randomDouble(0, 1);
    }

double Utility::randomDouble(double min, double max)
    {
    std::uniform_real_distribution<double> uniform_dist(min, max);
    return uniform_dist(engine);
    }

bool Utility::tossACoin()
    {
    return randomDouble(0.0, 1.0) < 0.5;
    }

int Utility::randomInt(int min, int max)
    {
    std::uniform_int_distribution<int> uniform_dist(min, max);
    return uniform_dist(engine);
    }

std::vector<int> Utility::randomIntVect(int number)
    {
    std::vector<int> v(number);
    std::iota (std::begin(v), std::end(v), 0);
    std::shuffle(v.begin(), v.end(), Utility::engine);
    return v;
    }

void Utility::splitCSV(const std::string & typeString,
                       std::vector<std::string> * types)
    {
    const char *str = typeString.c_str();
    char c = ',';
    do
        {
        const char *begin = str;
        while (*str != c && *str)
            {
            str++;
            }
        types->push_back(std::string(begin, str));
        }
    while (0 != *str++);
    }

int Utility::calculateNumberOfDays(const int startDay,
                                   const int startMonth,
                                   const int endDay,
                                   const int endMonth)
    {
    static const int daysInMonth[] =
        {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    int days = (startDay -1);
    for (int i = startMonth -1; i < endMonth -1; i++)
        {
        days += daysInMonth[i];
        }
    days += endDay;
    return days;
    }

int Utility::cumulativeProbability(const double * v, const int len)
    {
    return Utility::cumulativeProbability(std::vector<double>(v, v + len));
    }

int Utility::cumulativeProbability(const std::vector<double> &p)
    {
    int activity = -1;
    double sum = 0;
    double drand = Utility::randomDouble(0.0, 1.0);
    for (unsigned int i = 0; i < p.size(); i++)
        {
        sum += p[i];
        if (sum >= drand)
            {
            activity = i;
            break;
            }
        }
    return activity;
    }

std::vector<std::string> Utility::csvToTableHead(const std::string & filename)
    {
    std::string line;
    std::ifstream myfile(filename);
    std::vector<std::string> t;
    if (myfile.is_open())
        {
        getline(myfile, line);
        Utility::splitCSV(line, &t);
        myfile.close();
        }
    return t;
    }

std::vector<double> Utility::csvToDouble(const std::string & s)
    {
    std::vector<double> items;
    std::vector<std::string> stringItems;
    Utility::splitCSV(s, &stringItems);
    for (std::string &item : stringItems)
        {
        items.push_back(std::stod(item));
        }
    return items;
    }

std::vector<int> Utility::csvToInt(const std::string & s)
    {
    std::vector<int> items;
    std::vector<std::string> stringItems;
    Utility::splitCSV(s, &stringItems);
    for (std::string &item : stringItems)
        {
        items.push_back(std::stoi(item));
        }
    return items;
    }

const char* Utility::getTime()
    {
    time_t Time;
    time(&Time);
    char* pszDate = ctime(&Time);
    if(static_cast<char>(pszDate[strlen(pszDate)-1]) =='\n')
        pszDate[strlen(pszDate)-1]='\0';
    return pszDate;
//    time_t Time;
//    time(&Time);
//    char* dt = ctime(&Time);
//    uint32_t len = strlen(dt);
//    dt[len-1] = '\0';
//    char* dt_ = new char[len];
//    memset(dt_, '@', len);
//    memcpy(dt_, dt, len);
//    dt_[len]='\0';
//    return dt_;
    }

//**********************************************************************
