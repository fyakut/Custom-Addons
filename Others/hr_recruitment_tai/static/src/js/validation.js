odoo.define('hr_recruitment_tai.validations', function (require) {
'use strict';

var basic_fields = require('web.basic_fields');
var field_registry = require('web.field_registry');
var FieldChar = basic_fields.FieldChar;

/**
 * FieldChar extension to suggest existing companies when changing the company
 * name on a res.partner view (indeed, it is designed to change the "name",
 * "website" and "image" fields of records of this model).
 */
var FieldPhone = FieldChar.extend({



    /**
     * @override of FieldChar (called when the user is typing text)
     * Checks the <input/> value and shows suggestions according to
     * this value.
     *
     * @private
     */
    _onInput: function () {
        this._super.apply(this, arguments);
        alert("validation here");
    },
});



var FieldEmail = FieldChar.extend({

    events: _.extend({}, FieldChar.prototype.events, {

        'focusout': '_onFocusout',
    }),


    _onFocusout: function () {
        var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if(!re.test(this.$input.val()))
        {
            alert('email invalid');
        }
    },

    /**
     * @override of FieldChar (called when the user is typing text)
     * Checks the <input/> value and shows suggestions according to
     * this value.
     *
     * @private
     */
    _onInput: function () {
        this._super.apply(this, arguments);

    },
});


field_registry.add('field_phone', FieldPhone);
field_registry.add('field_email', FieldEmail);


return {
    FieldPhone: FieldPhone,
    FieldEmail: FieldEmail
};
});
