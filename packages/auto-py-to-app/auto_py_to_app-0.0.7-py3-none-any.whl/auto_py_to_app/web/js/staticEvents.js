/*
Handle user events
*/

// Top level inputs

const scriptLocationChange = async (event) => {
    colourInput(event.target, false, true, false);
    updateCurrentCommandDisplay();
};

const targetLocationChange = async (event) => {
    colourInput(event.target, false, false, true);
    updateCurrentCommandDisplay();
};

const scriptLocationSearch = async (event) => {
    const entryScriptNode = document.getElementById('entry-script');
    const value = await askForFile('python');
    if (value !== null) {
        entryScriptNode.value = value;
        await scriptLocationChange({ target: entryScriptNode });
    }
};

const targetLocationSearch = async (event) => {
    const entryTargetNode = document.getElementById('entry-target');
    const value = await askForFolder();
    if (value !== '') {
        entryTargetNode.value = value;
        await targetLocationChange({ target: entryTargetNode });
    }
};

const iconLocationChange = async (event) => {
    colourInput(event.target, true, true, false);
    updateCurrentCommandDisplay();
};

const iconLocationSearch = async (event) => {
    const iconPathNode = document.getElementById('icon-path');
    const value = await askForFile('icon');
    if (value !== null) {
        iconPathNode.value = value;
        await iconLocationChange({ target: iconPathNode });
    }
};

const additionalFilesAddFiles = async (event) => {
    const files = await askForFiles();
    if (files !== null) {
        const datasListNode = document.getElementById('datas-list');
        files.forEach(file => {
            addInputForSrcDst(datasListNode, 'include_files', file, '.', true, true);
        });
    }
};

const additionalFilesAddFolder = async (event) => {
    const folder = await askForFolder();
    if (folder !== '') {
        const datasListNode = document.getElementById('datas-list');
        const destinationFolder = folder.split(/[/\\]/);
        addInputForSrcDst(datasListNode, 'include_files', folder, `${destinationFolder[destinationFolder.length - 1]}/`, true, true);
    }
};

const additionalFilesAddBlank = (event) => {
    const datasListNode = document.getElementById('datas-list');
    addInputForSrcDst(datasListNode, 'include_files', '', '.', true, true);
};

// Settings section events

const recursionLimitToggle = (enabled) => {
    const button = document.getElementById('recursion-limit-switch');
    if (enabled) {
        button.classList.add('selected');
        button.classList.remove('unselected');
    } else {
        button.classList.remove('selected');
        button.classList.add('unselected');
    }
};

const rawArgumentsChange = (event) => {
    updateCurrentCommandDisplay();
};

const packageScript = async (event) => {
    if (packagingState === PACKAGING_STATE_PACKAGING) {  // Do not do anything while packaging
        return;
    }
    if (packagingState === PACKAGING_STATE_COMPLETE) { // This is now the clear output button
        setPackagingState(PACKAGING_STATE_READY);
        return;
    }

    // Pre-checks
    const currentConfiguration = getCurrentConfiguration();
    const entryScript = currentConfiguration.find(c => c.optionDest === 'filenames').value;
    const targetName = currentConfiguration.map(c=>c.optionDest).indexOf('target_name')===-1 ? '' :currentConfiguration.find(c => c.optionDest === 'target_name').value;

    if (entryScript === '') {
        alert(getTranslation('nonDom.alert.noScriptsLocationProvided'));
        return;
    }

    const willOverwrite = await eel.will_packaging_overwrite_existing(
        entryScript,
        getNonCxFreezeConfiguration().outputDirectory,
        targetName
    )();
    if (willOverwrite && !confirm(getTranslation('nonDom.alert.overwritePreviousOutput'))) {
        return
    }

    // If checks have passed, package the script
    startPackaging();
};

const openOutputFolder = (event) => {
    eel.open_folder_in_explorer(getNonCxFreezeConfiguration().outputDirectory)();
};

const setupEvents = () => {
    // Script location
    document.getElementById('entry-script').addEventListener('input', scriptLocationChange);
    document.getElementById('entry-script-search').addEventListener('click', scriptLocationSearch);

    // App location
    document.getElementById('entry-target').addEventListener('input', targetLocationChange);
    document.getElementById('entry-target-search').addEventListener('click', targetLocationSearch);

    // Icon
    document.getElementById('icon-path').addEventListener('input', iconLocationChange);
    document.getElementById('icon-path-search').addEventListener('click', iconLocationSearch);

    // // Additional files
    // document.getElementById('additional-files-add-files-button').addEventListener('click', additionalFilesAddFiles);
    // document.getElementById('additional-files-add-folder').addEventListener('click', additionalFilesAddFolder);
    // document.getElementById('additional-files-add-blank').addEventListener('click', additionalFilesAddBlank);

    // Settings
    document.getElementById('recursion-limit-switch').addEventListener('click', e => recursionLimitToggle(e.target.classList.contains('unselected')));
    document.getElementById('raw-arguments').addEventListener('input', rawArgumentsChange);
    document.getElementById('configuration-import').addEventListener('click', () => onConfigurationImport());
    document.getElementById('configuration-export').addEventListener('click', () => onConfigurationExport());

    // Build buttons
    document.getElementById('package-button').addEventListener('click', packageScript);
    document.getElementById('open-output-folder-button').addEventListener('click', openOutputFolder);

    // Add configurationGetters
    const getEntryScript = () => (['filenames', document.getElementById('entry-script').value]);
    const getEntryTarget = () => (['target_dir', document.getElementById('entry-target').value]);
    const getIcon = () => {
        const path = document.getElementById('icon-path').value;
        return path === '' ? null : ['icon', path];
    };
    configurationGetters.push(getEntryScript);
    configurationGetters.push(getEntryTarget);
    configurationGetters.push(getIcon);

    // Add configurationSetters
    const setEntryScript = (value) => {
        document.getElementById('entry-script').value = value;
        scriptLocationChange({ target: document.getElementById('entry-script') });
    };
    const setEntryTarget = (value) => {
        document.getElementById('entry-target').value = value;
        targetLocationChange({ target: document.getElementById('entry-target') });
    };
    const setAdditionalFileOfDoubleInput = (value) => {
        const datasListNode = document.getElementById('datas-list');
        const [val1, val2] = value.split(pathSeparator);
        addDoubleInputForSrcDst(datasListNode, 'datas', val1, val2, true, true);
    };
    const setAdditionalFileOfInput = (value) => {
        const datasListNode = document.getElementById('datas-list');
        addInputForSrcDst(datasListNode, 'include_files', value, '.', true, true);
    };
    const setIcon = (value) => {
        document.getElementById('icon-path').value = value;
        document.getElementById('icon-path').dispatchEvent(new Event('input'));
    };
    configurationSetters['filenames'] = setEntryScript;
    configurationSetters['target_dir'] = setEntryTarget;
    configurationSetters['include_files'] = setAdditionalFileOfInput;
    configurationSetters['icon'] = setIcon;

    configurationCleaners.push(() => setEntryScript('')); // filenames
    configurationCleaners.push(() => setEntryTarget('')); // target path
    configurationCleaners.push(() => setIcon('')); // icon

    // Soft initialise (to trigger any required initial events)
    setEntryScript('');
    setEntryTarget('');
};
