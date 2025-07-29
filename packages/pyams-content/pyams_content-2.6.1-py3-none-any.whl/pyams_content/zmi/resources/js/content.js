/* global MyAMS */

'use strict';


if (window.$ === undefined) {
    window.$ = MyAMS.$;
}


const content = {

    /**
     * TinyMCE editor extensions
     */
    TinyMCE: {

        initEditor: (input, settings) => {
            const mce = window.tinyMCE;
            if (mce !== undefined) {

                settings.external_plugins = $.extend({}, settings.external_plugins, {
                    'pyams_link': '/--static--/pyams_content/js/tinymce/internal-link/plugin.js',
                    'pyams_headers': '/--static--/pyams_content/js/tinymce/headers/plugin.js'
                });
                settings.style_formats = [{
                    title: 'Headers',
                    items: [
                        { title: 'H3 header', format: 'h3' },
                        { title: 'H4 header', format: 'h4' }
                    ]
                }, {
                    title: 'Blocs',
                    items: [
                        { title: 'Paragraph', format: 'p' },
                        { title: 'Blockquote', format: 'blockquote' },
                        { title: 'Div', format: 'div' },
                        { title: 'Pre', format: 'pre' }
                    ]
                }, {
                    title: 'Inline',
                    items: [
                        { title: 'Bold', icon: 'bold', format: 'bold' },
                        { title: 'Italic', icon: 'italic', format: 'italic' },
                        { title: 'Underline', icon: 'underline', format: 'underline' },
                        { title: 'Strikethrough', icon: 'strike-through', format: 'strikethrough' },
                        { title: 'Superscript', icon: 'superscript', format: 'superscript' },
                        { title: 'Subscript', icon: 'subscript', format: 'subscript' },
                        { title: 'Code', icon: 'sourcecode', format: 'code' }
                    ]
                }, {
                    title: 'Align',
                    items: [
                        { title: 'Left', icon: 'align-left', format: 'alignleft' },
                        { title: 'Center', icon: 'align-center', format: 'aligncenter' },
                        { title: 'Right', icon: 'align-right', format: 'alignright' }
                    ]
                }];
                if (settings.menubar) {
                    settings.menu = $.extend({}, settings.menu, {
                        insert: {
                            title: "Insert",
                            items: 'link pyams_link inserttable | charmap emoticons hr | ' +
                                'pagebreak nonbreaking anchor | insertdatetime'
                        }
                    });
                }
                if (settings.toolbar1) {
                    settings.toolbar1 = 'undo redo | pastetext | header-h3 header-h4 styleselect ' +
                        '| bold italic | alignleft aligncenter alignright ' +
                        '| bullist numlist outdent indent';
                }
                if (settings.toolbar2) {
                    settings.toolbar2 = 'forecolor backcolor | charmap pyams_link link ' +
                        '| fullscreen preview print | code';
                }
            }
        }
    },

    /**
     * Tree management
     */
    tree: {

        /**
         * Visibility switch callback handler
         *
         * @param form: original form (may be empty)
         * @param options: callback options
         */
        switchVisibleElement: (form, options) => {
            const
                node_id = options.node_id,
                tr = $(`tr[data-ams-tree-node-id="${node_id}"]`),
                table = $(tr.parents('table')),
                head = $('thead', table),
                col = $(`th[data-ams-column-name="visible"]`, head),
                colPos = col.index(),
                icon = $('i', $(`td:nth-child(${colPos+1})`, tr)),
                parent = $(`[data-ams-tree-node-id="${tr.data('ams-tree-node-parent-id')}"]`);
            let klass;
            if (parent.get(0).tagName === 'TR') {
                const parentIcon = $('i', $(`td:nth-child(${colPos+1})`, parent));
                klass = parentIcon.attr('class');
            } else {
                klass = table.data('ams-visible') ? '' : 'text-danger';
            }
            if (options.state === true) {
                icon.replaceWith(`<i class="${col.data('ams-icon-on')} ${klass}"></i>`);
            } else {
                icon.replaceWith(`<i class="${col.data('ams-icon-off')} ${klass}"></i>`);
            }
        }
    },


    /**
     * Widgets management
     */
    widget: {

        /**
         * Treeview widget
         */
        treeview: {

            selectFolder: (event, node) => {
                const target = $(event.target);
                target.siblings('input[type="hidden"]').val(node.id);
            },

            unselectFolder: (event, node) => {
                const target = $(event.target);
                target.siblings('input[type="hidden"]').val(null);
            }
        }
    },


    /**
     * Pictograms management
     */
    pictograms: {

        initManagerSelection: function () {
            const
                form = $(this),
                selected = $('input[type="hidden"]', $('.selected-pictograms', form)).listattr('value');
            return {
                selected: JSON.stringify(selected)
            };
        },

        switchPictogram: (event) => {
            $('i', event.currentTarget).tooltip('hide');
            let pictogram = $(event.currentTarget);
            if (!pictogram.hasClass('pictogram')) {
                pictogram = pictogram.parents('.pictogram');
            }
            const
                input = $('input', pictogram),
                parent = pictogram.parents('.pictograms'),
                manager = parent.parents('.pictograms-manager');
            if (parent.hasClass('available-pictograms')) {
                const name = input.attr('data-ams-pictogram-name');
                input.removeAttr('data-ams-pictogram-name')
                    .attr('name', name);
                $('a.action i', pictogram).replaceWith($('<i></i>')
                    .addClass('fa fa-fw fa-arrow-left hint opaque baseline')
                    .attr('data-ams-hint-gravity', 'se')
                    .attr('data-ams-hint-offset', '3'));
                $('.selected-pictograms', manager).append(pictogram);
            } else {
                const name = input.attr('name');
                input.removeAttr('name')
                    .attr('data-ams-pictogram-name', name);
                $('a.action i', pictogram).replaceWith($('<i></i>')
                    .addClass('fa fa-fw fa-arrow-right hint opaque baseline')
                    .attr('data-ams-hint-gravity', 'se')
                    .attr('data-ams-hint-offset', '3'));
                $('.available-pictograms', manager).append(pictogram);
            }
        },

        endDrag: (event, ui) => {
            $(ui.source).remove();
        }
    },


    /**
     * Paragraphs management
     */
    paragraphs: {

        switchEditor: (event, options) => {
            const
                object_id = options && options.object_id ? options.object_id : null,
                target = object_id ? $('.switcher-parent', $(`tr[id="${object_id}"]`)) : $(event.currentTarget),
                switcher = $('.switcher', target),
                editor = target.siblings('.editor');
            if (switcher.hasClass('expanded')) {
                MyAMS.core.clearContent(editor).then(() => {
                    editor.empty();
                    switcher.html('<i class="far fa-plus-square"></i>')
                        .removeClass('expanded');
                });
            } else {
                switcher.html('<i class="fas fa-spinner fa-spin"></i>');
                MyAMS.require('ajax', 'helpers').then(() => {
                    const
                        tr = target.parents('tr'),
                        objectName = tr.data('ams-element-name'),
                        table = tr.parents('table'),
                        location = table.data('ams-location');
                    MyAMS.ajax.post(`${location}/get-paragraph-editor.json`, {
                        object_name: objectName
                    }).then((result) => {
                        const content = result[objectName];
                        if (content) {
                            editor.html(content);
                            MyAMS.core.initContent(editor).then(() => {
                                MyAMS.helpers.scrollTo('#content', editor, {
                                    offset: -15
                                });
                            });
                        }
                    }).finally(() => {
                        switcher.html('<i class="far fa-minus-square"></i>')
                            .addClass('expanded');
                    });
                });
            }
        },

        switchAllEditors: (event) => {
            const
                target = $(event.currentTarget),
                switcher = $('.switcher', target),
                table = target.parents('table'),
                tbody = $('tbody', table);
            if (switcher.hasClass('expanded')) {
                $('tr', tbody).each((idx, elt) => {
                    const editor = $('.editor', elt);
                    MyAMS.core.clearContent(editor).then(() => {
                        editor.empty();
                        $('.switcher', elt).html('<i class="far fa-plus-square"></i>')
                            .removeClass('expanded');
                    });
                });
                switcher.html('<i class="far fa-plus-square"></i>')
                    .removeClass('expanded');
            } else {
                switcher.html('<i class="fas fa-spinner fa-spin"></i>');
                MyAMS.require('ajax', 'helpers').then(() => {
                    const location = table.data('ams-location');
                    MyAMS.ajax.post(`${location}/get-paragraphs-editors.json`).then((result) => {
                        for (const [name, form] of Object.entries(result)) {
                            const
                                row = $(`tr[data-ams-element-name="${name}"]`, tbody),
                                rowSwitcher = $('.switcher', row);
                            if (!rowSwitcher.hasClass('expanded')) {
                                const editor = $('.editor', row);
                                editor.html(form);
                                MyAMS.core.initContent(editor).then(() => {
                                    rowSwitcher.html('<i class="far fa-minus-square"></i>')
                                        .addClass('expanded');
                                });
                            }
                        }
                    }).finally(() => {
                        switcher.html('<i class="far fa-minus-square"></i>')
                            .addClass('expanded');
                    });
                });
            }
        },

        refreshTitle: (form, params) => {
            const
                row = $(`tr[data-ams-element-name="${params.element_name}"]`);
            if (row.attr('data-ams-url')) {
                $('td.title', row).text(params.title);
            } else {
                $('span.title', row).text(params.title);
            }
        }
    },


    /**
     * Medias galleries management
     */
    galleries: {

        /**
         * Sort medias into gallery
         */
        sortMedias: (event, ui) => {
            const
                gallery = $(event.target),
                location = gallery.data('ams-location'),
                elements = $('.media-thumbnail', gallery).listattr('data-ams-element-name');
            MyAMS.require('ajax', 'alert', 'i18n').then(() => {
                MyAMS.ajax.post(`${location}/set-medias-order.json`, {
                    order: elements.join(';')
                }).then((result) => {
                    MyAMS.alert.smallBox({
                        status: 'success',
                        message: MyAMS.i18n.DATA_UPDATED,
                        icon: 'fa-info-circle'
                    });
                });
            });
        },

        switchVisibleMedia: (event, options) => {
            const
                switcher = $(event.currentTarget),
                switcherHtml = switcher.html(),
                media = switcher.parents('.media-thumbnail'),
                gallery = switcher.parents('.gallery'),
                location = gallery.data('ams-location');
            switcher.html('<i class="fas fa-fw fa-spinner fa-spin"></i>');
            MyAMS.require('ajax').then(() => {
                MyAMS.ajax.post(`${location}/switch-media-visibility.json`, {
                    object_name: media.data('ams-element-name'),
                    attribute_name: 'visible'
                }).then((result) => {
                    if (result.status === 'success') {
                        if (result.state) {
                            switcher.html('<i class="far fa-fw fa-eye"></i>');
                        } else {
                            switcher.html('<i class="far fa-fw fa-eye-slash text-danger"></i>');
                        }
                    }
                }).catch(() => {
                    switcher.html(switcherHtml);
                });
            });
        },

        /**
         * Remove media from gallery
         */
        removeMedia: (event, options) => {
            const
                media = $(event.currentTarget).parents('.media-thumbnail'),
                gallery = media.parents('.gallery'),
                location = gallery.data('ams-location');
            MyAMS.require('ajax', 'alert', 'i18n', 'helpers').then(() => {
                MyAMS.alert.bigBox({
                    status: 'danger',
                    icon: 'fas fa-bell',
                    title: MyAMS.i18n.WARNING,
                    message: MyAMS.i18n.CONFIRM_REMOVE,
                    successLabel: MyAMS.i18n.CONFIRM,
                    cancelLabel: MyAMS.i18n.BTN_CANCEL
                }).then((status) => {
                    if (status !== 'success') {
                        return;
                    }
                    MyAMS.ajax.post(`${location}/remove-media.json`, {
                        object_name: media.data('ams-element-name')
                    }).then((result) => {
                        if (result.status === 'success') {
                            media.remove();
                            if (result.handle_json) {
                                MyAMS.ajax.handleJSON(result);
                            }
                        } else {
                            MyAMS.ajax.handleJSON(result);
                        }
                    });
                });
            });
        }
    },


    /**
     * Reviews management
     */
    review: {

        // Review comments timer
        timer: null,
        interval: 30000,

        // Scroll messages list to last message
        init: () => {
            $(document).off('update-comments.ams.content')
                .on('update-comments.ams.content', (evt, {count}) => {
                    const menu = $('a[href="#review-comments.html"]', $('nav'));
                    if (menu.exists()) {
                        $('.badge', menu).text(count);
                    }
                });
            const review = MyAMS.content.review;
            review.timer = setTimeout(review.getComments, review.interval);
        },

        initPage: () => {
            MyAMS.require('helpers').then(() => {
                const
                    messages = $('#review-messages-view'),
                    lastMessage = $('li', messages).last();
                if (messages.exists()) {
                    MyAMS.helpers.scrollTo(messages, lastMessage);
                }
            });
        },

        getComments: () => {
            MyAMS.require('ajax', 'helpers').then(() => {
                const
                    review = MyAMS.content.review,
                    menu = $('a[href="#review-comments.html"]', $('nav')),
                    badge = $('.badge', menu);
                MyAMS.ajax.get('get-comments.json', {
                    count: badge.text() || '0'
                }).then(({status, comments, count}, xhrStatus, xhr) => {
                    if (count !== parseInt(badge.text())) {
                        badge.removeClass('bg-info')
                            .addClass('bg-danger scaled');
                        badge.text(count);
                        setTimeout(() => {
                            badge.removeClass('bg-danger scaled')
                                .addClass('bg-info');
                        }, 10000);
                    }
                    if (comments) {
                        const
                            messagesView = $('#review-messages-view'),
                            messagesList = $('#review-messages');
                        for (const comment of comments) {
                            messagesList.append($(comment));
                        }
                        MyAMS.helpers.scrollTo(messagesView, $('li', messagesList).last());
                    }
                    review.timer = setTimeout(review.getComments, review.interval);
                });
            })
        }
    },


    /**
     * Thesaurus management
     */
    thesaurus: {

        /**
         * Update extracts list on selected thesaurus change
         *
         * @param evt: source change event
         */
        changeThesaurus: (evt) => {
            const
                form = $(evt.currentTarget).parents('form'),
                thesaurus = $('select[name$=".widgets.thesaurus_name"]', form),
                thesaurus_name = thesaurus.val(),
                extract = $('select[name$=".widgets.extract_name"]', form),
                plugin = extract.data('select2');
            extract.empty();
            extract.select2('data', null);
            plugin.results.clear();
            if (thesaurus_name) {
                MyAMS.require('ajax').then(() => {
                    MyAMS.ajax.get(`${window.location.origin}/api/thesaurus/extracts`, {
                        'thesaurus_name': thesaurus_name
                    }).then((result) => {
                        $('<option />')
                            .attr('id', 'form-widgets-extract_name-novalue')
                            .attr('value', '--NOVALUE--')
                            .text(MyAMS.i18n.NO_SELECTED_VALUE)
                            .appendTo(extract);
                        $(result.results).each((idx, elt) => {
                            $('<option />')
                                .attr('id', `form-widgets-extract_name-${idx}`)
                                .attr('value', elt.id)
                                .text(elt.text)
                                .appendTo(extract);
                        });
                        extract.val('--NOVALUE--').trigger('change');
                    });
                })
            }
        }
    }
};


if (window.MyAMS) {
    MyAMS.config.modules.push('content');
    MyAMS.content = content;
    console.debug("MyAMS: content module loaded...");
}
