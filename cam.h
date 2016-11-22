#ifndef CAM_H
#define CAM_H

#include <QObject>
#include <QHostAddress>

#include "camdiscovery.h"

class Cam : public QObject
{
    Q_OBJECT
public:
    explicit Cam(QObject *parent = 0);

signals:
    void camFound(QString videoUrl);
public slots:
    void discoveryReceived(QHostAddress, quint16, quint16);
private:
    quint16 videoPort;
    quint16 controlPort;
    QHostAddress hostname;
    CamDiscovery *discovery;
};

#endif // CAM_H
