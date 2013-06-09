#include "soapH.h"
#include "statsGet.nsmap"

const uint8_t MAX_POST_FIELD=255;

void logResponse(const guiltyStat & gs)
{
  std::cout << "===================================================="
            << "====================================================" 
            << std::endl;
  std::cout << "Author   :" << gs.author << std::endl;
  std::cout << "File     :" << gs.file << std::endl;
  std::cout << "Date     :" << gs.date << std::endl;
  std::cout << "LOC      :" << gs.loc << std::endl;
  std::cout << "===================================================="
            << "====================================================" 
            << std::endl;

}

void usage(char* argv, uint8_t err)
{
  if(argv)
  {
    fprintf(stderr, "\n");
    fprintf(stderr, "%s: ", argv);
    fprintf(stderr, "	%s -d\"date\" [-a[\"author\"] \
                    [-f\"file\"]", argv);
    fprintf(stderr, "\n");
  }
  exit(err);
}

void parseArgs(int argc, char* argv[], char* date, uint32_t date_max,
               char* file, uint32_t file_max, char* author, 
               uint32_t author_max)
{
  int8_t  c = 0;
  uint8_t opterr = 0;
     
  while ((c = getopt (argc, argv, "d:a:f:h")) != -1)
  {
    switch (c)
    {
      case 'd':
        strncpy(date, optarg, date_max);
        break;
      case 'a':
        strncpy(author, optarg, author_max);
        break;
      case 'f':
        strncpy(file, optarg, file_max);
        break;
      default:
        usage (argv[0], 1);
    }
  }
  return;
}

int main(int argc, char* argv[])
{
  guiltyStat gs;
  struct soap *soap = soap_new();
  char date   [MAX_POST_FIELD] = "";
  char file   [MAX_POST_FIELD] = "";
  char author [MAX_POST_FIELD] = "";
 
  parseArgs(argc, argv, date, MAX_POST_FIELD, file, MAX_POST_FIELD, 
            author, MAX_POST_FIELD);

  if(soap_call_ns2__statsGet(soap, NULL, NULL, date, file, author, gs)
     == SOAP_OK)
  {
    logResponse(gs);
  }
  else
  {
    soap_print_fault(soap, stderr);
  }
  soap_end(soap);
  soap_free(soap);
  return 0;
}
