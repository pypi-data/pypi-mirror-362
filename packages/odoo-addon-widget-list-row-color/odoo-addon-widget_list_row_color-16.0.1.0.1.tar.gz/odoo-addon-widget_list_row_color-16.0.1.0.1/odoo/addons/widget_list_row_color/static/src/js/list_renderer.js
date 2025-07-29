/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { ListRenderer } from '@web/views/list/list_renderer';
import { useEffect } from "@odoo/owl";


patch(ListRenderer.prototype, 'list_renderer_color_row', {
    setup() {
        this._super(...arguments);
        const self = this;
        
        this.active_colors = this.props.list.context?.active_colors;
        this.rowColor = 'color_row';
        this.backgroundRowColor = 'color_background_row';

        useEffect(() => {
            if (this.active_colors) {
                this.setRowColors();
            }
        });
    },
    setRowColors(){
        this.tableRef.el.querySelectorAll(
            'tbody tr[data-id].o_data_row'
        ).forEach((rowEl) => {
            let record = this.props.list.records.find(
                (record) => record.id === rowEl.dataset.id
            );
            if (this.active_colors
                    && record.data.hasOwnProperty(this.rowColor)
                    && record.data[this.rowColor] !== null) {
                $(rowEl).css("color", record.data[this.rowColor].toString());
            }

            if (this.active_colors
                    && record.data.hasOwnProperty(this.backgroundRowColor)
                    && record.data[this.backgroundRowColor] !== null) {
                $(rowEl).css(
                    "background-color",
                    record.data[this.backgroundRowColor].toString()
                );
            }
        });
    },
});

export default ListRenderer;
