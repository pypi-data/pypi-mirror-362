/**
 * PyAMS custom headers handler
 */
(function() {
    'use strict';

    const global = tinymce.util.Tools.resolve('tinymce.PluginManager');

    /** Check for nullable value */
    const isNullable = (a) => {
        return a === null || a === undefined;
    };

    /** Check for non-nullable value */
    const isNonNullable = (a) => {
        return !isNullable(a);
    };

    /** Get selection if it is an H3 or H4 header */
    const getSelectedHeader = (editor, name) => {
        const
            elm = editor.selection.getNode(),
            header = editor.dom.getParent(elm, name);
        if (header) {
            return editor.dom.select(name, header)[0];
        }
        if (elm && (elm.nodeName !== name)) {
            return null;
        }
        return elm;
    };

    /** Button setup for given header level */
    const setupButton = (editor, name) => {
        return function (api) {
            api.setActive(isNonNullable(getSelectedHeader(editor, name)));
            return editor.selection.selectorChangedWithUnbind(name, api.setActive);
        }
    };

    /** Toggle header on given level */
    const toggleHeader = (editor, name) => {
        return function () {
            editor.execCommand('mceToggleFormat', false, name);
        };
    };

    /** Buttons initialization */
    const initButtons = (editor) => {
        ['h3', 'h4'].forEach((name) => {
            editor.ui.registry.addToggleButton(`header-${name}`, {
                text: name.toUpperCase(),
                tooltip: `Toggle ${name.toUpperCase()} header`,
                onSetup: setupButton(editor, name),
                onAction: toggleHeader(editor, name)
            });
        });
    };

    /**
     * Main plugin registration
     */
    function Plugin() {
        global.add('pyams_headers', function (editor) {
            initButtons(editor);
            return {
                'name': "PyAMS headers toolbar buttons",
                'url': "https://pyams.ztfy.org"
            }
        });
        global.requireLangPack('pyams_headers', 'fr');
    }

    Plugin();

})();
