/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { ListRenderer } from '@web/views/list/list_renderer';
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

patch(ListRenderer.prototype, 'list_renderer_activity_ids', {
    setup() {
        this._super(...arguments);
        this.orm = useService("orm");
        this.action = useService("action");
    },

    async onCellClicked(record, column, ev) {
        if (this.props.list.model.root.resModel === "helpdesk.ticket"
            && this.props.list.resModel === "mail.activity"
        ) {
            const activityId = record.resId;
            
            const action = await this.orm.call(record.resModel, 'action_edit_activity', [activityId], {});
            if (!action) {
                this.doWarn(_t("No action found for this activity."));
                return;
            }
            this.action.doAction(action);
            return;
        }
        return await this._super(record, column, ev);
    },
});

export default ListRenderer;
