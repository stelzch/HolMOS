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

    QImage blackframe = QImage(640, 480, QImage::Format_RGB888);
    //blackframe.fil
    blackframe.fill(Qt::black);
    displayFrame(blackframe);

    cam = new Cam();
    QObject::connect(cam, SIGNAL(camFound(QString)), this, SLOT(camFound(QString)));
    videoThread = new VideoThread(this);
    QObject::connect(videoThread, SIGNAL(frameReceived(QImage)), this, SLOT(displayFrame(QImage)));
    QObject::connect(ui->brightnessSlider, SIGNAL(valueChanged(int)), this, SLOT(setIntParameter(int)));
    QObject::connect(ui->contrastSlider, SIGNAL(valueChanged(int)), this, SLOT(setIntParameter(int)));
    QObject::connect(ui->isoCombo, SIGNAL(activated(QString)), this, SLOT(setStrParameter(QString)));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::displayFrame(QImage image) {
    connected = true;
    frames++;
    ui->label->setPixmap(QPixmap::fromImage(image));
    ui->statusBar->showMessage("Showing frame "+QString::number(frames));
}

void MainWindow::camFound(QString url) {
    qDebug() << "Activating cam";
    if(videoThread->isRunning())
        videoThread->requestInterruption();
    videoThread->setUrl(url);
    videoThread->start();
}
void MainWindow::setIntParameter(int value) {
    QObject *sender = QObject::sender();
    if(sender == ui->brightnessSlider) {
        qDebug() << "Setting brightness to " << value;
        cam->setBrightness(value);
    } else if(sender == ui->contrastSlider) {
        qDebug() << "Setting contrast to " << value;
        cam->setContrast(value);
    }
}
void MainWindow::setStrParameter(QString value) {
    QObject *sender = QObject::sender();
    if(sender == ui->isoCombo) {
        cam->setIso(value);
    }
}
