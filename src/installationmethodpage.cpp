#include "installationmethodpage.h"
#include "ui/ui_installationmethodpage.h"

InstallationMethodPage::InstallationMethodPage(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::InstallationMethodPage)
{
    ui->setupUi(this);
    connect(ui->differenceLink, &QLabel::linkActivated, this, &InstallationMethodPage::hintPressed);
    connect(ui->steamButton, &QPushButton::pressed, this, &InstallationMethodPage::steamPressed);
    connect(ui->wineButton, &QPushButton::pressed, this, &InstallationMethodPage::winePressed);
}

void InstallationMethodPage::steamPressed()
{
    emit selectedSteam();
}

void InstallationMethodPage::winePressed()
{
    emit selectedWine();
}

void InstallationMethodPage::hintPressed()
{
    QMessageBox::information(
        this, "Explaination",
        "If you installed Geometry Dash through Steam, it's pretty much straightforward. "
        "If you installed Geometry Dash using Wine, you need to specify the path to the prefix and the game itself."
    );
}

InstallationMethodPage::~InstallationMethodPage()
{
    delete ui;
}
