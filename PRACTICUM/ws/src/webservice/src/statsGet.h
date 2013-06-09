//File: bikeGet.h
//gsoap ns2 service name: statsGet
//gsoap ns2 service namespace: urn: statsGet
//gsoap ns2 service location: http://localhost:12345
/** gsoap ns2 service location: http://sarroutbi.dyndns.org/statsGet.cgi **/
#import "stlvector.h"

class guiltyStat
{
  char*  date;
  char*  file;
  char*  author;
  double loc;
};

int ns2__statsGet(char* date, char* file, char* author, guiltyStat & stat);
