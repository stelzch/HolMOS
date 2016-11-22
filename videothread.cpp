#include "videothread.h"
#include <QTime>


VideoThread::VideoThread(QObject *parent) : QThread(parent)
{
}
void VideoThread::setUrl(QString url) {
    this->url = url;
}

void VideoThread::run() {
    // Initialize ffmpeg libraries
    av_register_all();

    // Initialize network
    avformat_network_init();

    if(avformat_open_input(&formatCtx, url.toStdString().c_str(), NULL, 0) != 0) {
        qDebug() << "Couldn't open video url";
        // Should abort now!
    }

    if(avformat_find_stream_info(formatCtx, NULL)<0) {
        qDebug() << "Couldn't read stream info!";
        // Should abort now!
    }
    av_dump_format(formatCtx, 0, url.toStdString().c_str(), 0);

    if(formatCtx->nb_streams != 1) {
        qDebug() << "Contains wrong number of streams";
        // Should abort now!
    }

    codecCtx = formatCtx->streams[0]->codec;

    codec = avcodec_find_decoder(codecCtx->codec_id);
    if(codec == NULL) {
        qDebug() << "Couldn't find codec";
        // Should abort now
    }

    if(avcodec_open2(codecCtx, codec, &opts)<0) {
        qDebug() << "Couldn't open codec";
        // Should abort now
    }
    frame = av_frame_alloc();
    framerate = codecCtx->framerate.num;

    // Prepare image conversion
    swsCtx = sws_getContext(codecCtx->width, codecCtx->height, codecCtx->pix_fmt, codecCtx->width, codecCtx->height,
                            AV_PIX_FMT_RGB24, SWS_BICUBIC, NULL, NULL, NULL);
    //lastFrame.start();

    // Framerate Calculations
    waitTime = (1.0/framerate)*1000;
    qDebug() << waitTime;
    qDebug() << "Framerate: " << framerate;



    AVPacket packet;

    int frameFinished, frames=0;
    QImage img(codecCtx->width, codecCtx->height, QImage::Format_RGB888);
    AVFrame *frameRGB;
    frameRGB = av_frame_alloc();
    avpicture_alloc( (AVPicture *) frameRGB, AV_PIX_FMT_RGB24, codecCtx->width, codecCtx->height);
    while(av_read_frame(formatCtx, &packet)>=0) {

        // The Thread should exit now
        if(QThread::currentThread()->isInterruptionRequested()) {
            break;
        }
        avcodec_decode_video2(codecCtx, frame, &frameFinished, &packet);
        qDebug() << "Received packet" << endl;
        if(frameFinished) {
            // Convert frame to RGB24
            sws_scale(swsCtx, frame->data, frame->linesize, 0, codecCtx->height, frameRGB->data, frameRGB->linesize);

            // Load into QImage
            for(int y=0; y < frame->height; ++y) {
                memcpy(img.scanLine(y), frameRGB->data[0]+ y*frameRGB->linesize[0], frameRGB->linesize[0]);
            }
            frames++;
            emit frameReceived(img);

            qDebug() << "Finished Frame #" << frames++;
        }
        av_free_packet(&packet);
    }
    qDebug() << "Closing input";
    av_free(frame);
    avcodec_close(codecCtx);
    avformat_close_input(&formatCtx);
}
VideoThread::~VideoThread() {

}
