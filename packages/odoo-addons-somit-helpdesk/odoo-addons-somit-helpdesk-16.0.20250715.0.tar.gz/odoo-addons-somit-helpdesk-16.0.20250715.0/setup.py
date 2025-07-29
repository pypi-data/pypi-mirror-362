import setuptools

with open("VERSION.txt", "r") as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-somit-helpdesk",
    description="Meta package for somit-helpdesk Odoo addons",
    version=version,
    install_requires=[
        "odoo-addon-api_common_base>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_automatic_stage_changes>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_automove>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_split_and_merge>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_stage_transition>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_activity_ids>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_api>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_board_logistics>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_contract_contract>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_document_pages>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_mail_message>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_massive_creation>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_subtags>=16.0dev,<16.1dev",
        "odoo-addon-helpdesk_ticket_to_lead>=16.0dev,<16.1dev",
        "odoo-addon-mail_activity_chatter>=16.0dev,<16.1dev",
        "odoo-addon-mail_activity_mail_template>=16.0dev,<16.1dev",
        "odoo-addon-mail_cc_and_to_text>=16.0dev,<16.1dev",
        "odoo-addon-widget_list_limit_cell>=16.0dev,<16.1dev",
        "odoo-addon-widget_list_message>=16.0dev,<16.1dev",
        "odoo-addon-widget_list_row_color>=16.0dev,<16.1dev",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Odoo",
        "Framework :: Odoo :: 16.0",
    ],
)
