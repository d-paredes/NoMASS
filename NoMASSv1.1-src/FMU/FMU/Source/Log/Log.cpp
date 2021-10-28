// Undefined description of file -- Jacob Chapman -- 2016
//
// REVISION HISTORY:
//   Initial refactoring -- Daniel A. Paredes-Soto -- 3.1.2018
//   Updated -- daps -- 22.12.2017
//   printLog() exit program only if errorFlag equals True -- 22.12.2017

//**********************************************************************

#include <fstream>
#include <iostream>
#include <string>

#include <Utility/Utility.hpp>

#include "Log.hpp"

// Define the static member, somewhere in an implementation file.
std::stringstream Log::buf;
bool Log::errorFlag = false;

//**********************************************************************

//Log::Log() {}

Log::Log(bool reset)
    {
    if(!reset)
        return;

    char* pszUsername = getenv(USER);
    time_t Time;
    time(&Time);
    char* pszDate = ctime(&Time);
    if(static_cast<char>(pszDate[strlen(pszDate)-1]) =='\n')
        pszDate[strlen(pszDate)-1]='\0';
    std::ofstream outfile;
    outfile.open("NoMASS.log", std::ios_base::trunc);
    outfile << "   **   ~~~   ** " << "Created by ";
    if(pszUsername != NULL)
        {
        outfile << pszUsername;
        }
    outfile << " on " << pszDate;
    outfile << std::endl;
    outfile << "   **   ~~~   ** " << std::endl;
    outfile.close();
    }

void Log::printLog()
    {
    const long bufPostion = buf.tellp();
    //std::cout << "writing Log into disk" << std::endl;
    //std::cout << "length:" << length << "::" << std::endl;
    //std::cout << "//" << buf.str() << "\\" << std::endl;
    //if (errorFlag) {
    std::string line;
    std::ofstream outfile;
    outfile.open("NoMASS.log", std::ios_base::app);

    if (errorFlag) {
        outfile << "   *************"  << std::endl;
        outfile << "   ************* ===== ";
        outfile << "Final No-MASS (Detailed Occupancy) Error Summary =====";
        outfile << std::endl;

        if (std::getline(buf, line)) {
            outfile << "   **  Fatal  ** " << line  << std::endl;
        }
    }

    while (std::getline(buf, line)) {
        outfile << "   **   ~~~   ** " << line  << std::endl;
    }

    // jump to the last known buffer position
    buf.clear();
    buf.seekg(bufPostion); // buf.seekg(0, std::ios::beg);

    if (errorFlag) {
        outfile << "   *************"  << std::endl;
        outfile << "   *************"  << std::endl;
    }
    outfile.close();

    if (errorFlag)
        {
        exit(-999);
        return;
        }
//    if (errorFlag)
//        {
//        std::ofstream outfile;
//        outfile.open("No-MASS.err", std::ios_base::app);
//        outfile << "   *************"  << std::endl;
//        outfile << "   ************* ===== ";
//        outfile << "Final No-MASS (Detailed Occupancy) Error Summary =====";
//        outfile << std::endl;
//        std::string line;
//
//        if (std::getline(Log::buf, line))
//            {
//            outfile << "   **  Fatal  ** " << line  << std::endl;
//            }
//        while (std::getline(Log::buf, line))
//            {
//            outfile << "   **   ~~~   ** " << line  << std::endl;
//            }
//        outfile << "   *************"  << std::endl;
//        outfile << "   *************"  << std::endl;
//        outfile.close();
//        }
    }

void Log::error()
    {
    errorFlag = true;
    Log::printLog();
    }

void Log::error(const char* message, const char* filename, const char* functionName, const uint32_t lineNo)
{
    buf << message;

    std::cout << "ERROR ";
#	if defined(_MSC_VER)
    buf << " in " << functionName << "(): ";	// __FUNCTION__ macro is not defined in MSVC
#	endif
    std::cout << message << std::endl;

    if(strcmp(filename,""))
        {
        std::cout << "Called from " << filename;
        buf <<  "Called from " << filename;
        if(strcmp(functionName, ""))
            {
            std::cout << " in " << functionName;
            buf << " in " << functionName;
            }
        if(lineNo > 0)
            {
            std::cout << " at line number " << lineNo;
            buf << " at line number " << lineNo;
            }
        std::cout << std::endl;
        buf << "\n";
        }

    //exit(-999);
    //errorFlag = true;
    //Log::printLog();
    error();
    return;
}

void Log::reset()
    {
    errorFlag = false;
    }

bool Log::getError()
    {
    return errorFlag;
    }

//**********************************************************************
