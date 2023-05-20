languages = {
    'english': {
        'checking': {
            'checkout_user_barcode': 'User Barcode',
            'checkout_item_barcode': 'Item Barcode',
            'checkout_item_title': 'Item Title',
            'checkout_confirm': 'Checkout',
            'checkout_heading': 'Check Item Out',
            'checkout_view': 'View Checkouts',
            'checkout_invalid_error_title': 'Already Checked Out',
            'checkout_invalid_error_body': 'This item is already checked out to a user. This checkout cannot be '
                                           'completed at this time.',
            'checkout_invalid_barcode_title': 'Invalid Barcode',
            'checkout_invalid_barcode_body': 'The user or item barcode were invalid or do not exist.',
            'checkout_not_allowed_error_title': 'Checkout Not Permitted',
            'checkout_not_allowed_error_body': 'You are not presently allowed to checkout items. If you think this is '
                                               'a mistake, please contact an administrator.',
            'checkout_nonexistent_user_error_title': 'User Does Not Exist',
            'checkout_nonexistent_user_error_body': 'A user with that barcode does not exist. Please check the '
                                                    'barcode and try again.',
            'checkin_return': 'Return Item',
            'checkin_heading': 'Check Item In',
            'checkin_error_title': 'Not Checked Out',
            'checkin_error_body': 'That item does not exist or is not checked out.'
        },
        'developer': {
            'test_add': 'Add Test Item',
            'table_drop': 'Drop All Tables'
        },
        'general': {
            'home_tab': 'Home',
            'configure_server': 'Configure Server',
            'records_heading': 'Item Record',
            'create_message': 'Create Message of the Day',
            'create_message_short': 'Create MOTD'
        },
        'item_info': {
            'item_add_heading': 'Create Item',
            'item_manage_heading': 'Manage Item Info',
            'item_barcode': 'Barcode',
            'item_title': 'Title',
            'item_author': 'Author',
            'item_description': 'Item Description',
            'item_publish_date': 'Publish Date',
            'item_type': 'Item Type',
            'item_location': 'Location',
            'item_quantity': 'Item Quantity',
            'item_status': 'Status',
            'item_available': 'Available',
            'item_unavailable': 'Checked Out',
            'item_check_heading': 'Item Check',
            'item_action_check_in': 'Check In',
            'item_action_check_out': 'Check Out',
            'item_record_add': 'Add Record',
            'item_record_manage': 'Manage Record',
            'item_delete_all': 'Delete Record + Items',
            'missing_barcode_title': 'Barcode Missing',
            'missing_barcode_body': 'Items must have a barcode in order to be created.',
            'missing_field_title': 'Missing Field',
            'missing_field_body': 'Records must have a title field.',
            'item_cant_delete_error_title': 'Item Currently Checked Out',
            'item_cant_delete_error_body': 'Warning: An item with this barcode is currently checked out. This barcode '
                                           'CANNOT be deleted at this time.',
            'item_barcode_in_use_error_title': 'Barcode Already in Use',
            'item_barcode_in_use_error_body': 'Warning: This barcode is already in use. Please try a different barcode.',
            'item_delete': 'Delete Item',
            'item_not_selected_title': 'Please Select an Item',
            'item_not_selected_body': 'In order to manage an item, you must first select one.'
        },
        'locations': {
            'location_heading': 'Locations',
            'location_create': 'Create Location',
            'location_view': 'View Locations',
            'location_barcode': 'Location Barcode',
            'location_manage': 'Manage Location',
            'location_save': 'Save Location',
            'location_id': 'Location ID',
            'location_name': 'Location Name',
            'location_barcode_in_use_error_title': 'Barcode in Use',
            'location_barcode_in_use_error_body': 'This barcode is already in use for a location. Please try another.'
        },
        'login': {
            'login_heading': 'Login',
            'username': 'Username',
            'password': 'Password',
            'login_error_title': 'Incorrect Credentials',
            'login_error_body':  'Your username or password are incorrect. Please contact an administrator if this '
                                 'continues.',
            'logout': 'Logout'
        },
        'menubar': {
            'file_menu': 'File',
            'checkout_menu': 'Checkout',
            'users_menu': 'Users',
            'developer_menu': 'Admin',
            'help_menu': 'Help',
            'github': 'GitHub',
            'discord': 'Discord'
        },
        'prompts': {
            'prompt_accept': 'Okay',
            'prompt_add_item': 'Add Record',
            'prompt_add_item_to_record': 'Create Item From Record',
            'prompt_confirm': 'Confirm',
            'prompt_delete': 'Are you sure you would like to delete this? This cannot be undone.',
            'prompt_deny': 'Cancel',
            'prompt_exit': 'Close',
            'prompt_warning': 'Warning',
            'prompt_save_changes': 'Save Changes'
        },
        'settings': {
            'settings_heading': 'Settings',
            'settings': 'Settings',
            'setting_enabled': 'Enabled',
            'setting_disabled': 'Disabled',
            'settings_theme': 'Theme',
            'settings_version': 'Settings Version: ',
            'settings_update_check': 'Automatically Check for Updates',
            'settings_show_checkout': 'Show Checkout Menu',
            'settings_show_developer': 'Show Admin Menu',
            'settings_show_help': 'Show Help Menu',
            'settings_show_users': 'Show Users Menu',
            'settings_theme_dark': 'Dark',
            'settings_theme_light': 'Light',
            'settings_theme_system': 'System'
        },
        'update': {
            'update_heading': 'Update Checker',
            'update_last_checked': 'Last Checked',
            'update_available_version': 'Available Version',
            'update_current_version': 'Your Version',
            'update_get': 'Get Update',
            'update_check_for': 'Check for Updates',
        },
        'users': {
            'users_home_heading': 'Users',
            'user_create_heading': 'Add User',
            'user_barcode': 'User Barcode',
            'user_first_name': 'First Name',
            'user_last_name': 'Last Name',
            'user_id': 'ID',
            'user_birthday': 'Birthday',
            'user_email': 'Email',

            'user_add': 'Add User',
            'user_view': 'View All Users',
            'user_specific': 'View User',
            'user_manage': 'Manage User',
            'user_manage_save': 'Save User',

            'user_is_admin': 'Is User Admin',
            'user_allowed_checkouts': 'Allow User to Checkout',
            'user_allowed_item_management': 'Allow Item Management',
            'user_allowed_modification_of_users': 'Allow Modification of Users',

            'user_not_found_title': 'No User Found',
            'user_not_found_body': 'A user with that barcode does not exist. Please check that the barcode has been '
                                   'entered correctly.'

        }
    }
}
