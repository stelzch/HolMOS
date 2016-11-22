#include "mainwindow.h"
#include "camcontrol.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
//    CamControl cc(0, QHostAddress("169.254.71.178"), 8008);
//    qDebug() << cc.sendMessage("about");
    QStringList libraryPaths("libs");
    a.setLibraryPaths(libraryPaths);
    MainWindow w;
    w.show();

    return a.exec();
}
