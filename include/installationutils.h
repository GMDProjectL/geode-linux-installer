#ifndef INSTALLATIONUTILS_H
#define INSTALLATIONUTILS_H
#include <QString>

class InstallationUtils {
public:
    static InstallationUtils* get();

    void downloadGeode(QString outPath);
    void unpackGeode(QString zipPath, QString outPath);

    void installForSteam();
    void installForWine(QString winePrefix, QString gdPath);
};

#endif // INSTALLATIONUTILS_H
