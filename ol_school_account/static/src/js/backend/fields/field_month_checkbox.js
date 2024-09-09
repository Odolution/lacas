/** @odoo-module alias=ol.finance.field.month_checkbox */

import field_registry from 'web.field_registry_owl';
import AbstractField from 'web.AbstractFieldOwl';

import {_lt} from 'web.core';

class FieldOlFinanceMonthCheckboxes extends AbstractField {
    template = 'ol_finance.FieldMany2ManyCheckBoxes';
    supportedFieldTypes = ['char']
    description = _lt("Month checkbox")
    patched() {
        super.patched();
        this._setValue("Queso")
    }
}

field_registry.add('ol_finance_month_checkboxes', FieldOlFinanceMonthCheckboxes);

return FieldOlFinanceMonthCheckboxes;

