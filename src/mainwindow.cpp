#include "mainwindow.h"
#include "ui/ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    mainPage = new MainPage(ui->stackedWidget);

    ui->stackedWidget->addWidget(mainPage);
    ui->stackedWidget->setCurrentWidget(mainPage);

    connect(mainPage, &MainPage::startInstallation, this, &MainWindow::goToInstallationMethodPage);
}

void MainWindow::goToInstallationMethodPage()
{
    installationMethodPage = new InstallationMethodPage(ui->stackedWidget);

    ui->stackedWidget->addWidget(installationMethodPage);
    ui->stackedWidget->setCurrentWidget(installationMethodPage);

    connect(
        installationMethodPage, &InstallationMethodPage::selectedSteam,
        this, &MainWindow::goToSteamInstallPage
        );

    connect(
        installationMethodPage, &InstallationMethodPage::selectedWine,
        this, &MainWindow::goToWineInstallPage
        );
}

void MainWindow::goToSteamInstallPage()
{
    QMessageBox::information(this, "steam", "wip");
}

void MainWindow::goToWineInstallPage()
{
    QMessageBox::information(this, "wine", "wip");
}

MainWindow::~MainWindow()
{
    delete ui;
    delete mainPage;

    if (installationMethodPage != nullptr) {
        delete installationMethodPage;
    }
}
