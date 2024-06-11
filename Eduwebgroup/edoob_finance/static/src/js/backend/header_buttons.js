/** @odoo-module alias=school.finance.header.buttons */

import KanbanController from 'web.KanbanController';
import ListController from 'web.ListController';
import FormController from 'web.FormController';

import { ComponentWrapper } from 'web.OwlCompatibility';
const { Component } = owl;

export class SchoolMakeCharge extends Component {
    static template = 'school.finance.Make.charge'
    goToMakeChargeWizard() {
        const controller = this.props.controller;
        this.props.controller.do_action('edoob_finance.make_student_charge_action', {
            additional_context: {'active_ids': controller.getSelectedIds()},
        });
    }
}

FormController.include({
    _schoolMakeChargeButtonTarget: undefined,
    _schoolMakeChargeButton: undefined,

    /**
     * @override
     * @param {jQuery} [$node]
     */
    renderButtons($node) {
        this._super(...arguments);
        if (this.$buttons && this.modelName === 'school.student') {
            this._schoolMakeChargeButtonTarget = document.createElement('span');
            this.$buttons.find('div.o_form_buttons_view').append(this._schoolMakeChargeButtonTarget);
            window.a = this._schoolMakeChargeButtonTarget;
        }
    },

    /**
     * @override
     */
    async start() {
        const res = await this._super(...arguments);
        if (this.modelName === 'school.student' && this.$buttons && this.$buttons.length) {
            this._schoolMakeChargeButton = new ComponentWrapper(this, SchoolMakeCharge, {controller: this});
            await this._schoolMakeChargeButton.mount(this._schoolMakeChargeButtonTarget);
        }
        return res
    },
})

// ListController.include({
//     _schoolMakeChargeButtonTarget: undefined,
//     _schoolMakeChargeButton: undefined,
//
//     /**
//      * @override
//      * @param {jQuery} [$node]
//      */
//     _renderHeaderButtons() {
//         this._super(...arguments);
//         if (this.$headerButtons && this.modelName === 'school.student') {
//             this._schoolMakeChargeButtonTarget = document.createElement('span');
//             this.$buttons.find('div.o_form_buttons_view').append(this._schoolMakeChargeButtonTarget);
//             window.a = this._schoolMakeChargeButtonTarget;
//         }
//     },
//
//     /**
//      * @override
//      */
//     async start() {
//         const res = await this._super(...arguments);
//         if (this.modelName === 'school.student' && this.$buttons && this.$buttons.length) {
//             this._schoolMakeChargeButton = new ComponentWrapper(this, SchoolMakeCharge, {controller: this});
//             await this._schoolMakeChargeButton.mount(this._schoolMakeChargeButtonTarget);
//         }
//         return res
//     },
//
// })

// KanbanController.include({
//     /**
//      * @override
//      */
//     init() {
//         this._super(...arguments);
//         this._schoolEnrollButton = undefined;
//         this._schoolEnrollButtonTarget = undefined;
//     },
//
//     /**
//      * @override
//      * @param {jQuery} [$node]
//      */
//     renderButtons($node) {
//         this._super(...arguments);
//         if (this.$buttons && this.modelName === 'school.student') {
//             this._schoolEnrollButtonTarget = document.createElement('span');
//             this.$buttons.find('.o-kanban-button-new').replaceWith(this._schoolEnrollButtonTarget);
//         }
//     },
//
//     /**
//      * @override
//      */
//     async start() {
//         const res = await this._super(...arguments);
//         if (this.modelName === 'school.student' && this.$buttons && this.$buttons.length) {
//             this._schoolEnrollButton = new ComponentWrapper(this, SchoolEnrollButton, {btnStyleClass: 'btn-primary', controller: this});
//             await this._schoolEnrollButton.mount(this._schoolEnrollButtonTarget);
//         }
//         return res
//     }
// })

return {
    SchoolMakeCharge,
}