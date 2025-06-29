#include "mainpage.h"
#include "ui/ui_mainpage.h"

MainPage::MainPage(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::MainPage)
{
    ui->setupUi(this);
    connect(ui->pushButton, &QPushButton::clicked, this, &MainPage::startButtonPressed);
}

void MainPage::startButtonPressed() {
    emit startInstallation();
}

MainPage::~MainPage()
{
    delete ui;
}
