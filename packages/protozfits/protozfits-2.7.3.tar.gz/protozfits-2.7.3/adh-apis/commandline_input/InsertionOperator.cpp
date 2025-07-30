#include <ostream>
#include <string>
#include <iostream>
#include <vector>
#include <list>
#include <sstream>
#include <iomanip>
#include <limits>
#include <typeinfo>

/**
 * @file InsertionOperator.cpp
 * @brief  define insertion operators for Config class
 *
 * -http://www.cplusplus.com/reference/ostream/ostream/operator%3C%3C/
 *  These operator are mandatory to write std::container to Config object
 *  
 *  Character types 
 *      -char        Exactly one byte in size. At least 8 bits.
 *      -char16_t    Not smaller than char. At least 16 bits.
 *      -char32_t    Not smaller than char16_t. At least 32 bits.
 *      -wchar_t     Can represent the largest supported character set.
 *  Integer types (signed)  signed char Same size as char. At least 8 bits.
 *      -signed short int    Not smaller than char. At least 16 bits.
 *      -signed int  Not smaller than short. At least 16 bits.
 *      -signed long int Not smaller than int. At least 32 bits.
 *  Integer types (unsigned)    unsigned char  
 *      -unsigned short int
 *      -unsigned int
 *      -unsigned long int
 *  Floating-point types    
 *       -float   
 *       -double  Precision not less than float
 *       -long double Precision not less than double
 *  Boolean type 
 *       - bool    
 */

using namespace std;

template<typename T>
ostream& format (ostream& out,list<T>& l) ;

template<typename T>
ostream& format (ostream& out,vector<T>& source) ;


void del_comma(string &value)
{
 value = value.substr(0,value.size()-1);
}


template<typename T>
ostream& format (ostream& out,vector<T>& source) {
  list<T> dest(source.begin(), source.end());
  return format(out,dest);
}

template<typename T>
ostream& format (ostream& out,list<T>& l) {

  ostringstream result;


//  std::string result="";
//gcc4.1
  for (auto eentry=l.begin(); eentry!=l.end(); eentry++)
  {
    auto entry = *eentry;
//  for(auto entry : l)
//  {
    std::ostringstream tmp_out;
    if ( typeid(entry) == typeid(float)) {
      tmp_out << std::setprecision( std::numeric_limits<float>::digits10 + 2)
          << entry; 
      result << tmp_out.str();
      }
      //result = result + tmp_out.str(); }
    else if ( typeid(entry) == typeid(double)) {
      tmp_out << std::setprecision( std::numeric_limits<double>::digits10 + 2)
          << entry; 
      result << tmp_out.str();
      }
      //result = result + tmp_out.str();}
    else if ( typeid(entry) == typeid(long double)) {
      tmp_out <<std::setprecision(std::numeric_limits<long double>::digits10+ 2)
          << entry; 
      result << tmp_out.str();}

    else {
       result << entry;
//      result = result+std::to_string(entry);
    }
    if (typeid(entry) == typeid(unsigned short int) ||
        typeid(entry) == typeid(unsigned int) ||
        typeid(entry) == typeid(unsigned long int) ){
      result << "U";
//      result = result +  "U" ;
    }
    result << ",";
//    result = result +"," ;
  }
  string rresult = result.str();
  del_comma(rresult);
  out << rresult ;
  return out;
} 


namespace ADH {
namespace Conf {

ostream& operator << (ostream& out,std::list<std::string >  l) {
  std::string result="";
//gcc4.1
  for (auto eentry=l.begin(); eentry!=l.end(); eentry++)
  {
    auto entry= *eentry;
//  for(auto entry : l)
//    {
    result = result+entry+"," ; }
  del_comma(result);
  out << result ;
  return out;
}

ostream& operator << (ostream& out,list<char> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<char16_t> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<char32_t> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<wchar_t> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<signed short int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<signed int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<signed long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<signed long long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<unsigned short int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<unsigned int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<unsigned long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<unsigned long long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<float> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<double> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<long double> l) {
  return format(out,l); }

ostream& operator << (ostream& out,list<bool> l) {
  return format(out,l); }

// std::vector 
ostream& operator << (ostream& out,std::vector<std::string >  l) {
  std::string result="";
//gcc4.1
  for (auto eentry=l.begin(); eentry!=l.end(); eentry++)
  {
    auto entry = *eentry;
//  for(auto entry : l)
//    {
    result = result+entry+"," ; }
  del_comma(result);
  out << result ;
  return out;
}
ostream& operator << (ostream& out,vector<char> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<char16_t> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<char32_t> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<wchar_t> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<signed short int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<signed int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<signed long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<signed long long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<unsigned short int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<unsigned int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<unsigned long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<unsigned long long int> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<float> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<double> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<long double> l) {
  return format(out,l); }

ostream& operator << (ostream& out,vector<bool> l) {
  return format(out,l); }

};}; // end namespace ADH::Conf
