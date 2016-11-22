#include "camcontrol.h"

CamControl::CamControl(QObject *parent, QHostAddress addr, quint16 port) : QObject(parent)
{
    manager = new QNetworkAccessManager();
    this->addr = addr;
    this->port = port;
}
QString CamControl::sendMessage(QString message) {
    QUrl url("http://"+addr.toString()+":"+QString::number(port)+"/about");
    qDebug() << "Requesting "+url.toString();
    QNetworkRequest request(url);
    QNetworkReply *reply = manager->get(request);
    QEventLoop eventLoop;
    QObject::connect(reply, SIGNAL(finished()), &eventLoop, SLOT(quit()));
    eventLoop.exec();
    QString result = reply->readAll();
    reply->waitForReadyRead(20000);
    qDebug() << "Result: " << result;

    reply->deleteLater();

}
