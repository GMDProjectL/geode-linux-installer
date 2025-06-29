#ifndef INSTALLATIONMETHODPAGE_H
#define INSTALLATIONMETHODPAGE_H

#include <QWidget>
#include <QMessageBox>

namespace Ui {
class InstallationMethodPage;
}

class InstallationMethodPage : public QWidget
{
    Q_OBJECT

public:
    explicit InstallationMethodPage(QWidget *parent = nullptr);
    ~InstallationMethodPage();

signals:
    void selectedWine();
    void selectedSteam();

public slots:
    void winePressed();
    void steamPressed();

public slots:
    void hintPressed();

private:
    Ui::InstallationMethodPage *ui;
};

#endif // INSTALLATIONMETHODPAGE_H
