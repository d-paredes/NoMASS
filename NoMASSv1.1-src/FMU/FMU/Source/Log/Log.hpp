// Undefined description of file -- Jacob Chapman -- 2017
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018
//   Update -- daps -- 22.12.2017 external <string.h>, <stdlib.h>, <stdint.h> added
//   Update -- daps -- 2.1.2018 ERROR macro added
//   Update -- daps -- 5.1.2018 RESETLOG macro to reset the Log file

//**********************************************************************

//#ifndef LOG_H
//#define	LOG_H
#ifndef LOG_HPP_
#define	LOG_HPP_

#include <iostream>
#include <sstream>

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

//**********************************************************************

#if defined(_MSC_VER)
#define __FUNCTION__ FunctionMacroNotDefinedInMSVC
#endif

#define ERROR(message) Log::error(message, __FILE__, __FUNCTION__, __LINE__)
#define LOG Log()
#define RESETLOG Log(true)

//**********************************************************************

/**
 * @brief Logs the error messages
 * @details Logs the error messages for later writing to file
 */

//**********************************************************************

class Log
    {
    public:
        //Log();
        Log(const bool reset = false);

        template<typename T>
        Log &operator << (const T &t)
            {
            if(!errorFlag)
                {
                //buf << t << "\n";
                buf << t;
                //std::cout << "NoMASS log:" << t << std::endl;
                std::cout << t;
                }
            return *this;
            }

        static void printLog();
        static void error();
        static void error(const char* message, const char* fileName = "", const char* functionName = "", const uint32_t lineNo = 0);
        void reset();
        bool getError();

    private:
        static std::stringstream buf;
        static bool errorFlag;
    };

//**********************************************************************

//#endif	/* LOG_H */
#endif	// LOG_HPP_
