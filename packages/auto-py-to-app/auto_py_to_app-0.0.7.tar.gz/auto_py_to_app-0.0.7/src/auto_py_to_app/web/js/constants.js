const options_ignored = ['help','version','replace_paths','optimize'];
const options_static = ['command','script','icon', 'target_dir', 'filenames','include_files'];
const options_overridden = [];

const options_inputTypeFile = ['command','script','init_script','base_name','icon','manifest','bin_includes','bin_excludes','include_files','zip_includes', 'manifest'];
const options_inputTypeDirectory = ['shortcut_dir','target_dir','default_path','include_path','bin_path_includes','bin_path_excludes','include_files'];
const options_inputTypeDoubleFileDest = ['datas', 'binaries'];
const options_inputTypeDoubleDirectoryDest = ['datas'];
const options_inputTypeMultipleInput = ['excludes','includes','packages','default_path','include_path','bin_includes','bin_excludes','bin_path_includes','bin_path_excludes','include_files','zip_includes','zip_include_packages'];
const options_inputTypeDoubleMultipleInput = ['datas','binaries'];

const advancedSections = [
    {
        titleI18nPath: 'dynamic.title.generalOptions',
        options: ['init_script','base_name','target_name','compress','silent']
    },
    // {
    //     titleI18nPath: 'dynamic.title.whatToBundleWhereToSearch',
    //     options: ['excludes','includes','packages','default_path','include_path','bin_includes','bin_excludes','bin_path_includes','bin_path_excludes','zip_includes','zip_include_packages','zip_exclude_packages']
    // },
    {
        titleI18nPath: 'dynamic.title.windowsSpecificOptions',
        options: ['manifest','copyright','trademarks', 'uac_admin', 'include_msvcr', 'shortcut_name','shortcut_dir']
    },
];


// String constants
OPTION_IGNORED = 'OPTION_IGNORED';
OPTION_STATIC = 'OPTION_STATIC';
OPTION_OVERRIDDEN = 'OPTION_OVERRIDDEN';
OPTION_SHOW = 'OPTION_SHOW';

OPTION_INPUT_TYPE_SWITCH = 'OPTION_INPUT_TYPE_SWITCH';
OPTION_INPUT_TYPE_DROPDOWN = 'OPTION_INPUT_TYPE_DROPDOWN';
OPTION_INPUT_TYPE_INPUT = 'OPTION_INPUT_TYPE_INPUT';
OPTION_INPUT_TYPE_MULTIPLE_INPUT = 'OPTION_INPUT_TYPE_MULTIPLE_INPUT';
OPTION_INPUT_TYPE_DOUBLE_MULTIPLE_INPUT = 'OPTION_INPUT_TYPE_DOUBLE_MULTIPLE_INPUT';

OPTION_INPUT_VALUE_TEXT = 'OPTION_INPUT_VALUE_TEXT';
OPTION_INPUT_VALUE_FILE = 'OPTION_INPUT_VALUE_FILE';
OPTION_INPUT_VALUE_DIRECTORY = 'OPTION_INPUT_VALUE_DIRECTORY';
OPTION_INPUT_VALUE_DOUBLE_FILE_DEST = 'OPTION_INPUT_VALUE_DOUBLE_FILE_DEST';
OPTION_INPUT_VALUE_DOUBLE_DIRECTORY_DEST = 'OPTION_INPUT_VALUE_DOUBLE_DIRECTORY_DEST';

PACKAGING_STATE_READY = 'PACKAGING_STATE_READY';
PACKAGING_STATE_PACKAGING = 'PACKAGING_STATE_PACKAGING';
PACKAGING_STATE_COMPLETE = 'PACKAGING_STATE_COMPLETE';
