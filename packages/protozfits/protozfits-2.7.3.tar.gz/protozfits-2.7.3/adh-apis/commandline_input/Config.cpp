#include "Config.h" 
#include <cctype>
#include <stdexcept>
#include <fstream>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <list>
#include <stdexcept>

/** @file Config.cpp
 *  @brief Base configuration class
 */

namespace ADH
{
namespace Conf 
{

/*---------------------------------------------------------------------------*/
Config::~Config() 
{
   //for ( auto entry :  _entries) delete entry.second;
}


/*---------------------------------------------------------------------------*/
bool Config::add(const std::string& section,const  std::string& key
  , const std::string& value, const std::string comment )
{

    Param param(value,comment);

    //std::map<std::string, Param >* perSectionMap = nullptr;
    // search if a map already exist for this section
    if ( _entries.find(section) == _entries.end() )
    {// No map for his section, create and store it now
        //perSectionMap = new std::map<std::string,Param>();
        //_entries[section]=perSectionMap;
        _entries[section] = std::map<std::string,Param>();
    }
/*
    else
    {
        perSectionMap = _entries.find(section)->second;
    }
*/
    // At this point unique pointer exit (either just cerated, either already
    //  existing
    //
    if (_entries.find(section)->second.insert
       (std::pair<std::string, Param >(key,param))
        .second == false)
    { 
      std::string str_list = this->getInternal( section,key);
      if ( str_list.find(",") == std::string::npos ) // not yet a list,
                                                   //  only one elem
      str_list = "\"" + str_list + "\"";
      
      str_list = str_list + ",\""+value + "\"";
      
      Param list_param(str_list,comment);
      _entries.find(section)->second.at(key) = list_param;
      
    }
    return true;
}

/*---------------------------------------------------------------------------*/
const std::string& Config::getInternal(const std::string& section
                                  , const std::string& key) const
{
    //std::map<std::string,Param >* perSectionMap = nullptr;
    if (  _entries.find(section) == _entries.end())
    {
        throw std::runtime_error("section " + section +" does not exist");
    }
    //perSectionMap = _entries.find(section)->second;
    if ( _entries.find(section)->second.find(key)
        ==  _entries.find(section)->second.end() )
    {
        throw std::runtime_error(yellow  + "key " + key + no_color + " for section " + section
        + yellow + " does not exist" + no_color);
    }


    return _entries.find(section)->second.find(key)->second._value;

}

/*---------------------------------------------------------------------------*/
std::list<std::string> Config::getListFromString(const std::string& entry) const
{
  std::list<std::string> val_str_list;
  // search all comma and store their posistion in list_pos_comma
  std::list<int> list_pos_comma;
  size_t pos_comma = 0;

  while (pos_comma != std::string::npos)
  {
    pos_comma = entry.find(',' , pos_comma+1);
    if ( pos_comma != std::string::npos) {
      list_pos_comma.push_back(pos_comma);
    }
  }
  if ( list_pos_comma.size()==0)
  { // list with only one elemenent
    std::string res = entry;
    val_str_list.push_back(res);
    return val_str_list;
  }

// Get elem between comma and store it to val_str_list 
  int last_comma = -1;
  std::string elem;
  //gcc4.1
  for (auto ccomma_pos=list_pos_comma.begin(); ccomma_pos!=list_pos_comma.end(); ccomma_pos++)
  {
    int comma_pos = *ccomma_pos;
//  for ( int comma_pos : list_pos_comma) {
    if ( last_comma == -1 )
    {
      size_t len = comma_pos;
      elem = entry.substr(0,len);
    }
    else
    {
      size_t pos = last_comma+1;
      size_t len = comma_pos-last_comma-1;
      elem = entry.substr(pos,len);
    }
    elem = trim(elem); // supress blanck character before
                       //  and after first other character
    val_str_list.push_back(elem);
    last_comma = comma_pos;
  }
    // add last elem
    elem = entry.substr(last_comma+1);
    elem = trim(elem); // supress blanck character before
                       //  and after first other character
    val_str_list.push_back(elem);

  return  val_str_list;
}
/*---------------------------------------------------------------------------*/
/*
 * print all configuration key/value pair
 */
  void Config::printAll() const
  {
    std::cout<< green << std::endl;
    std::cout<< green <<   "==========STARTING CONFIGURATION SERVICE LISTING===== "
         << no_color <<  std::endl;
//gcc4.1
    for (auto ssection=_entries.begin(); ssection!=_entries.end(); ssection++)
    {
        auto& section = *ssection;
//    for ( auto &section:_entries  )
//    {
      std::cout<< green << std::endl;
      std::cout<< green <<   "Section: "  << section.first <<  std::endl;
      std::cout<< green << std::left <<  std::setw(30)<< "---- Key ----"
           << std::left << std::setw(30)<< "--- value ---" 
           << std::left << std::setw(30)<< "-- comment --" 
           << no_color << std::endl;
//gcc4.1
      for (auto eelem=section.second.begin(); eelem!=section.second.end(); eelem++)
      {
        auto& elem = *eelem;
//      for ( auto &elem : section.second)
//      {
        std::cout<< green << std::setw(30) << std::left << elem.first
             << std::setw(30) << std::left << elem.second._value  << "#"
             << std::setw(30) << std::left << elem.second._comment << no_color << std::endl;
      }
    }
    std::cout<< green << no_color << std::endl;
    std::cout<< green <<   "==========ENDING CONFIGURATION SERVICE LISTING===== "
         << no_color <<  std::endl;
    std::cout << std::endl;
}

std::string Config::trimKey(const std::string &entry)const
{
  std::string result = entry;
  if ( entry.find("--")!=std::string::npos )
  { result = entry.substr(2,entry.size()-2) ; }
  else if (entry.find("-")!=std::string::npos)
  { result = entry.substr(1,entry.size()-1) ; }

  return result;
}

// this function needs to take an unsigned char, see
// https://en.cppreference.com/w/cpp/string/byte/isspace#Notes
bool is_nonspace(unsigned char c) {
    return !std::isspace(c);
}

/*---------------------------------------------------------------------------*/
// trim from start
std::string &Config::ltrim(std::string &s)const {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), is_nonspace));
        return s;
}

/*---------------------------------------------------------------------------*/
// trim from end
std::string &Config::rtrim(std::string &s) const{
        s.erase(std::find_if(s.rbegin(), s.rend(), is_nonspace).base(), s.end());
        return s;
}

/*---------------------------------------------------------------------------*/
// trim from both ends
std::string &Config::trim(std::string &s) const{
        return ltrim(rtrim(s));
}




/*---------------------------------------------------------------------------*/
}; // end namespace Conf
}; // end namespace ADH

