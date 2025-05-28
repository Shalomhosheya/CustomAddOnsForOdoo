odoo.define('custom_pos.pos_custom', function (require) {
    'use strict';

    const { PosComponent } = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class CustomButton extends PosComponent {
        async onClick() {
            try {
                // Show input popup to collect the custom note
                const { confirmed, payload } = await this.showPopup('TextInputPopup', {
                    title: this.env._t('Add Custom Note'),
                    confirmText: this.env._t('Save'),
                    cancelText: this.env._t('Cancel'),
                    value: this.env.pos.get_order().custom_note || '',
                });
                
                if (confirmed && payload !== undefined) {
                    const order = this.env.pos.get_order();
                    if (order) {
                        order.custom_note = payload;  // Set the custom note
                        this.env.pos.get_order().trigger('change', this.env.pos.get_order()); // Update UI
                    }
                }
            } catch (error) {
                console.error('Error in custom note popup:', error);
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('Failed to save note.'),
                });
            }
        }
    }

    CustomButton.template = 'CustomButton';

    Registries.Component.add(CustomButton);

    return CustomButton;
});
