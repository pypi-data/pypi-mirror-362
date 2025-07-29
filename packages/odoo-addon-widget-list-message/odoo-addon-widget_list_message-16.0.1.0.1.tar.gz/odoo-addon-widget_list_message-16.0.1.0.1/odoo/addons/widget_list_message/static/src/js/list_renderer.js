/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { ListRenderer } from "@web/views/list/list_renderer";
import { useEffect, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

import { formatMessageField } from "./list_message_tooltip";


patch(ListRenderer.prototype, 'widget_list_message.MessageListRenderer', {
    setup() {
        this._super();

        useEffect(() => {            
            this.addMessageTooltips();
        });
    },

    addMessageTooltips() {
        this.tableRef.el.querySelectorAll('td.o_data_cell').forEach((cellEl) => {
            const cellName = cellEl.getAttribute('name');
            const cellId = cellEl.parentNode.getAttribute("data-id");
            
            if (!cellName || !cellId) return;

            const record = this.props.list.records.find(r => r.id === cellId)

            if (!record) return;

            if (cellName === 'body') {
                const message = {
                    email_from: formatMessageField(record.data.email_from),
                    email_to: formatMessageField(record.data.email_to),
                    email_cc: formatMessageField(record.data.email_cc),
                }
                cellEl.setAttribute(
                    'data-tooltip-template',
                    'widget_list_message.ListMessageTooltip'
                );
                cellEl.setAttribute('data-tooltip-props', JSON.stringify({
                    message: message
                }));
                cellEl.setAttribute('data-tooltip-info', JSON.stringify({
                    message: message
                }))
            }
        });
    }
});
