#ifndef CAMCONTROL_H
#define CAMCONTROL_H

#include <QObject>
#include <QHostAddress>
#include <QUdpSocket>

class CamControl : public QObject
{
    Q_OBJECT
public:
    explicit CamControl(QObject *parent = 0, QHostAddress addr=QHostAddress::LocalHost, quint16 port=8000);
    QString sendMessage(QString message);
signals:

public slots:

private:
    QUdpSocket *socket;
    QHostAddress addr;
    quint16 port;
};

#endif // CAMCONTROL_H
