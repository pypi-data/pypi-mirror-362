# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, tools
import email

try:
    from xmlrpc import client as xmlrpclib
except ImportError:
    import xmlrpclib


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def message_process(
        self,
        model,
        message,
        custom_values=None,
        save_original=False,
        strip_attachments=False,
        thread_id=None,
    ):
        thread_id = super(MailThread, self).message_process(
            model, message, custom_values, save_original, strip_attachments, thread_id
        )
        # extract message bytes - we are forced to pass the message as binary because
        # we don't know its encoding until we parse its headers and hence can't
        # convert it to utf-8 for transport between the mailgate script and here.
        if isinstance(message, xmlrpclib.Binary):
            message = bytes(message.data)
        if isinstance(message, str):
            message = message.encode("utf-8")
        message = email.message_from_bytes(message, policy=email.policy.SMTP)

        # parse the message, verify we are not in a loop by checking message_id is not duplicated
        msg_dict = self.message_parse(message, save_original=save_original)

        mail_mail = self.env["mail.mail"].search(
            [("message_id", "=", msg_dict.get("message_id"))]
        )
        if mail_mail:
            email_cc = set(tools.email_normalize_all(msg_dict.get("cc", "")))
            email_to = set(tools.email_normalize_all(msg_dict.get("to", "")))
            mail_mail.write(
                {
                    "email_cc": ",".join(sorted(email_cc)),
                    "email_to": ",".join(sorted(email_to)),
                }
            )
        return thread_id
