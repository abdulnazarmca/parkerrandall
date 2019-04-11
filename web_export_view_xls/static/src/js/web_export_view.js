
odoo.define('web_export_view', function (require) {
"use strict";


var session = require('web.session');
    var core = require('web.core');
var Widget = require('web.Widget');
var BasicRenderer = require('web.BasicRenderer');
var ActionManager = require('web.ActionManager');
var ListRenderer = require('web.ListRenderer');
var ActionManager = require('web.ActionManager');
var ListController = require('web.ListController');
var AbstractController = require('web.AbstractController');
var core = require('web.core');
var pyeval = require('web.pyeval');
var Sidebar = require('web.Sidebar');
var _t = core._t;
var qweb = core.qweb;



ListController.include({                // Add the menu in side bar in icon

    init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
    },

    on_sidebar_export_treeview_xls: function () {
            var self = this;

              var row = []
              var export_rows = []
                var children;
                var self = this,
                view = this.getParent();
                // Anand
                var cache = [];

                 var fields = view.view_stack[0].fields_view.arch.children;

                children = view.getChildren();
            if (children) {
                children.every(function (child) {
                    if (child.field && child.field.type == 'one2many') {
                        view = child.viewmanager.views.list.controller;
                        return false; // break out of the loop
                    }
                    if (child.field && child.field.type == 'many2many') {
                        view = child.list_view;
                        return false; // break out of the loop
                    }
                    return true;
                });
            }
            var export_columns_keys = [];
            var export_columns_names = [];
            $.each(fields, function () {
                if (this.tag == 'field' && this.attrs.invisible != 1) {
                    // non-fields like `_group` or buttons
                    export_columns_keys.push(1);
                   // export_columns_names.push(this.string);
                }
            });
            var heads = $("thead")
           /* $.each(heads, function (idx, ele) {
            console.log("heads",ele)
            $.each(ele.childNodes,function (ind,head){

            console.log("headfdf",head.childNodes)
            $.each(head.childNodes, function(id,th){
            console.log("thhhh",th)
                if(th.attributes.class){
                if(th.attributes.class.nodeValue != 'o_list_record_selector'){
                    export_columns_names.push(th.innerText);
                console.log("tthhh",th.innerText)
                }
                }
            })

            });
           // if(){


             //       }
            });*/

            $("table > thead > tr > th").each(function (ind,th) {
                    if($(this).hasClass('o_list_record_selector')){
                            return true
                    }
                    else{
                    export_columns_names.push($(this).text());
                    }
            })
            export_columns_keys =  this.getSelectedIds(),
            $.blockUI();

            if (children) {

            $( '.o_list_view' ).find( 'tbody' ).find( 'tr' ).has( 'input[type=checkbox]:checked' ).each(function(id,selectedRows){
              row = []

            $(selectedRows.children).each(function(ind,val){
            if(val.attributes.class.nodeValue != 'o_list_record_selector'){
            if(val.attributes.class.nodeValue.indexOf('o_list_number') != -1){
                    
                   var amt = val.textContent.split(/\s{1}/)
                   if (!isNaN(parseFloat(amt[0])))
                    {var num = amt[0]}
                   else
                    {var num = amt[1]}
                   var myStr = num.replace(/,/g, "");
                   var res = parseFloat(myStr)
                     row.push(res)
            }
               /* if(val.attributes.class.nodeValue == 'o_data_cell o_list_number o_monetary_cell o_readonly_modifier' || val.attributes.class.nodeValue == 'o_data_cell o_list_number o_readonly_modifier'){

                }*/
                else{
                     row.push(val.textContent)

                }

                    }

            });
            export_rows.push(row)
            });

            }
            session.get_file({
                url: '/web/export/xls_view',
                data: {data: JSON.stringify({
                    model: view.env.modelName,
                    headers: export_columns_names,
                    rows: export_rows
                })},
                complete: $.unblockUI
            });
        },

 // Todo : include the side bar instead of overriding function


     renderSidebar: function ($node) {
        if (this.hasSidebar && !this.sidebar) {
            var other = [{
                label: _t("Export"),
                callback: this._onExportData.bind(this)
            }];
             other.push({
                    label: _t("Export As Excel"),
                    callback: this.on_sidebar_export_treeview_xls.bind(this)
                });
            if (this.archiveEnabled) {
                other.push({
                    label: _t("Archive"),
                    callback: this._onToggleArchiveState.bind(this, true)
                });
                other.push({
                    label: _t("Unarchive"),
                    callback: this._onToggleArchiveState.bind(this, false)
                });
            }
            if (this.is_action_enabled('delete')) {
                other.push({
                    label: _t('Delete'),
                    callback: this._onDeleteSelectedRecords.bind(this)
                });
            }
            this.sidebar = new Sidebar(this, {
                editable: this.is_action_enabled('edit'),
                env: {
                    context: this.model.get(this.handle, {raw: true}).getContext(),
                    activeIds: this.getSelectedIds(),
                    model: this.modelName,
                },
                actions: _.extend(this.toolbarActions, {other: other}),
            });
            this.sidebar.appendTo($node);

            this._toggleSidebar();
        }
    },




});

});
