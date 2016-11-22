#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <QLabel>
#include <QAction>
#include <QObject>
#include <QStatusBar>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    connected = false;

    QObject::connect(ui->actionVerbinden, SIGNAL(triggered(bool)), this, SLOT(connect(bool)));
    connectDialog = new ConnectDialog();
    QObject::connect(ui->actionTrennen, SIGNAL(triggered(bool)), this, SLOT(disconnect()));

    QImage blackframe = QImage(640, 480, QImage::Format_RGB888);
    blackframe.fill(Qt::black);
    displayFrame(blackframe);

    cam = new Cam();
    QObject::connect(cam, SIGNAL(camFound(QString)), this, SLOT(camFound(QString)));
    videoThread = new VideoThread(this);
    QObject::connect(videoThread, SIGNAL(frameReceived(QImage)), this, SLOT(displayFrame(QImage)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::displayFrame(QImage image) {
    connected = true;
    qDebug() << "Received frame";
    ui->label->setPixmap(QPixmap::fromImage(image));
}

void MainWindow::connect(bool checked) {
    Q_UNUSED(checked)
    if(connectDialog->exec() == QDialog::Accepted) {
       QString url("udp://");
       url.append(connectDialog->hostname);
       url.append(":");
       url.append(QString::number(connectDialog->portNumber));
       ui->statusBar->showMessage(tr("Verbinde mit '")+url+"'...");
       ui->actionVerbinden->setEnabled(false);
       ui->actionTrennen->setEnabled(true);
       //videoThread = new VideoThread(this, url.toStdString().c_str());
       QObject::connect(videoThread, SIGNAL(frameReceived(QImage)), this, SLOT(displayFrame(QImage)));
       videoThread->start();
    }
}
void MainWindow::camFound(QString url) {
    qDebug() << "Activating cam";
    if(videoThread->isRunning())
        videoThread->requestInterruption();
    videoThread->setUrl(url);
    videoThread->start();
}

void MainWindow::disconnect() {
    ui->actionTrennen->setEnabled(false);
    ui->actionVerbinden->setEnabled(true);
    videoThread->requestInterruption();
}
