#include <stdlib.h>
#include <stdint.h>

#include "soapH.h" 
#include "statsGet.nsmap"

// libstat include files
#include "libstat.h"

int main(int argc, char* argv[])
{
  // master/slave sockets
  int m;
  int s;
  // soap struct
  struct soap *soap = soap_new();
  // create soap context and serve one CGI-based request:
  if (argc < 2) {
    // serve as CGI application
    soap_serve(soap);
  }
  else { 
    m = soap_bind(soap, NULL, atoi(argv[1]), 100);
    if (m < 0) { 
      soap_print_fault(soap, stderr);
      exit(-1);
    }
    while(1) { 
      s = soap_accept(soap);
      fprintf(stderr, "Socket connection successful: slave socket = %d\n", s);
      if (s < 0) { 
        soap_print_fault(soap, stderr);
        exit(1);
      } 
      soap_serve(soap);
      soap_end(soap);
    }
  }
  soap_done(soap);
  free(soap);
  return 0;
  soap_serve(soap_new());
}

int ns2__statsGet(struct soap *soap, char* date, char* file,
                  char* author, guiltyStat & response)
{
  soap_set_omode(soap, SOAP_ENC_ZLIB);
  soap->z_level = 9; // best compression
  LibStat ls(date, file, author);
  uint64_t loc;
  loc = ls.getLOCs();
  response.date   = date;
  response.file   = file;
  response.author = author;
  response.loc    = loc;
  return SOAP_OK;
}
