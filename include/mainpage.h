#ifndef MAINPAGE_H
#define MAINPAGE_H

#include <QWidget>

namespace Ui {
class MainPage;
}

class MainPage : public QWidget
{
    Q_OBJECT

public:
    explicit MainPage(QWidget *parent = nullptr);
    ~MainPage();

signals:
    void startInstallation();

public slots:
    void startButtonPressed();

private:
    Ui::MainPage *ui;
};

#endif // MAINPAGE_H
