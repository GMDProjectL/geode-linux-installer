#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "mainpage.h"
#include "installationmethodpage.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void goToInstallationMethodPage();
    void goToSteamInstallPage();
    void goToWineInstallPage();

private:
    Ui::MainWindow *ui;
    MainPage *mainPage;
    InstallationMethodPage *installationMethodPage;
};
#endif // MAINWINDOW_H
