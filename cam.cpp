#include "cam.h"

Cam::Cam(QObject *parent) : QObject(parent)
{
    discovery = new CamDiscovery();
    connect(discovery, SIGNAL(camDiscovered(QHostAddress,quint16,quint16)), this, SLOT(discoveryReceived(QHostAddress,quint16,quint16)));
}
void Cam::discoveryReceived(QHostAddress addr, quint16 videoPort, quint16 controlPort) {
    qDebug() << "Found cam";

    // Exit if the message was repeated and ports didn't change
    if(videoPort == this->videoPort && controlPort == this->controlPort)
        return;
    this->videoPort = videoPort;
    this->controlPort = controlPort;
    this->hostname = addr;

    QString url("udp://:"+QString::number(videoPort));
    qDebug() << "Camera Url: " << url;
    emit camFound(url);
}
