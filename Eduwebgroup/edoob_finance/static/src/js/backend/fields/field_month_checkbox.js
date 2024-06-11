/** @odoo-module alias=edoob.finance.field.month_checkbox */

import field_registry from 'web.field_registry_owl';
import AbstractField from 'web.AbstractFieldOwl';

import {_lt} from 'web.core';

class FieldEdoobFinanceMonthCheckboxes extends AbstractField {
    template = 'edoob_finance.FieldMany2ManyCheckBoxes';
    supportedFieldTypes = ['char']
    description = _lt("Month checkbox")
    patched() {
        super.patched();
        this._setValue("Queso")
    }
}

field_registry.add('edoob_finance_month_checkboxes', FieldEdoobFinanceMonthCheckboxes);

return FieldEdoobFinanceMonthCheckboxes;

