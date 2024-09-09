/** @odoo-module alias='school.finance.list.controller' */

import ListController from "web.ListController";

ListController.include({
    _renderHeaderButtons() {
        const res = this._super(...arguments);
        const selectedRecords = !!this.selectedRecords.length;
        this.$buttons.find('.o_make_charge_student').toggle(selectedRecords);
        return res;
    },
    renderButtons(node) {
        this._super(...arguments);
        this.$buttons.on('click', '.o_make_charge_student', this._makeStudentChargeWizard.bind(this))
    },
    _makeStudentChargeWizard() {
        this.do_action('school_finance.action_make_student_charge');
    }
})