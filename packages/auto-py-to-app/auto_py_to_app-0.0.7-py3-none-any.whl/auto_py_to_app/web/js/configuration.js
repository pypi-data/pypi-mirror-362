/*
Handle configuration modifications
*/

const configurationGetters = []; // Each function in this should either return null or [option.dest, value]
const configurationSetters = {}; // dest: fn(value) => void, used to set option values
const configurationCleaners = []; // Each function in this should clear a dest value

// Get option-value pairs [[option, value], ...]
const getCurrentConfiguration = () => {
    const currentConfiguration = [
        // {
        //     optionDest: 'noconfirm',
        //     value: true
        // }
    ];

    // Call all functions to get data
    configurationGetters.forEach(getter => {
        const optionValuePair = getter();
        if (optionValuePair !== null) {
            currentConfiguration.push({
                optionDest: optionValuePair[0],
                value: optionValuePair[1],
            })
        }
    });

    return currentConfiguration;
};

const getNonCxFreezeConfiguration = () => {
    return {
        outputDirectory: document.getElementById('entry-target').value,
        increaseRecursionLimit: !document.getElementById('recursion-limit-switch').classList.contains('unselected'),
        manualArguments: document.getElementById('raw-arguments').value
    };
};

const getCurrentCommand = (withTargetPath = true) => {
    const currentConfiguration = getCurrentConfiguration();

    // Match configuration values with the correct flags
    filterFunc = withTargetPath ? c => c.optionDest !== 'filenames' : c=> (c.optionDest !== 'filenames' && c.optionDest !== 'target_dir');
    const optionsAndValuesAfterFilter = currentConfiguration.filter(filterFunc);
    const optionsAndValuesDest = optionsAndValuesAfterFilter.map(c => c.optionDest);
    const optionsAndValuesDestDuplicates = optionsAndValuesDest.filter((c,i)=>optionsAndValuesDest.indexOf(c)!==optionsAndValuesDest.lastIndexOf(c) && optionsAndValuesDest.indexOf(c)===i);
    const optionsAndValuesUnique = optionsAndValuesAfterFilter.filter(c => optionsAndValuesDestDuplicates.indexOf(c.optionDest)===-1);

    const optionsAndValuesUniqueFormat = optionsAndValuesUnique.map(c => {
        // Identify the options
        const option = options.find(o => o.dest === c.optionDest);

        if (option.nargs === 0) {
            // For switches, there are some switches for false switches that we can use
            const potentialOption = options.find(o => o.dest === c.optionDest && o.const === c.value);
            if (potentialOption !== undefined) {
                return chooseOptionString(potentialOption.option_strings);
            } else {
                return null; // If there is no alternate option, skip it as it won't be required
            }
        } else {
            const optionFlag = chooseOptionString(option.option_strings);
            return `${optionFlag} "${c.value}"`;
        }
    }).filter(x => x !== null);

    const optionsAndValuesDuplicatesFormat = optionsAndValuesDestDuplicates.map(d => {
        // Identify the options
        const optionsDuplicate = optionsAndValuesAfterFilter.filter(o=>o.optionDest===d);
        const option = options.find(o => o.dest === d);
        const optionFlag = chooseOptionString(option.option_strings);
        const seperatedOptionCommand = optionsDuplicate.map(c => {
            if (option.nargs === 0) {
                // For switches, there are some switches for false switches that we can use
                const potentialOption = options.find(o => o.dest === c.optionDest && o.const === c.value);
                if (potentialOption !== undefined) {
                    return chooseOptionString(potentialOption.option_strings);
                } else {
                    return null; // If there is no alternate option, skip it as it won't be required
                }
            } else {
                return `"${c.value}"`;
            }
        });
        return `${optionFlag} ${seperatedOptionCommand.join(',')}`;
    }).filter(x => x !== null);

    // Identify the entry script provided
    const entryScriptConfig = currentConfiguration.find(c => c.optionDest === 'filenames');
    const entryScript = entryScriptConfig === undefined ? "" : entryScriptConfig.value;

    return `cxfreeze --script "${entryScript}" ${optionsAndValuesUniqueFormat.join(' ')} ${optionsAndValuesDuplicatesFormat.join(' ')} ${getNonCxFreezeConfiguration().manualArguments}`;
};

const updateCurrentCommandDisplay = () => {
    document.querySelector('#current-command textarea').value = getCurrentCommand();
};

const isCommandDefault = () => {
    return getCurrentCommand() === 'cxfreeze --script ""  ';
}
