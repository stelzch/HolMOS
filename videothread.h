#ifndef VIDEOTHREAD_H
#define VIDEOTHREAD_H

#include <QObject>
#include <QDebug>
#include <QThread>
#include <QImage>
#include <QTime>

// Include ffmpeg libraries
extern "C" {
    #include <libavcodec/avcodec.h>
    #include <libavformat/avformat.h>
    #include <libswscale/swscale.h>
    #undef main
}

class VideoThread : public QThread
{
    Q_OBJECT
    void run() Q_DECL_OVERRIDE;
public:
    VideoThread(QObject *parent);
    void setUrl(QString url);
    virtual ~VideoThread();
    long framerate;
signals:
    void frameReceived(QImage);
private:
    QString url;
    AVFormatContext *formatCtx = NULL;
    AVCodecContext *codecCtx = NULL;
    AVCodec *codec = NULL;
    AVDictionary *opts = NULL;
    AVFrame *frame;
    struct SwsContext *swsCtx = NULL;
    QTime lastFrame;
    int waitTime;
};

#endif // VIDEOTHREAD_H
