CC=g++
AR=ar
ARFLAGS=rcs
CCFLAGS=-ggdb
OUTPUT_DIR=o
SRC_DIR=src
OUT_STAT=$(OUTPUT_DIR)/libstat.o
LIB_STAT=$(OUTPUT_DIR)/libstat.a
LIB_STAT_SRC=$(wildcard $(SRC_DIR)/*.cpp)
LIB_STAT_INC=-Iinclude -Isrc

all: $(OUTPUT_DIR) $(OUT_STAT) $(LIB_STAT)

$(OUT_STAT): $(LIB_STAT_SRC)
	$(CC) $(CCFLAGS) $(LIB_STAT_INC) -o $@ -c $^

$(LIB_STAT): $(OUT_STAT)
	$(AR) $(ARFLAGS) $@ $^

$(OUTPUT_DIR): 
	@mkdir -p $(OUTPUT_DIR)

clean:
	rm -rf $(LIB_STAT) $(OUT_STAT) *~ $(SRC_DIR)/*.*~ $(OUTPUT_DIR)

.PHONY = clean all
