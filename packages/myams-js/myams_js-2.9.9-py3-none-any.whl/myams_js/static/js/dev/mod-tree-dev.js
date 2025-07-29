(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define(["exports"], factory);
  } else if (typeof exports !== "undefined") {
    factory(exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod.exports);
    global.modTree = mod.exports;
  }
})(typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : this, function (_exports) {
  "use strict";

  Object.defineProperty(_exports, "__esModule", {
    value: true
  });
  _exports.tree = void 0;
  /* global MyAMS */
  /**
   * MyAMS tree management
   */

  const $ = MyAMS.$;
  const tree = _exports.tree = {
    /**
     * Open/close tree node inside a table
     */
    switchTreeNode: evt => {
      const removeChildNodes = nodeId => {
        $(`tr[data-ams-tree-node-parent-id="${nodeId}"]`).each((idx, elt) => {
          const row = $(elt);
          removeChildNodes(row.data('ams-tree-node-id'));
          dtTable.row(row).remove().draw();
        });
      };
      const node = $(evt.currentTarget),
        switcher = $('.switcher', node),
        tr = node.parents('tr').first(),
        table = tr.parents('table').first(),
        dtTable = table.DataTable();
      node.tooltip('hide');
      if (switcher.hasClass('expanded')) {
        removeChildNodes(tr.data('ams-tree-node-id'));
        switcher.html('<i class="far fa-plus-square"></i>').removeClass('expanded');
      } else {
        const location = tr.data('ams-location') || table.data('ams-location') || '',
          treeNodesTarget = tr.data('ams-tree-nodes-target') || table.data('ams-tree-nodes-target') || 'get-tree-nodes.json',
          sourceName = tr.data('ams-element-name');
        switcher.html('<i class="fas fa-spinner fa-spin"></i>');
        MyAMS.require('ajax').then(() => {
          MyAMS.ajax.post(`${location}/${sourceName}/${treeNodesTarget}`, {
            can_sort: !$('td.sorter', tr).is(':empty')
          }).then(result => {
            if (result.length > 0) {
              let newRow;
              for (const row of result) {
                newRow = $(row);
                dtTable.row.add(newRow).draw();
                MyAMS.core.initContent(newRow).then();
              }
            }
            switcher.html('<i class="far fa-minus-square"></i>').addClass('expanded');
          });
        });
      }
    },
    /**
     * Open close all tree nodes
     */
    switchTree: evt => {
      const node = $(evt.currentTarget),
        switcher = $('.switcher', node),
        th = node.parents('th'),
        table = th.parents('table').first(),
        tableID = table.data('ams-tree-node-id'),
        dtTable = table.DataTable();
      node.tooltip('hide');
      if (switcher.hasClass('expanded')) {
        $('tr[data-ams-tree-node-parent-id]').filter(`tr[data-ams-tree-node-parent-id!="${tableID}"]`).each((idx, elt) => {
          dtTable.row(elt).remove().draw();
        });
        $('.switcher', table).each((idx, elt) => {
          $(elt).html('<i class="far fa-plus-square"></i>').removeClass('expanded');
        });
      } else {
        const location = table.data('ams-location') || '',
          target = table.data('ams-tree-nodes-target') || 'get-tree.json',
          tr = $('tbody tr', table.first());
        switcher.html('<i class="fas fa-spinner fa-spin"></i>');
        MyAMS.require('ajax').then(() => {
          MyAMS.ajax.post(`${location}/${target}`, {
            can_sort: !$('td.sorter', tr).is(':empty')
          }).then(result => {
            $(`tr[data-ams-tree-node-id]`, table).each((idx, elt) => {
              dtTable.row(elt).remove().draw();
            });
            $(result).each((idx, elt) => {
              const newRow = $(elt);
              dtTable.row.add(newRow).draw();
            });
            MyAMS.core.initContent(table).then();
            switcher.html('<i class="far fa-minus-square"></i>').addClass('expanded');
          });
        });
      }
    },
    /**
     * Custom tree element delete callback
     *
     * @param form: source form, which can be null if callback wasn't triggered from a form
     * @param options: callback options
     */
    deleteElement: (form, options) => {
      console.debug(options);
      const nodeId = options.node_id;
      if (nodeId) {
        $(`tr[data-ams-tree-node-parent-id="${nodeId}"]`).each((idx, elt) => {
          const table = $(elt).parents('table'),
            dtTable = table.DataTable();
          dtTable.row(elt).remove().draw();
        });
      }
    },
    /**
     * Sort and re-parent tree elements
     */
    sortTree: (evt, details) => {
      const table = $(evt.target),
        dtTable = table.DataTable(),
        data = $(table).data();
      let target = data.amsReorderUrl;
      if (target) {
        // Disable row click handler
        const row = $(data.amsReorderSource.node);
        row.data('ams-disabled-handlers', 'click');
        try {
          // Get root ID
          const tableID = row.parents('table').first().data('ams-tree-node-id');
          // Get moved row ID
          const rowID = row.data('ams-tree-node-id');
          const rowParentID = row.data('ams-tree-node-parent-id');
          // Get new parent ID
          const parent = row.prev('tr');
          let parentID, switcher, action;
          if (parent.exists()) {
            // Move below an existing row
            parentID = parent.data('ams-tree-node-id');
            // Check switcher state
            switcher = $(`.${data.amsTreeSwitcherClass || 'switcher'}`, parent);
            if (switcher.hasClass(data.amsTreeSwitcherExpandedClass || 'expanded')) {
              // Opened folder: move as child
              if (rowParentID === parentID) {
                // Don't change parent
                action = 'reorder';
              } else {
                // Change parent
                action = 'reparent';
              }
            } else {
              // Closed folder or simple item: move as sibling
              parentID = parent.data('ams-tree-node-parent-id');
              if (rowParentID === parentID) {
                // Don't change parent
                action = 'reorder';
              } else {
                // Change parent
                action = 'reparent';
              }
            }
          } else {
            // Move to site root
            parentID = tableID;
            switcher = null;
            if (rowParentID === parentID) {
              // Already child of site root
              action = 'reorder';
            } else {
              // Move from inner folder to site root
              action = 'reparent';
            }
          }
          // Call ordering target
          const localTarget = MyAMS.core.getFunctionByName(target);
          const postData = {
            action: action,
            child: rowID,
            parent: parentID,
            order: JSON.stringify($('tr[data-ams-tree-node-id]', table).listattr('data-ams-tree-node-id')),
            can_sort: !$('td.sorter', row).is(':empty')
          };
          if (typeof localTarget === 'function') {
            localTarget.call(table, dtTable, postData);
          } else {
            if (!target.startsWith(window.location.protocol)) {
              const location = data.amsLocation;
              if (location) {
                target = `${location}/${target}`;
              }
            }
            MyAMS.require('ajax').then(() => {
              MyAMS.ajax.post(target, postData).then(result => {
                const removeRow = rowID => {
                  const row = $(`tr[data-ams-tree-node-id="${rowID}"]`, table);
                  dtTable.row(row).remove().draw();
                };
                const removeChildRows = rowID => {
                  const childs = $(`tr[data-ams-tree-node-parent-id="${rowID}"]`, table);
                  childs.each((idx, elt) => {
                    const childRow = $(elt),
                      childID = childRow.attr('data-ams-tree-node-id');
                    removeChildRows(childID);
                    dtTable.row(childRow).remove().draw();
                  });
                };
                if (result.status) {
                  MyAMS.ajax.handleJSON(result);
                } else {
                  // Remove parent row if changed parent
                  if (postData.action === 'reparent') {
                    removeRow(parentID);
                  }
                  // Remove moved row children
                  removeChildRows(parentID);
                  removeChildRows(rowID);
                  dtTable.row(row).remove().draw();
                  let newRow, oldRow;
                  for (const resultRow of result) {
                    newRow = $(resultRow);
                    oldRow = $(`tr[id="${newRow.attr('id')}"]`);
                    dtTable.row(oldRow).remove().draw();
                    dtTable.row.add(newRow).draw();
                    MyAMS.core.initContent(newRow).then();
                  }
                }
              });
            });
          }
        } finally {
          // Restore row click handler
          setTimeout(function () {
            $(row).removeData('ams-disabled-handlers');
          }, 50);
        }
      }
      return false;
    }
  };

  /**
   * Global module initialization
   */
  if (window.MyAMS) {
    if (MyAMS.env.bundle) {
      MyAMS.config.modules.push('tree');
    } else {
      MyAMS.tree = tree;
      console.debug("MyAMS: tree module loaded...");
    }
  }
});
//# sourceMappingURL=mod-tree-dev.js.map
