/**
 * PyAMS internal link plug-in handler
 */
(function() {
    'use strict';

    const global = tinymce.util.Tools.resolve('tinymce.PluginManager');
    const rangeUtils = tinymce.util.Tools.resolve('tinymce.dom.RangeUtils');
    const tools = tinymce.util.Tools.resolve('tinymce.util.Tools');

    const LINK_SELECTOR = 'a[href]';

    const isLink = (elm) => {
        return elm && elm.nodeName.toLowerCase() === 'a';
    };

    const getHrefFromLink = (elm) => {
        return elm.getAttribute('href');
    };

    const getLink = (editor) => {
        return editor.dom.getParent(editor.selection.getStart(), LINK_SELECTOR);
    };

    const removeLinksInSelection = (editor) => {
        const dom = editor.dom;
        rangeUtils(dom).walk(editor.selection.getRng(), (nodes) => {
            tools.each(nodes, (node) => {
                if (isLink(node)) {
                    dom.remove(node, false);
                }
            });
        });
    };

    const insertLink = (editor, data) => {
        editor.undoManager.transact(() => {
            const link = editor.dom.createHTML('a', {
                href: `oid://${data.oid}`,
                title: data.title || data.text
            }, data.text);
            if (editor.selection.isCollapsed()) {
                editor.insertContent(link);
            } else {
                removeLinksInSelection(editor);
                editor.selection.setContent(link);
                editor.addVisual();
            }
        });
    };

    const updateLink = (editor, link, data) => {
        editor.undoManager.transact(() => {
            editor.dom.setAttribs(link, {
                href: `oid://${data.oid}`,
                title: data.title || data.text
            });
            editor.dom.setHTML(link, data.text);
        });
    };

    const submitLink = (editor, data) => {
        if (!(data.oid && data.text)) {
            editor.windowManager.alert("Internal number and link text are required!");
            return false;
        } else {
            const link = getLink(editor);
            if (link) {
                updateLink(editor, link, data);
            } else {
                insertLink(editor, data);
            }
            return true;
        }
    };

    const openLinkDialog = (editor) => {
        const currentData = {};
        const link = getLink(editor);
        if (link) {
            if (link.href.startsWith('oid://')) {
                currentData.oid = link.href.substring(6);
            } else {
                currentData.oid = link.href;
            }
            currentData.text = link.innerText;
            currentData.title = link.title;
        } else {
            currentData.text = editor.selection.getContent();
        }
        editor.windowManager.open({
            title: "Insert internal link",
            size: 'normal',
            body: {
                type: 'panel',
                items: [{
                    type: 'input',
                    name: 'oid',
                    inputMode: 'text',
                    label: "Internal number",
                    placeholder: "Link target unique reference"
                }, {
                    type: 'input',
                    name: 'text',
                    inputMode: 'text',
                    label: "Link text",
                    placeholder: "Displayed link text content"
                }, {
                    type: 'input',
                    name: 'title',
                    inputMode: 'text',
                    label: "Title",
                    placeholder: ""
                }]
            },
            buttons: [{
                type: 'cancel',
                name: 'cancel',
                text: "Cancel"
            }, {
                type: 'submit',
                name: 'save',
                text: "Save",
                primary: true
            }],
            initialData: currentData,
            onSubmit: (api) => {
                if (submitLink(editor, api.getData())) {
                    api.close();
                }
            }
        });
    };

    const openDialog = (editor) => {
        return function() {
            openLinkDialog(editor);
        }
    };

    const toggleState = (editor, toggler) => {
        editor.on('NodeChange', toggler);
        return function() {
            return editor.off('NodeChange', toggler);
        }
    };

    const checkActiveState = (editor) => {
        return function(api) {
            const updateState = () => {
                let activeMode = !editor.mode.isReadOnly();
                if (activeMode) {
                    const link = getLink(editor);
                    activeMode = (link !== null) && link.getAttribute('href').startsWith('oid://');
                }
                return api.setActive(activeMode);
            }
            updateState();
            return toggleState(editor, updateState);
        }
    }

    const initMenuItem = (editor) => {
        editor.ui.registry.addMenuItem('pyams_link', {
            text: "Internal link...",
            icon: 'browse',
            shortcut: 'Meta+Shift+K',
            onAction: openDialog(editor)
        });
    };

    const initButton = (editor) => {
        editor.ui.registry.addToggleButton('pyams_link', {
            icon: 'browse',
            tooltip: "Insert internal link",
            onAction: openDialog(editor),
            onSetup: checkActiveState(editor)
        });
    };

    /**
     * Main plugin registration
     */
    function Plugin() {
        global.add('pyams_link', function (editor) {
            initMenuItem(editor);
            initButton(editor);
            return {
                'name': "PyAMS internal links",
                'url': "https://pyams.ztfy.org"
            }
        });
        global.requireLangPack('pyams_link', 'fr');
    }

    Plugin();

}());
