#include "cam.h"

Cam::Cam(QObject *parent) : QObject(parent)
{
    control = NULL;
    discovery = new CamDiscovery();
    connect(discovery, SIGNAL(camDiscovered(QHostAddress,quint16,quint16)), this, SLOT(discoveryReceived(QHostAddress,quint16,quint16)));
}
void Cam::discoveryReceived(QHostAddress addr, quint16 videoPort, quint16 controlPort) {

    // Exit if the message was repeated and ports didn't change
    if(videoPort == this->videoPort && controlPort == this->controlPort)
        return;
    qDebug() << "Found cam";
    this->videoPort = videoPort;
    this->controlPort = controlPort;
    this->hostname = addr;

    control = new CamControl(this, addr, controlPort);

    QString url("udp://:"+QString::number(videoPort));
    qDebug() << "Camera Url: " << url;
    emit camFound(url);
}
void Cam::setBrightness(int brightness) {
    if(control != NULL) {
        control->sendMessage("RASPBERRY brightness="+QString::number(brightness));
    }
}
void Cam::setContrast(int contrast) {
    if(control != NULL) {
        control->sendMessage("RASPBERRY contrast="+QString::number(contrast));
    }
}
void Cam::setIso(QString iso) {
    if(control != NULL) {
        control->sendMessage("RASPBERRY iso="+iso);
    }
}
