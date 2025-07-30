/**
 *  @file ColoredOutpute.h
 *
 *  @brief Colored output constants definitions extracted from the BasicDefs.h file.
 *
 *  Created on: Apr 19, 2021
 *      Author: muraczewski
 */

#ifndef COLORED_OUTPUT_H_
#define COLORED_OUTPUT_H_
#include <string>

namespace ADH{

/** @namespace ADH::ColoredOutput
     *  @brief const strings to use to display colored text in consoles
     *
     *  The actual color results will vary depending on custom user settings on the terminal itself
     *
     *  @todo Ideally, once we chose the loggin facitlity, the values below should be overriden as needed accordingly
     */
    namespace ColoredOutput
    {
        #define COLORED_OUTPUT
        #ifdef COLORED_OUTPUT
            const std::string red =      "\33[31m"; ///< Red
            const std::string green =    "\33[32m"; ///< Green
            const std::string yellow =   "\33[33m"; ///< Yellow
            const std::string blue =     "\33[34m"; ///< Blue
            const std::string magenta =  "\33[35m"; ///< Magenta
            const std::string cyan =     "\33[36m"; ///< Cyan
            const std::string white =    "\33[37m"; ///< White
            const std::string no_color = "\33[0m";  ///< Return to shell default
            const std::string light_red =     "\33[91m"; ///< Lighter red
            const std::string light_green =   "\33[92m"; ///< Lighter green
            const std::string light_yellow =  "\33[93m"; ///< Lighter Yellow
            const std::string light_blue =    "\33[94m"; ///< Lighter Blue
            const std::string light_magenta = "\33[95m"; ///< Lighter Magenta
            const std::string light_cyan =    "\33[96m"; ///< Lighter Cyan
            const std::string light_white =   "\33[97m"; ///< Bright White
        #else
            const std::string red =      "";
            const std::string green =    "";
            const std::string yellow =   "";
            const std::string blue =     "";
            const std::string magenta =  "";
            const std::string cyan =     "";
            const std::string white =    "";
            const std::string no_color = "";
            const std::string light_red =     "";
            const std::string light_green =   "";
            const std::string light_yellow =  "";
            const std::string light_blue =    "";
            const std::string light_magenta = "";
            const std::string light_cyan =    "";
            const std::string light_white =   "";
        #endif
    } //namespace ADH::ColoredOutput
}

#endif
