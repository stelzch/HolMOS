#include "camdiscovery.h"

CamDiscovery::CamDiscovery(QObject *parent) : QObject(parent)
{
    socket = new QUdpSocket();
    socket->bind(QHostAddress::Any, 13654);
    connect(socket, SIGNAL(readyRead()), this, SLOT(processDatagrams()));
}

void CamDiscovery::processDatagrams() {
    while(socket->hasPendingDatagrams()) {
        QByteArray data;
        data.resize(socket->pendingDatagramSize());
        QHostAddress sender;
        quint16 senderPort;

        socket->readDatagram(data.data(), data.size(), &sender, &senderPort);

        QString message(data);
        if(message.startsWith("RASPBERRY DISCOVERY")) {
            QStringList messageComponents = message.split(":");
            if(messageComponents.size() != 2) {
                qDebug() << "Discovery message doesn't contain metadata: " << message;
                return;
            }
            QStringList portList = messageComponents.at(1).split(",");
            if(portList.length() != 2) {
                qDebug() << "Discovery message is malformed: " << message;
                return;
            }
            quint16 videoPort = portList.at(0).toUInt();
            quint16 controlPort = portList.at(1).toUInt();
            if(videoPort == 0 || controlPort == 0 || videoPort > 65535 || controlPort > 65535) {
                // Check for string to int conversion errors and invalid port numbers
                qDebug() << "Invalid port numbers. VideoPort: " << videoPort << " ControlPort: " << controlPort;
                return;
            }
            qDebug() << "Ports: " << videoPort << " and " << controlPort;
            emit camDiscovered(sender, videoPort, controlPort);
        } else {
            qDebug() << "Received " << message << " from " << sender.toString() << ":" << senderPort;
        }
    }
}
