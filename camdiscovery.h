#ifndef CAMDISCOVERY_H
#define CAMDISCOVERY_H

#include <QObject>
#include <QUdpSocket>
#include <QStringList>

class CamDiscovery : public QObject
{
    Q_OBJECT
public:
    explicit CamDiscovery(QObject *parent = 0);
signals:
    void camDiscovered(QHostAddress, quint16, quint16);
public slots:
    void processDatagrams();
private:
    QUdpSocket *socket;
};

#endif // CAMDISCOVERY_H
