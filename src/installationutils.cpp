#include "installationutils.h"


InstallationUtils* InstallationUtils::get()
{
    static InstallationUtils instance;
    return &instance;
}
