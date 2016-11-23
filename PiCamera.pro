#-------------------------------------------------
#
# Project created by QtCreator 2016-11-18T18:19:44
#
#-------------------------------------------------

QT       += core gui network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = PiCamera
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    videothread.cpp \
    camdiscovery.cpp \
    cam.cpp \
    camcontrol.cpp

HEADERS  += mainwindow.h \
    videothread.h \
    camdiscovery.h \
    cam.h \
    camcontrol.h

FORMS    += mainwindow.ui

CONFIG += static
unix: CONFIG += link_pkgconfig
unix: PKGCONFIG += libavcodec libswscale libavutil libavformat
linux-g++-32: LIBS += -L/opt/ffmpeg-static/lib -lswscale -lm -lavformat -ldl -lxcb -lxcb-shm -lxcb-xfixes -lxcb-shape -lX11 -lm -llzma -lbz2 -lz -pthread -lavcodec -ldl -lxcb -lxcb-shm -lxcb-xfixes -lxcb-shape -lX11 -lm -llzma -lbz2 -lz -pthread -lswresample -lm -lavutil -lm

CONFIG += staticlib
win32:
win32: CONFIG += link_pkgconfig
win32: PKGCONFIG += libavcodec libswscale libavutil libavformat
#win32: LIBS += -lswscale -lavformat -lavcodec -lavicap32 -lstrmiids -luuid -loleaut32 -lsecur32 -lmingw32 -lSDLmain -lSDL -mwindows -luser32 -ldxguid -lxvidcore -lx264 -lvpx -lpthread -lvorbisenc -lvorbis -lvo-amrwbenc -lvidstab -ltheoraenc -ltheoradec -logg -lspeex -lopus -lopencore-amrwb -lopencore-amrnb -lmp3lame -lcaca -lncurses -lglut -lglu32 -lopengl32 -lbs2b -lbluray -lxml2 -lass -lfribidi -lharfbuzz -lcairo -lgobject-2.0 -lfontconfig -lusp10 -lmsimg32 -lgdi32 -lpixman-1 -L/home/cstelz/Software/Builds/mxe/usr/i686-w64-mingw32.static/lib/../lib -lffi -lexpat -lfreetype -lpng16 -lharfbuzz_too -lglib-2.0 -lole32 -lwinmm -lshlwapi -lpcre -lgnutls -lhogweed -lnettle -lidn /home/cstelz/Software/Builds/mxe/usr/i686-w64-mingw32.static/lib/libz.a /home/cstelz/Software/Builds/mxe/usr/i686-w64-mingw32.static/lib/libiconv.a -lws2_32 -lcrypt32 -lgmp -lintl -liconv -llzma -lbz2 -lz -lpsapi -ladvapi32 -lshell32 -mconsole -lswresample -L/home/cstelz/Software/Builds/mxe/usr/i686-w64-mingw32.static/lib  -lavutil -lm
