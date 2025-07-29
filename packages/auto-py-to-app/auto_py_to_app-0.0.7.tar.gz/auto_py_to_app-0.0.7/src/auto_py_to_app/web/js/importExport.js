const importConfiguration = (configuration) => {
    // TODO Check for version to support older versions

    // Re-init UI by clearing everything (copy the array first as it will be mutated during the iteration)
    [...configurationCleaners].forEach(cleaner => cleaner());

    configuration.cxfreezeOptions.forEach(({ optionDest, value }) => {
        if (configurationSetters.hasOwnProperty(optionDest)) {
            configurationSetters[optionDest](value);
        } else {
            // TODO Warn user?
            // TODO noconfirm is expected to come here
        }
    });

    // setup nonCxFreezeOptions
    recursionLimitToggle(configuration.nonCxFreezeOptions.increaseRecursionLimit);
    document.getElementById('raw-arguments').value = configuration.nonCxFreezeOptions.manualArguments;
    if ('outputDirectory' in configuration.nonCxFreezeOptions) {
        document.getElementById('output-directory').value = configuration.nonCxFreezeOptions.outputDirectory;
    }
};

const _collectDataToExport = () => {
    const nonCxFreezeConfiguration = getNonCxFreezeConfiguration();
    delete nonCxFreezeConfiguration.outputDirectory; // This does not need to be saved in the config

    return {
        version: "auto-py-to-app-configuration_v1",
        cxfreezeOptions: getCurrentConfiguration(),
        nonCxFreezeOptions: nonCxFreezeConfiguration
    }
};

const onConfigurationImport = async () => {
    if (!isCommandDefault()) {
        const response = await displayModal(
            getTranslation('dynamic.modal.configModalTitle'),
            getTranslation('dynamic.modal.configModalDescription'),
            [
                getTranslation('dynamic.modal.configModalConfirmButton'),
                getTranslation('dynamic.modal.configModalCancelButton')
            ]);

        if (response !== getTranslation('dynamic.modal.configModalConfirmButton'))
            return;
    }

    const data = await eel.import_configuration()();
    importConfiguration(data);
};

const onConfigurationExport = async () => {
    const data = _collectDataToExport();
    await eel.export_configuration(data)();
};
