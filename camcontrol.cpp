#include "camcontrol.h"

CamControl::CamControl(QObject *parent, QHostAddress addr, quint16 port) : QObject(parent)
{
    socket = new QUdpSocket();
    this->addr = addr;
    this->port = port;
    socket->connectToHost(addr, port);
}
QString CamControl::sendMessage(QString message) {
    socket->write(message.toStdString().c_str(), message.length());
}
