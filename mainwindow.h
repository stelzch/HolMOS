#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "connectdialog.h"
#include "videothread.h"
#include "cam.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void displayFrame(QImage);
    void connect(bool);
    void disconnect();
    void camFound(QString url);

private:
    Ui::MainWindow *ui;
    VideoThread *videoThread;
    bool connected;
    ConnectDialog *connectDialog;
    Cam *cam;
};

#endif // MAINWINDOW_H
