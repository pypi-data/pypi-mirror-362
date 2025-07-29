from odoo import models


class MailActivity(models.Model):
    _inherit = ["mail.activity", "mail.thread"]
    _name = "mail.activity"
