#ifndef CONNECTDIALOG_H
#define CONNECTDIALOG_H

#include <QDialog>

namespace Ui {
class ConnectDialog;
}

class ConnectDialog : public QDialog
{
    Q_OBJECT

public:
    explicit ConnectDialog(QWidget *parent = 0);
    QString getHostname();
    int getPort();
    ~ConnectDialog();
    QString hostname;
    int portNumber;
public slots:
    void parseInput();
private:
    Ui::ConnectDialog *ui;
};

#endif // CONNECTDIALOG_H
