CBPREFIX = /SFCB
CB_SRC = $(PRJ_PATH)/SFCB
CBEXECPREFIX =  $(CBPREFIX)/local
CBINCDIR = $(CB_SRC)/sblim-sfcb-1.3.2
CBLIBDIR = $(CBEXECPREFIX)/lib
INSTALLDIR = $(CBEXECPREFIX)/lib/cmpi

SONAME = libcmpiIPMI_TextRedirectionServiceProvider.so
LIBNAME = libcmpiIPMI_TextRedirectionServiceProvider.so.4
TARGET = $(SONAME)

#ifdef (DEBUG)
DEBUGFLAGS = -g -DDEBUG
#else
#DEBUGFLAGS =
#endif

DEFS = -D_REENTRANT
LIBS = -lpthread -L$(CBLIBDIR)
LIB += -lmulti

INCLUDES = -I$(CBINCDIR)
CXX = $(CROSS_COMPILE)gcc
CXXFLAGS = $(DEBUGFLAGS) $(INCLUDES) $(DEFS) -Wall -fPIC -DCMPI_PLATFORM_LINUX_GENERIC_GNU


SRCS = \
cmpiIPMI_TextRedirectionServiceProvider.c \
cmpiIPMI_TextRedirectionService.c \
IPMI_TextRedirectionService.c


OBJS = $(addsuffix .o, $(basename $(SRCS)))

.SUFFIXES : .o .c

all:      $(LIBNAME)

$(LIBNAME):     $(OBJS)
	$(CXX) -shared -Wl,-soname,$(SONAME) -o $(LIBNAME) $(OBJS) $(LDFLAGS)
	$(STRIP) $(LIBNAME)
	ln -s $(LIBNAME) $(SONAME)

.c.o:
	$(CXX) $(CXXFLAGS) -c $< -o $@