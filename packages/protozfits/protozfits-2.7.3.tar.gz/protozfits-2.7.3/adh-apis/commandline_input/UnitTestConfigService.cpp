#include <ConfigService.h>
#include <CMakeDefs.h>

/**
 * @file UnitTestConfigService.cpp
 *
 * @brief Unit tests of the Configuration classes
 *
 */
#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <math.h>
#include <stdexcept>

#include "BasicDefs.h"

using namespace std;
using namespace ADH::Conf;

int parseAndTest(ConfigService& conf,std::string full_path_name);

/*---------------------------------------*/
class Point
{
friend std::ostream& operator << (std::ostream& out, const Point& x)
{
  return(x.operator <<(out));
}

public:
Point (): _name("none"), _x(0), _y(0), _z(0) { ; } ;
Point (std::string name, double x,double y,double z)
      :_name(name), _x(x), _y(y), _z(z) { ; } ;

Point (const std::string& entry)
{
    size_t name_pos = entry.find("name=");
    size_t x_pos = entry.find("x=");
    size_t y_pos = entry.find("y=");
    size_t z_pos = entry.find("z=");

    if (x_pos == std::string::npos || y_pos == std::string::npos 
        || z_pos == std::string::npos )
    {
        throw;
    }
    _name = entry.substr(name_pos+5, x_pos-name_pos-5);
    // remove blank
    ostringstream nname;
    for (auto it=_name.begin(); it!=_name.end(); it++)
    {
        if (*it != ' ')
            nname << *it;
    }
    _name = nname.str();
   // _name.erase(std::remove_if( _name.begin(), _name.end(), [](char c){ return (c == ' ' );}), _name.end() );

    std::string x_string = entry.substr(x_pos+2, y_pos-x_pos-2);
    std::string y_string = entry.substr(y_pos+2, z_pos-y_pos-2);
    std::string z_string = entry.substr(z_pos+2, entry.size()-z_pos-2);
//    cout << "Positions=" << x_pos << " " << y_pos << " " << z_pos << endl;
//    cout << "Inter string: " << x_string << " " << y_string << " " << z_string << endl;
    _x=std::stod(x_string);
    _y=std::stod(y_string);
    _z=std::stod(z_string);
    
//    cout << "Point is=" << _name << " " << _x << " " << _y << " " << _z << endl;
};


double x() const { return _x; } ;
double y() const { return _y; } ;
double z() const { return _z; } ;
std::string name() const { return _name; } ;

 std::ostream& operator << (std::ostream& out) const {
    out << this->str() << std::endl ;
    return out ;
  }


private:
std::string str() const { 
    std::ostringstream sresult;
 //   std::string result;
    sresult << "{name=" << _name << " x=" << _x << " y=" << _y << " z=" << _z << "}";
    return sresult.str();
 //   result = "{name=" + _name + " x=" + std::to_string(_x) +
 //        " y=" + std::to_string(_y) + " z=" + std::to_string(_z) + "}" ;
 //   cout << "Original:" << endl;
 //   cout << result << endl;
 //   cout << "New:" << endl;
 //   cout << sresult.str() << endl;
 //   cout << endl;
 //   return result;
}


std::string _name;
double _x,_y,_z;

};


/*---------------------------------------*/
int main(int argc, char** argv)
{
    std::cout << green << "Binary path: " << CMAKE_BINARY_DIR << no_color << std::endl;

    try
    {
      std::string usage
        =("usage:myprog --key value\n -h: display help \n--help display help");
      std::ostringstream svers;
      svers << ADH_VERSION_MAJOR << "." << ADH_VERSION_MINOR;
      std::string version = svers.str();
      

      ConfigService conf(usage, version);

      if ( conf.parseArgument(argc,argv) != true ) { cout << "Parsing failure... " << endl; return -1; }

      char** aargv;
      aargv = new char*[100];
      for (uint32 i=0;i<100;i++)
        aargv[i] = new char[1024];
      sprintf(aargv[0], "%s", "my_program");
      sprintf(aargv[1], "%s", "--algo1");
      sprintf(aargv[2], "%s", "calibration");
      sprintf(aargv[3], "%s", "--tag");
      sprintf(aargv[4], "%s", "version_0.1");
      sprintf(aargv[5], "%s", "--split");
      sprintf(aargv[6], "%s", "1");
      sprintf(aargv[7], "%s", "--tel_ids");
      sprintf(aargv[8], "%s", "1,4,67,32");
      sprintf(aargv[9], "%s", "--ports");
      sprintf(aargv[10], "%s", "tcp::2222");
      sprintf(aargv[11], "%s", "--ports");
      sprintf(aargv[12], "%s", "tcp::22");
//      sprintf(aargv[9], "%s", "--tel_ids");
//      sprintf(aargv[10], "%s", "4");
//      sprintf(aargv[11], "%s", "--tel_ids");
//      sprintf(aargv[12], "%s", "67");
//      sprintf(aargv[13], "%s", "--tel_ids");
//      sprintf(aargv[14], "%s", "32");

      ConfigService config(usage, version);
      config.parseArgument(13, aargv);

      std::cout << green << "relartive path[" << config.getRelativePath() << "]" << no_color << std::endl;

      if ( config.getVersion().compare(version) != 0 ) { return -1;} 
      if ( config.getMessage().compare(usage) != 0 ) { return -1;} 
std::cout << __LINE__ << std::endl;
      {
        std::string val = config.get<std::string>("algo1");
        if ( val.compare("calibration") != 0 ) {return -1;}
      } 
std::cout << __LINE__ << std::endl;
      {
        std::string val = config.get<std::string>("tag");
        if ( val.compare("version_0.1") != 0 ) {return -1;}
      } 
 std::cout << __LINE__ << std::endl;
      {
        bool val = config.get<bool>("split");
        if ( val != 1 ) {return -1;}
      } 
std::cout << __LINE__ << std::endl;
      {std::list<int> val 
          = config.getList<int>("tel_ids");
        std::list<int> ref={1,4,67,32};

        if (val != ref) { return -1; }
      }

std::cout << __LINE__ << std::endl;
//config.printAll();
      // test lists made by repeated section/key
      {std::list<std::string> val 
          = config.getList<std::string>("ports");
std::cout << __LINE__ << std::endl;
        std::list<std::string> ref={"tcp::2222" , "tcp::22"};
std::cout << __LINE__ << std::endl;

        if (val != ref) { return -1; }
      }

std::cout << __LINE__ << std::endl;
    /* Check addRequired and checkRequiredParams */
    config.addRequired("split");    
    config.addRequired(DEFAULT_SECTION,"tel_ids");    
    if ( !config.checkRequiredParams() ) { return -1;}
    config.addRequired("none exisitng section", "non existing key");    
    if ( config.checkRequiredParams() ) { return -1;}

    std::cout << green << "-----------> All Arguments tests pass" << no_color << std::endl;
std::cout << __LINE__ << std::endl;


// Test Abstract base class Config method here thanks to ConfigService
// because Config class cannot be instantiated
      int val_src = 2;
      config.add("section", "key", val_src );
      int val_res = config.get<int>("section", "key");
      if (val_res != val_src) { return -1; }
      if ( !config.has("section", "key")) { return -1;}
      if ( config.has("unexisting section", "key")) { return -1;}
      if ( config.has("section", "unexisitng key")) { return -1;}
      if ( config.has("sunexisting section", "unexisitng key")) { return -1;}

std::cout << __LINE__ << std::endl;
      Point pt("o_point", 3.2,-432.2,4);

      config.add("Geo", "center",pt);
      // get from Config
      Point pt_res(config.get<std::string>("Geo","center"));
      cout << "STring: " << config.get<string>("Geo", "center") << endl;
      //Point pt_res2 = config.get<Point>("Geo","center");
      // test result
      if (pt_res.x() !=  3.2 || pt_res.y() !=-432.2   || pt_res.z() !=4 ||
      pt_res.name().compare("o_point") !=0) { return -1; }

std::cout << __LINE__ << std::endl;
      // test std::list<int>
      // add to config
      std::list<int> list_int{ 2 , 6 , 8, 9 } ;
      config.add("s71", "list elem" , list_int);
std::cout << __LINE__ << std::endl;
      // get from Config
      std::list<int>list_int_res=config.getList<int>("s71", "list elem");
      if ( list_int != list_int_res ) { return -1; }
std::cout << __LINE__ << std::endl;
      if ( !config.has("s71", "list elem")) { return -1;}
std::cout << __LINE__ << std::endl;
      if ( config.has("unexisting section", "list elem")) { return -1;}

std::cout << __LINE__ << std::endl;
      // test std::list<std::string>
      // add to config
      std::list<std::string> list_str={ "Telescope1" , "Tel2" , "Tel3" } ;
      config.add("s71", "list string" , list_str);
      // get from Config
      std::list<std::string>list_str_res
        = config.getList<std::string>("s71", "list string");
      if ( list_str_res != list_str ) { return -1; }

      {
      config.add("s71", "list repeated" , "first");
      config.add("s71", "list repeated" , "second");
      config.add("s71", "list repeated" , "third");
      // get from Config
      std::vector<std::string>list_str
        = config.getVector<std::string>("s71", "list repeated");
      std::vector<std::string> list_str_res = { "first","second","third" } ;

      if ( list_str_res != list_str ) { return -1; }
      }

std::cout  << __LINE__  << std::endl;

        string binary_dir = CMAKE_BINARY_DIR;
        //build path to input configuration file.
        string relative_path = binary_dir + "/../../apis/commandline_input/configUnitTest.ini";

      if (parseAndTest(config, relative_path) == -1) {return -1;}
//      if (parseAndTest(config,"../../../Resources/configUnitTest.ini") == -1) { return -1;}

std::cout << green << __LINE__ << no_color << std::endl;
      ConfigService config_cpy=config;
std::cout << green  << __LINE__ << no_color <<std::endl;
 
        return 0;
      
      //no test write as this pollutes the source hierarchy
      // test write
//std::cout << green  << __LINE__ << no_color <<std::endl;
//      if (!config_cpy.writeFile("./Resources/outfile.ini") ) { return -1; }
//std::cout << green  << __LINE__ << no_color <<std::endl;
      
//      config_cpy.printAll();
std::cout << __LINE__ << std::endl;
      ADH::Conf::ConfigService conf2;
std::cout << __LINE__ << std::endl;

//      if (parseAndTest(conf2,"./outfile.ini") == -1) { return -1;}
      }
      catch (std::exception& e)  {
          std::cout << light_red <<"catch exception in ConfigService.cpp while parsing input file: " << e.what()
                << no_color << std::endl;
          return -1;
      }

      std::cout << green << "-----------> All tests pass" << no_color << std::endl;
  return 0;
}
//-----------------------------------------------------------------------------
// Now test ConfigService class
// First, parse an existing file
int parseAndTest(ConfigService& config,std::string full_path_name)

{
    // test to parse input configuration file
    if (  config.parseFile(full_path_name) != true) { return -1; }

std::cout << green << __LINE__ << no_color << std::endl;
    ConfigService conf(config);
std::cout << green << __LINE__ << no_color << std::endl;
    //conf.printAll();

    try {
        // test std::string
        std::string val_str =  conf.get<std::string>("reader", "value_string"); 
        if ( val_str.find("test space") == std::string::npos) { return -1; }

std::cout << green << __LINE__ << no_color << std::endl;

        // test correct decimal unsigned integer value with 'u' suffix
        unsigned int val_u_int_res = 
          conf.get<unsigned int>("reader", "unsigned_int_u");
        if ( val_u_int_res != 4294967295u) { return -1; };

std::cout << green << __LINE__ << no_color << std::endl;
        // test correct decimal unsigned integer value with 'U' suffix
        unsigned int val_U_int_res = 
          conf.get<unsigned int>("reader", "unsigned_int_U");
        if ( val_U_int_res != 4294967295) { return -1; };

        // test non correct decimal unsigned integer value with 'U' suffix
        std::string val_error_u_int_res = 
          conf.get<std::string>("reader", "error_unsigned_int_U");
        if ( val_error_u_int_res.compare("-12U") != 0) { return -1; };

        // test correct decimal unsigned long value with 'u' suffix
        unsigned long val_u_long_res = 
          conf.get<unsigned long>("reader", "unsigned_long_u");
        if ( val_u_long_res != 18446744073709551614u) { return -1; };

        // test correct decimal unsigned long value with 'u' suffix
        unsigned long val_U_long_res = 
          conf.get<unsigned long>("reader", "unsigned_long_U");
        if ( val_U_long_res != 18446744073709551614u) { return -1; };

        // test correct hexadecimal  unsigned int
        {unsigned int val = 
          conf.get<unsigned int>("reader", "unsigned_hex_int");
        if ( val != 0x80000000) { return -1; }; }

        // test correct hexadecimal  unsigned long
        {unsigned long val = 
          conf.get<unsigned long>("reader", "unsigned_hex_long_int_max");
        if ( val != 0x8000000000000000u) { return -1; }; }


        // test correct decimal max  integer value 
        { int val_int_res = conf.get<int>("reader", "integer_max");
        if ( val_int_res !=  2147483647) { return -1; }; }

        // test correct decimal min  integer value 
        { int val_int_res = conf.get<int>("reader", "integer_min");
        if ( val_int_res != -2147483648) { return -1; }; }

        // test correct min long interger
        { long int val = conf.get<long int>("reader", "long_integer_min");
        if (val != -9223372036854775807) { return -1; } }

        // test correct max long interger
        {long int val = conf.get<long int>("reader", "long_integer_max");
        if (val != 9223372036854775807) { return -1; } }

        // test correct hexadecimal integer value with lower case prefix
        {int hex_integer = conf.get<int>("reader", "hex_integer");
        if (hex_integer != 0x7fffffff) { return -1; } }

        // test correct hexadecimal integer negative value lower case prefix
        {int hex_integer = conf.get<int>("reader", "hex_minus_integer");
        if (hex_integer != -0x2a) { return -1; }} 

std::cout << green << __LINE__ << no_color << std::endl;
        // test correct hexadecimal integer value with upper case prefix
        {int hex_integer_uc = conf.get<int>("reader", "hex_integer_upper_case");
        if (hex_integer_uc != 0x2a) { return -1; }} 

        // test correct hexadecimal long integer value
        {long int val = conf.get<long int>("reader", "hex_long_integer_max");
        if (val != 0x7fffffffffffffff) { return -1; }} 
        // test correct decimal float value 
        {float val_float_res = 
          conf.get<float>("reader", "float");
        if ( val_float_res != 0.125659f) { return -1; }; }

        // test correct decimal float value 
        {float val_float_res = 
          conf.get<float>("reader", "float_without_dec");
        if ( val_float_res != 2.) { return -1; }; }

        // test correct max decimal float value exponential format  
        float val_max_float_exp_res = 
          conf.get<float>("reader", "max_float_exp");
        if ( val_max_float_exp_res != 3.40282e+38f) { return -1; };

        // test correct min decimal float value exponential format  
        float val_min_float_exp_res = 
          conf.get<float>("reader", "min_float_exp");
        if ( val_min_float_exp_res != 1.17550e-38f) { return -1; };

        // test correct negative decimal float value
        float val_neg_float_res = 
          conf.get<float>("reader", "negative_float");
        if ( val_neg_float_res != -0.45221f) { return -1; };

std::cout << green << __LINE__ << no_color << std::endl;
        // test correct negative decimal float minimum value
        float val_neg_float_exp_res = 
          conf.get<float>("reader", "nageative_min_float_exp");
        if ( val_neg_float_exp_res != -1.17550e-38f) { return -1; };

        // test correct decimal double value 
        double val_double_res = 
          conf.get<double>("reader", "double");
        if ( val_double_res != 340283004324324234324242343255834534000.3) 
        { return -1; };

        // test correct decimal double value  exponential format
        double val_float_exp_res = 
          conf.get<double>("reader", "double_exp");
        if ( val_float_exp_res != 3.40283e+38) { return -1; };

        // test correct decimal double negative value  exponential format
        double val_neg_double_exp_res = 
          conf.get<double>("reader", "negative_double_exp");
        if ( val_neg_double_exp_res != -1.79769e+308) { return -1; };

        {long double valld =
          conf.get<long double>("reader", "long_double_max");
        if ( valld != 1.18973e+4932l) { return -1; };}

        // test correct decimal long double min
        {long double valld =
          conf.get<long double>("reader", "long_double_min");
        if ( valld != 3.3621e-4931l) { return -1; };}



        // test correct True boolean value in string format
        {bool val_bool_true = 
          conf.get<bool>("reader", "bool_true");
        if ( val_bool_true != true) { return -1; };}

std::cout << green << __LINE__ << no_color << std::endl;
        // test correct False boolean value in string format
        { bool val_bool_false = 
          conf.get<bool>("reader", "bool_false");
        if ( val_bool_false != false) { return -1; }; }

        // test correct Yes boolean value in string format
        {bool val_bool_true = 
          conf.get<bool>("reader", "bool_yes");
        if ( val_bool_true != true) { return -1; };}

        // test correct no boolean value in string format
        {bool val_bool_false = 
          conf.get<bool>("reader", "bool_no");
        if ( val_bool_false != false) { return -1; }; }

        // test blank value
        try
        { std::string val = 
          conf.get<std::string>("reader", "value_blank");
         return -1;  // This should never be excecuted
        }
        catch (std::runtime_error e) 
        { // normal as blank value cannot be added to Config
        } 

std::cout << green << __LINE__ << no_color << std::endl;
        // test std::vector<int>
        std::vector<int> list_int =
          conf.getVector<int>("reader", "list_int_elem");
        std::vector<int> list_int_ref = { 1,5,7,8 } ;
        if ( list_int != list_int_ref ) { return -1; } 
std::cout << green << __LINE__ << no_color << std::endl;
  
        // test std::vector<int>  hexadecimal format
        { std::vector<int> list_get =
          conf.getVector<int>("reader", "list_int_hex_elem");
        std::vector<int> list_ref = { 0x1,0x5a,0xd,0xF } ;
        if ( list_get != list_ref ) { return -1; } }
std::cout << green << __LINE__ << no_color << std::endl;
  
        // test std::vector<int> // octal format
        { std::vector<int> list_get =
          conf.getVector<int>("reader", "list_int_octal_elem");
        std::vector<int> list_ref = { 01,05,0545454,0652 } ;
        if ( list_get != list_ref ) { return -1; } }
std::cout << green << __LINE__ << no_color << std::endl;

        // test std::vector<std::string>
        std::vector<std::string> list_str =
          conf.getVector<std::string>("reader", "list_str_elem");
        std::vector<std::string> list_str_ref = { "tel1"," tel 2 ","tel5 ","tel7"," tel12"  } ;
std::cout << list_str << std::endl;
std::cout << list_str_ref << std::endl;
        if ( list_str != list_str_ref ) { return -1; } 
  
std::cout << green << __LINE__ << no_color << std::endl;
        // test std::vector<unsigned int>
        { std::vector<unsigned int> list_get =
          conf.getVector<unsigned int>("reader", "list_uint_elem");
        std::vector<unsigned int> list_ref = { 4294967295u,3294967295u
                                            ,2294967295u } ;
        if ( list_get != list_ref ) { return -1; } }
std::cout << green << __LINE__ << no_color << std::endl;

        // test std::vector<unsigned long>
        { std::vector<unsigned  long> list_get =
          conf.getVector<unsigned long>("reader", "list_ulong_elem");
        std::vector<unsigned long> list_ref = { 18446744073709551614u
                                              ,18446344073709551614u } ;
        if ( list_get != list_ref ) { return -1; } }

        // test std::vector<float>
        { std::vector<float> list_get =
          conf.getVector<float>("reader", "list_float_elem");
        std::vector<float> list_ref = { 4.5,7.6,-1.2, 3.40282e+38,1.17550e-38 } ;
        if ( list_get != list_ref ) { return -1; } }

        // test std::vector<float>
        { std::vector<float> list_get =
          conf.getVector<float>("reader", "list_float_elem");
        std::vector<float> list_ref = { 4.5,7.6,-1.2, 3.40282e+38,1.17550e-38 } ;
        if ( list_get != list_ref ) { return -1; } }

        // test std::vector<double>
        { std::vector<double> list_get =
          conf.getVector<double>("reader", "list_double_elem");
        std::vector<double> list_ref = {340283004324324234324242343255834534000.3
                                      ,3.40283e+38,-1.79769e+308 } ;
        if ( list_get != list_ref ) { return -1; } }
std::cout << green << __LINE__ << no_color << std::endl;


        { std::vector<long int> list_get =
          conf.getVector<long int>("reader", "list_longint_elem");
        std::vector<long int>list_ref={-9223372036854775807,9223372036854775807};
        if ( list_get != list_ref ) { return -1; } }

        // test list with mixed UINT and ULONG
        { std::vector<unsigned long > list_get =
          conf.getVector<unsigned long >("reader", "list_mix_ulong");
        std::vector<unsigned long>list_ref={4294967295u,18446744073709551614u};
        if ( list_get != list_ref ) { return -1; } }

        // test list with mixed INT and LONG
        { std::vector<long > list_get =
          conf.getVector<long>("reader", "list_mix_long");
        std::vector<long>list_ref={-1,5,-6,-9223372036854775807,9223372036854775807};
        if ( list_get != list_ref ) { return -1; } }

        // test list with mixed INT and LONG FLOAT
        { std::vector<float > list_get =
          conf.getVector<float>("reader", "list_mix_float");
        std::vector<float>list_ref={(float)-1,-(float)9223372036854775807,2.6};
        if ( list_get != list_ref ) { return -1; } }

        // test list with mixed INT and LONG FLOAT and DOUBLE
        { std::vector<double > list_get =
          conf.getVector<double>("reader", "list_mix_double");
        std::vector<double>list_ref={(double)-1,(double)-9223372036854775807,(double)2.6,-1.79769e+308};
        if ( list_get != list_ref ) { return -1; } }

        // test list with mixed INT and LONG FLOAT DOUBLE and LONGDOUBLE 
        { std::vector<long double > list_get =
          conf.getVector<long double>("reader", "list_mix_long_double");
        std::vector<long double>list_ref={(long double)-1,(long double)-9223372036854775807,(long double)2.6,(long double)-1.79769e+308,1.18973e+4932l};}

        { std::vector<bool> list_get =
          conf.getVector<bool>("reader", "list_boolean_elem");
        std::vector<bool>list_ref={true,false,1,0};
        if ( list_get != list_ref ) { return -1; } }
        
std::cout << green << __LINE__ << no_color << std::endl;

        // Test Custom class
        std::string val_str_pt = conf.get<std::string>("Geo", "center"); 
        Point myPoint(val_str_pt);
        if (myPoint.name().compare("o_point") != 0) { return -1; }
        if (myPoint.x() != 3.2) { return -1; }
        if (myPoint.y() != -432.2) { return -1; }
        if (myPoint.z() != 4) { return -1; }

      }
      catch (std::bad_cast& e)  {
        std::cout << yellow << "CastExeption: " << e.what() << no_color << std::endl;
        return -1;
      }
      catch (std::exception& e)  {
        std::cout << light_red  <<"catch exception in ConfigService.cpp yes, really: " << e.what() << no_color << std::endl;

      return -1;
      }

    return 0;
}
         

