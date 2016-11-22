#ifndef CAMCONTROL_H
#define CAMCONTROL_H

#include <QObject>
#include <QTcpSocket>
#include <QHostAddress>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QEventLoop>

class CamControl : public QObject
{
    Q_OBJECT
public:
    explicit CamControl(QObject *parent = 0, QHostAddress addr=QHostAddress::LocalHost, quint16 port=8000);
    QString sendMessage(QString message);
signals:

public slots:

private:
    QNetworkAccessManager *manager;
    QTcpSocket *socket;
    QHostAddress addr;
    quint16 port;
};

#endif // CAMCONTROL_H
