APP=statsGet
SRC=$(APP).h
SOAPCC=soapcpp2
CCFLAGS=-DWITH_GZIP
CC=g++
CLI=ws_client
CLI_SRC=$(CLI).cpp
LIBSTAT_PATH=../../libstat
LIBSTAT_LIB_PATH=$(LIBSTAT_PATH)/o
LIBSTAT_LIB=stat
LIBSTAT_INC=$(LIBSTAT_PATH)/include

#SOAP_OUT=$(APP).nsmap $(APP).wsdl ns.xsd soap$(APP)Object.h soap$(APP)Proxy.h soapC.cpp soapClient.cpp soapClientLib.cpp soapH.h soapServer.cpp soapServerLib.cpp soapStub.h soapObject.h soapProxy.h ns2.nsmap ns2.wsdl ns2.xsd soap$(APP)Service.cpp soap$(APP)Service.h
SOAP_OUT=$(APP).nsmap ns.xsd soap$(APP)Object.h soap$(APP)Proxy.h soapC.cpp soapClient.cpp soapClientLib.cpp soapH.h soapServer.cpp soapServerLib.cpp soapStub.h soapObject.h soapProxy.h ns2.nsmap ns2.xsd soap$(APP)Service.cpp soap$(APP)Service.h

INC_DIR=/usr/include/gsoap/import

all: soap build buildcli

clean: soapclean cleanall cleancgi cleanxml cleancli

soap: $(SRC)
	$(SOAPCC)  $(SRC) -I$(INC_DIR)

soapclean:
	rm -f $(SOAP_OUT)

cleancgi:
	rm -f *.cgi

cleanall:
	rm -f *~

cleanxml:
	rm -f *.xml

cleancli:
	rm -f $(CLI)

build: $(APP)Cgi.cpp
	$(CC) $(CCFLAGS) -o $(APP).cgi -I. -I$(LIBSTAT_INC) $(APP)Cgi.cpp soapC.cpp soapServer.cpp -lgsoap++ -L${LIBSTAT_LIB_PATH} -l${LIBSTAT_LIB}

buildcli:
	$(CC) -o $(CLI) soapC.cpp soapClient.cpp $(CLI_SRC) -lgsoap++

.PHONY = all clean soap soapclean cleancgi cleanall cleanxml cleancli build buildcli
