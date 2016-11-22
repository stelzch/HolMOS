#include "connectdialog.h"
#include "ui_connectdialog.h"

#include <QLineEdit>

ConnectDialog::ConnectDialog(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::ConnectDialog)
{
    ui->setupUi(this);
}

ConnectDialog::~ConnectDialog()
{
    delete ui;
}
void ConnectDialog::parseInput() {
    hostname = this->ui->ipEdit->text();
    portNumber = this->ui->portEdit->text().toInt();
}
