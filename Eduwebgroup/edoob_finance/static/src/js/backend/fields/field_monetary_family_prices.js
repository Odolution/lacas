/** @odoo-module alias=edoob.finance.field.family_prices */

import field_registry from 'web.field_registry_owl';
import AbstractField from 'web.AbstractFieldOwl';

import { useService } from "@web/core/utils/hooks";

import {_lt} from 'web.core';

class FieldEdoobFinanceMonetaryFamilyPrices extends AbstractField {
    static template = 'edoob.finance.FieldMonetaryFamilyPrices';
    static fieldDependencies = {
        plan_pricelist_option: {type: 'selection'},
        plan_pricelist_id: {type: 'Many2one'},
        student_families: {type: 'Many2many'},
    }
    static supportedFieldTypes = ['monetary'];
    static description = _lt("Price");
    static resetOnAnyFieldChange = true;
    static isQuickEditable = true;

    setup() {
        this.rpc = useService("rpc");
    }

    get focusableElement() {
        return this.mode === 'readonly' ? null : this.el.querySelector('input');
    }

    get formattedValue() {
        return this._formatValue(this.value);
    }
    _onInput(ev) {
        this._setValue(ev.target.value);
    }
    async _showLinePrices(ev) {
        const action = await this.rpc({
            model: 'tuition.plan.line',
            method: 'action_show_family_prices',
            args: [this.recordData.id],
        })
        this.trigger('do_action', {action});
    }
}

field_registry.add('edoob_finance_family_prices', FieldEdoobFinanceMonetaryFamilyPrices);

return FieldEdoobFinanceMonetaryFamilyPrices;